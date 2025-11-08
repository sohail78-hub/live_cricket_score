 # 🏏 Pakistan Cricket Live Dashboard

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)
![License](https://img.shields.io/badge/License-MIT-orange)

A beautiful, responsive **live cricket score dashboard** focused on **Pakistan cricket**, built with Python and Flask. It pulls real-time data from ESPNcricinfo RSS feeds to show live international matches and breaking news — perfect for fans who want everything in one place!

## 🔥 Features

✅ **Live International Matches Only**  
✅ **Pakistan-Focused News with Images**  
✅ **Auto-refresh Every 3 Minutes**  
✅ **Responsive Design (Mobile & Desktop)**  
✅ **Professional Layout Like Cricinfo**  
✅ **Reliable Flag Display & Fallback Images**  
✅ **Easy Setup – Just Run One Command**

### 📁 Project Structure

```Pakistan-cricket-live/
│
├── app.py                  ← Main Flask application
├── README.md               ← This file
│
├── templates/
│   └── index.html          ← Responsive HTML template with dynamic content
│
└── static/
    ├── styles.css          ← Modern CSS styling with gradients and hover effects
    ├── default-news.png    ← Fallback image for missing news thumbnails
    └── pakistan-flag.png   ← Local flag image (to avoid external dependencies)
```

### ✅ Key Files Explained

| File | Purpose |
|------|--------|
| `app.py` | Fetches live scores & news, filters only international/Pakistan-relevant content, serves the web page |
| `templates/index.html` | Clean, modern frontend with scrollable match cards and news grid |
| `static/styles.css` | Styling for a professional sports dashboard look |
| `static/default-news.png` | Shown when a news article has no image |
| `static/pakistan-flag.png` | High-quality Pakistan flag used in header |

## 🚀 How to Run (Step-by-Step)

You can create and run this project **from scratch using CLI or AI prompts like Gemini**.

### Step 1: Create Project Folder

```
mkdir pakistan-cricket-live
cd pakistan-cricket-live
```

### Step 2: Create Required Directories

```
mkdir templates
mkdir static
```

### Step 3: Create app.py

Use your terminal editor (nano, vim) or paste directly:

# app.py - Pakistan Cricket Live Dashboard

```
import requests
import xml.etree.ElementTree as ET
from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

# RSS Feeds
LIVE_SCORES_URL = "https://static.cricinfo.com/rss/livescores.xml"
PAK_NEWS_URL = "https://www.espncricinfo.com/rss/content/story/feeds/7.xml"

# Keywords for Pakistan relevance
PAK_KEYWORDS = ['Pakistan', 'PAK', 'PCB', 'PSL', 'Pak', 'Shaheen', 'Babar', 'Rizwan',
                'Haris', 'Shadab', 'Imam', 'Fakhar', 'Naseem', 'Mohammad', 'Afridi',
                'Khan', 'Karachi', 'Lahore', 'Quetta', 'Peshawar', 'Multan', 'Islamabad']

# Exclude domestic leagues
DOMESTIC_TEAMS = [
    'Glamorgan', 'Kent', 'Middlesex', 'Northamptonshire', 'Derbyshire',
    'Leicestershire', 'Gloucestershire', 'Lancashire', 'Hampshire',
    'Nottinghamshire', 'Sussex', 'Essex', 'Yorkshire', 'Surrey',
    'Warwickshire', 'Worcestershire', 'Baroda', 'Jharkhand', 'Haryana',
    'Uttarakhand', 'Police Sports Club', 'Colts Cricket Club'
]

INTERNATIONAL_TEAMS = [
    'India', 'Australia', 'England', 'Pakistan', 'New Zealand',
    'South Africa', 'West Indies', 'Sri Lanka', 'Afghanistan', 'Bangladesh'
]


def fetch_live_scores():
    try:
        response = requests.get(LIVE_SCORES_URL, timeout=10)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        scores = []

        for item in root.findall('.//item'):
            title_elem = item.find('title')
            desc_elem = item.find('description')
            link_elem = item.find('link')

            if not title_elem or not title_elem.text:
                continue

            title = title_elem.text.strip()
            description = desc_elem.text.strip() if desc_elem else ""
            link = link_elem.text.strip() if link_elem else "#"

            # Skip domestic matches
            if any(team in title for team in DOMESTIC_TEAMS):
                continue
            if not any(team in title for team in INTERNATIONAL_TEAMS):
                continue

            combined = f"{title} {description}".lower()
            if any(kw.lower() in combined for kw in PAK_KEYWORDS):
                scores.append({'title': title, 'description': description, 'link': link})

        return scores

    except Exception as e:
        print(f"[ERROR] Live scores: {e}")
        return []


def fetch_pakistan_news():
    try:
        response = requests.get(PAK_NEWS_URL, timeout=10)
        response.raise_for_status()

        ns = {'media': 'http://search.yahoo.com/mrss/'}
        root = ET.fromstring(response.content)
        articles = []

        for item in root.findall('.//item'):
            title_elem = item.find('title')
            desc_elem = item.find('description')
            link_elem = item.find('link')
            pub_date_elem = item.find('pubDate')
            cover_img = item.find('coverImages')
            media_content = item.find('media:content', ns)

            if not title_elem:
                continue

            img_url = (cover_img.text.strip() if cover_img is not None and cover_img.text else
                       media_content.get('url') if media_content is not None else None)

            articles.append({
                'title': title_elem.text.strip(),
                'description': desc_elem.text.strip() if desc_elem is not None else "",
                'link': link_elem.text.strip() if link_elem is not None else "#",
                'pub_date': pub_date_elem.text.strip() if pub_date_elem is not None else "",
                'image': img_url or "/static/default-news.png"
            })

        return articles

    except Exception as e:
        print(f"[ERROR] News: {e}")
        return []


@app.route('/')
def index():
    return render_template(
        'index.html',
        live_scores=fetch_live_scores(),
        pakistan_news=fetch_pakistan_news(),
        last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )


if __name__ == '__main__':
    app.run(debug=True)

```

## Step 4: Create templates/index.html
Create file: templates/index.html

Paste this code:
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Pakistan Cricket Live</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}" />
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet" />
</head>
<body>
    <header class="header">
        <div class="flag-container">
            <img src="{{ url_for('static', filename='pakistan-flag.png') }}" alt="Pakistan Flag" class="flag-img" />
        </div>
        <h1>Pakistan Cricket Live</h1>
        <p id="update-time">Last updated: {{ last_updated }}</p>
    </header>

    <main class="container">
        <!-- Live Matches -->
        <section class="section live-matches">
            <h2><i class="fas fa-cricket-bat-ball"></i> Live Matches</h2>
            {% if live_scores %}
                <div class="match-row">
                    {% for match in live_scores %}
                        <div class="match-card">
                            <div class="match-content">
                                <h3>{{ match.title }}</h3>
                                <p>{{ match.description }}</p>
                                <a href="{{ match.link }}" target="_blank" class="btn">Follow Match →</a>
                            </div>
                        </div>
                    {% endfor %}
                </div>
            {% else %}
                <p class="no-data">No live international matches at the moment.</p>
            {% endif %}
        </section>

        <!-- News Section -->
        <section class="section news-section">
            <h2><i class="fas fa-newspaper"></i> Pakistan Cricket News</h2>
            {% if pakistan_news %}
                <div class="news-grid">
                    {% for article in pakistan_news %}
                        <article class="news-card-pro">
                            <img src="{{ article.image }}" alt="News image" class="news-image" onerror="this.src='/static/default-news.png';">
                            <div class="news-body">
                                <h3>{{ article.title }}</h3>
                                <p class="news-desc">{{ article.description }}</p>
                                {% if article.pub_date %}
                                    <small class="news-date">{{ article.pub_date }}</small>
                                {% endif %}
                                <a href="{{ article.link }}" target="_blank" class="btn btn-small">Read Full Story</a>
                            </div>
                        </article>
                    {% endfor %}
                </div>
            {% else %}
                <p class="no-data">No recent news updates.</p>
            {% endif %}
        </section>
    </main>

    <footer>
        <p>Data from <a href="https://www.espncricinfo.com" target="_blank">ESPNcricinfo</a></p>
    </footer>

    <script>
        setTimeout(() => location.reload(), 180000); // Auto-refresh every 3 min
    </script>
