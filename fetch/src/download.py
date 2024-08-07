import requests
import os
import sqlite3
import logging
from datetime import datetime
import json

def init_db():
    cwd = os.getcwd()
    conn = sqlite3.connect(os.path.join(cwd, "download.db"))
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS papers
                     (id TEXT PRIMARY KEY, title TEXT, keyword TEXT, local_link TEXT, date TEXT)''')
    conn.commit()
    conn.close()

def get_paper_by_id(paper_id):
    cwd = os.getcwd()
    conn = sqlite3.connect(os.path.join(cwd, "download.db"))
    c = conn.cursor()
    c.execute("SELECT * FROM papers WHERE id = ?", (paper_id,))
    paper = c.fetchone()
    conn.close()
    return paper

def is_paper_in_db(paper_id):
    cwd = os.getcwd()
    conn = sqlite3.connect(os.path.join(cwd, "download.db"))
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM papers WHERE id = ?", (paper_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def save_db(update):
    paper = get_paper_by_id(update['link'])
    cwd = os.getcwd()
    conn = sqlite3.connect(os.path.join(cwd, "download.db"))
    cursor = conn.cursor()
    
    if paper:
        # 如果 ID 存在，检查并更新关键字字段
        existing_keywords = json.loads(paper[2])
        new_keywords = update['keyword']
        updated_keywords = list(set(existing_keywords + new_keywords))
        cursor.execute("UPDATE papers SET keyword = ? WHERE id = ?", (json.dumps(updated_keywords), update['link']))
    else:
        # 如果 ID 不存在，插入新记录
        cursor.execute("INSERT INTO papers (id, title, keyword, date) VALUES (?, ?, ?, ?)",
                       (update['link'], update['title'], json.dumps(update['keyword']), str(update['published'])))
    
    conn.commit()
    conn.close()
    return True

def save_paper(update, keyword, proxy):
    pdf_url = update['link'].replace('abs', 'pdf')
    if proxy:
        proxies = {
            'http': f'{proxy}',
            'https': f'{proxy}',
        }
        response = requests.get(pdf_url, proxies=proxies)
    else:
        response = requests.get(pdf_url)
    
    published_date = str(update['published'])
    filename = f"{published_date}_{'_'.join(update['title'][:50].split())}.pdf"
    directory = os.path.join('papers', keyword)
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)

def down_load(updates, keywords, proxy = ""):
    init_db()
    for keyword in keywords:
        for update in updates:
            if any(key == keyword for key in update["keyword"]):
                if save_db(update):
                    #save_paper(update, keyword, proxy)
                    pass

def fetch_all_papers():
    cwd = os.getcwd()
    conn = sqlite3.connect(os.path.join(cwd, "download.db"))
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM papers")
    rows = cursor.fetchall()
    conn.close()
    
    papers = []
    for row in rows:
        paper = {
            'id': row[0],
            'title': row[1],
            'keyword': json.loads(row[2]),  # 将关键字从 JSON 字符串转换回列表
            'local_link': row[3],
            'date': row[4]
        }
        papers.append(paper)
    
    for paper in papers:
        print(paper)

def update_local_link(paper_id, local_link):
    cwd = os.getcwd()
    conn = sqlite3.connect(os.path.join(cwd, "download.db"))
    cursor = conn.cursor()
    cursor.execute("UPDATE papers SET local_link = ? WHERE id = ?", (local_link, paper_id))
    conn.commit()
    conn.close()

if __name__=="__main__":
    updates = [{'link': 'id1', 'title': 'title1', 'keyword': ['AI'], 'published': '2023-08-07 12:00:00'}, ]
    keywords = ['AI', 'Machine Learning']
    proxy = None
    
    #down_load(updates, keywords, proxy)
    fetch_all_papers()
    #updates = [{'link': 'id1', 'title': 'title1', 'keyword': ['Machine Learning'], 'published': '2023-08-07 12:00:00'}, ]
    #down_load(updates, keywords, proxy)
    fetch_all_papers()

