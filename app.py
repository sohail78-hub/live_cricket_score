# app.py - Cricket Live Score Dashboard (Updated)

import requests
import xml.etree.ElementTree as ET
from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

# RSS Feed URLs
LIVE_SCORES_URL = "https://static.cricinfo.com/rss/livescores.xml"
PAK_NEWS_URL = "https://www.espncricinfo.com/rss/content/story/feeds/7.xml"

# Keywords for Pakistan-related content
PAK_KEYWORDS = [
    'Pakistan', 'PAK', 'PCB', 'PSL', 'Pak', 'Shaheen', 'Babar', 'Rizwan',
    'Haris', 'Shadab', 'Imam', 'Fakhar', 'Naseem', 'Mohammad', 'Afridi',
    'Khan', 'Karachi', 'Lahore', 'Quetta', 'Peshawar', 'Multan', 'Islamabad',
    'Sultans', 'Qalandars', 'Gladiators', 'United', 'Zalmi', 'Wahab',
    'Hasan', 'Imad', 'Sohaib', 'Asia Cup', 'Ind vs Pak'
]

# List of domestic leagues/teams to exclude
DOMESTIC_TEAMS = [
    'Glamorgan', 'Kent', 'Middlesex', 'Northamptonshire', 'Derbyshire',
    'Leicestershire', 'Gloucestershire', 'Lancashire', 'Hampshire',
    'Nottinghamshire', 'Sussex', 'Essex', 'Yorkshire', 'Surrey',
    'Warwickshire', 'Worcestershire', 'Baroda', 'Jharkhand', 'Haryana',
    'Uttarakhand', 'Police Sports Club', 'Colts Cricket Club',
    'Band-e-Amir Dragons', 'Speen Ghar Tigers', 'Amo Sharks', 'Mis Ainak Knights'
]

# International teams (for filtering)
INTERNATIONAL_TEAMS = [
    'India', 'Australia', 'England', 'Pakistan', 'New Zealand', 'South Africa',
    'West Indies', 'Sri Lanka', 'Afghanistan', 'Bangladesh', 'Zimbabwe', 'Ireland'
]


def fetch_live_scores():
    """Fetch live scores and show only international matches"""
    try:
        response = requests.get(LIVE_SCORES_URL, timeout=10)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        scores = []

        for item in root.findall('.//item'):
            title_elem = item.find('title')
            desc_elem = item.find('description')
            link_elem = item.find('link')

            if title_elem is None or not title_elem.text:
                continue

            title = title_elem.text.strip()
            description = desc_elem.text.strip() if desc_elem is not None else ""
            link = link_elem.text.strip() if link_elem is not None else "#"

            # Skip if any domestic team is mentioned
            if any(team in title for team in DOMESTIC_TEAMS):
                continue

            # Must include at least one international team
            if not any(team in title for team in INTERNATIONAL_TEAMS):
                continue

            # Optional: still apply Pakistan relevance filter
            combined = f"{title} {description}".lower()
            if any(kw.lower() in combined for kw in PAK_KEYWORDS):
                scores.append({
                    'title': title,
                    'description': description,
                    'link': link
                })

        return scores

    except Exception as e:
        print(f"[ERROR] Failed to fetch live scores: {e}")
        return []


def fetch_pakistan_news():
    """Fetch Pakistan cricket news with image support"""
    try:
        response = requests.get(PAK_NEWS_URL, timeout=10)
        response.raise_for_status()

        ns = {
            'media': 'http://search.yahoo.com/mrss/',
            'atom': 'http://www.w3.org/2005/Atom'
        }

        root = ET.fromstring(response.content)
        articles = []

        for item in root.findall('.//item'):
            title_elem = item.find('title')
            desc_elem = item.find('description')
            link_elem = item.find('link')
            pub_date_elem = item.find('pubDate')
            cover_img_elem = item.find('coverImages')
            media_content = item.find('media:content', ns)

            if title_elem is None or not title_elem.text:
                continue

            article = {
                'title': title_elem.text.strip(),
                'description': desc_elem.text.strip() if desc_elem is not None else "",
                'link': link_elem.text.strip() if link_elem is not None else "#",
                'pub_date': pub_date_elem.text.strip() if pub_date_elem is not None else ""
            }

            img_url = None
            if cover_img_elem is not None and cover_img_elem.text:
                img_url = cover_img_elem.text.strip()
            elif media_content is not None:
                img_url = media_content.get('url')

            article['image'] = img_url or "/static/default-news.png"
            articles.append(article)

        return articles

    except Exception as e:
        print(f"[ERROR] Failed to fetch Pakistan news: {e}")
        return []


@app.route('/')
def index():
    live_scores = fetch_live_scores()
    pakistan_news = fetch_pakistan_news()
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template(
        'index.html',
        live_scores=live_scores,
        pakistan_news=pakistan_news,
        last_updated=last_updated
    )


if __name__ == '__main__':
    app.run(debug=True)