</body>
</html>
```

## Step 5: Create static/styles.css
Create file: static/styles.css

```
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: 'Segoe UI', sans-serif;
    background: linear-gradient(135deg, #1a5276, #2874a6);
    color: #fff;
    line-height: 1.7;
    min-height: 100vh;
    padding-bottom: 70px;
}

/* Header */
.header {
    background: #000;
    text-align: center;
    padding: 1.5rem;
    border-bottom: 5px solid #f1c40f;
}
.flag-container { margin-bottom: 0.5rem; }
.flag-img { width: 70px; height: auto; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.4); }
.header h1 { color: #f1c40f; margin: 0; font-size: 1.9rem; }
#update-time { font-size: 0.95rem; opacity: 0.8; font-style: italic; }

.container { max-width: 1400px; margin: 2rem auto; padding: 0 1rem; }
.section h2 { color: #f1c40f; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.6rem; }

/* Live Matches Row */
.match-row {
    display: flex; gap: 1.2rem; overflow-x: auto; padding: 0.5rem 0 1.5rem;
}
.match-card {
    min-width: 300px; flex: 0 0 300px;
    background: white; color: #333; border-radius: 12px;
    padding: 1.3rem; box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    transition: transform 0.3s ease;
}
.match-card:hover { transform: translateY(-6px); }
.match-card h3 { color: #1a5276; font-size: 1.1rem; margin-bottom: 0.6rem; }
.match-card p { font-size: 0.95rem; color: #555; margin-bottom: 0.8rem; }

/* Buttons */
.btn {
    display: inline-block; background: #1a5276; color: white;
    padding: 0.6rem 1rem; border-radius: 6px; text-decoration: none;
    font-weight: bold; font-size: 0.9rem; transition: all 0.3s;
}
.btn:hover { background: #f1c40f; color: #000; transform: scale(1.05); }
.btn-small { padding: 0.5rem 0.8rem; font-size: 0.85rem; }

/* News Grid */
.news-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; }
.news-card-pro {
    background: white; color: #333; border-radius: 12px;
    overflow: hidden; box-shadow: 0 8px 16px rgba(0,0,0,0.15);
    transition: transform 0.3s ease;
}
.news-card-pro:hover { transform: translateY(-5px); }
.news-image { width: 100%; height: 180px; object-fit: cover; }
.news-body { padding: 1.2rem; }
.news-card-pro h3 { color: #1a5276; font-size: 1.1rem; margin-bottom: 0.6rem; }
.news-desc { font-size: 0.95rem; color: #555; margin-bottom: 0.8rem; }
.news-date { color: #7f8c8d; font-size: 0.85rem; display: block; margin-bottom: 0.8rem; }

.no-data {
    text-align: center; font-style: italic; color: #bdc3c7;
    padding: 2rem; background: rgba(255,255,255,0.1); border-radius: 8px;
}

footer {
    text-align: center; padding: 1rem; background: #000;
    color: #bdc3c7; font-size: 0.9rem;
}

@media (max-width: 768px) {
    .container { padding: 1rem; }
    .header h1 { font-size: 1.6rem; }
    .match-card { min-width: 280px; flex: 0 0 280px; }
}
```

## Step 7: Install Dependencies

```
pip install flask requests
```

## Step 8: Run the App

```
python app.py
```

Open: http://localhost:5000

## 🧠 Tips for Using with AI Prompts (Gemini, ChatGPT, etc.)
You can generate this entire project by giving an AI prompt like:

"Create a Flask app that shows live cricket scores and Pakistan cricket news from ESPNcricinfo RSS feeds. Show only international matches. Make it responsive with a Pakistan flag in the header, horizontal match row, and news cards with images." 

Then copy-paste each file and run step-by-step.

## 🛡️ Disclaimer
This app uses publicly available RSS feeds from ESPNcricinfo:

https://static.cricinfo.com/rss/livescores.xml
https://www.espncricinfo.com/rss/content/story/feeds/7.xml
Data is fetched in real time. No scraping or authentication required.

👉 Do not use for commercial purposes without permission.

### 🌟 Star If You Like It!
If you found this project helpful, please give it a ⭐ on GitHub!

### 📬 Feedback / Issues?
Have ideas or found bugs? Open an issue or contact me!

### 🏏 Powered by Python, Flask, and passion for Pakistan cricket!


To download this as a file, you can copy the entire content above and save it as `README.md` on your computer. The file contains all the necessary information about your project, including setup instructions, file structure, and usage guidelines.