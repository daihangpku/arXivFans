import requests
import os
import sqlite3
import logging
from datetime import datetime
import arxiv

def init_db():
    conn = sqlite3.connect('download.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS papers
                 (id TEXT PRIMARY KEY, title TEXT, keyword TEXT)''')
    conn.commit()
    conn.close()

def is_paper_in_db(paper_id):
    conn = sqlite3.connect('download.db')
    c = conn.cursor()
    c.execute("SELECT 1 FROM papers WHERE id = ?", (paper_id,))
    exists = (c.fetchone() is not None)
    conn.close()
    return exists

def save_db(update):
    if is_paper_in_db(update['link']):
        return False
    else:
        conn = sqlite3.connect('download.db')
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO papers (id, title, keyword) VALUES (?, ?, ?)",
              (update['link'], update['title'], update['keyword'][0]))
        conn.commit()
        conn.close()
        return True

def save_paper(update, keyword, proxy):
    
    pdf_url = update['link'].replace('abs', 'pdf')
    if proxy:
        proxies = {
            'http': f'http://{proxy}',
            'https': f'https://{proxy}',
        }
        response = requests.get(pdf_url,proxies=proxies)
    else:
        response = requests.get(pdf_url)
    
    published_date = datetime.strptime(update['published'], '%Y-%m-%d %H:%M:%S').date()
    filename = f"{published_date.strftime('%Y-%m-%d')}_{'_'.join(update['title'][:50].split())}.pdf"
    directory = os.path.join('papers', keyword)
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)

def down_load(updates, keywords, proxy):
    init_db()
    for keyword in keywords:
        for update in updates:
            if any(key == keyword for key in update["keyword"]):
                if save_db(update):
                    save_paper(update, keyword, proxy)

