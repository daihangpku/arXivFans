import arxiv
from datetime import datetime, timedelta
import json
import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import multiprocessing
from .download import down_load

def create_session_with_proxy(proxy):
    session = requests.Session()
    session.proxies.update(proxy)
    
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    
    return session

def multi_processing(results, categories, keywords, proxy):
    processes = []
    for category in categories:
        p = multiprocessing.Process(target=down_load, args=(results, keywords, proxy))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()


def fetch_arxiv_updates(categories, keywords, proxy, download_mode, days):
    search_query = ' OR '.join([f'cat:{cat}' for cat in categories])
    if not proxy == "":
        proxies = {
            'http': f'{proxy}',
            'https': f'{proxy}',
        }
        print("using proxy")
        session_with_proxy = create_session_with_proxy(proxies)
        arxiv.Client._session = session_with_proxy

    search = arxiv.Search(search_query,max_results = 1000,sort_by = arxiv.SortCriterion.SubmittedDate)
    print("searching finished")
    results = []
    result = []
    cnt = 0
    for passage in search.results():
        cnt += 1
        if passage.updated.date()>datetime.now().date()-timedelta(days=days):
            if any(keyword.lower() in passage.summary.lower() for keyword in keywords):
                results.append({
                    "title": passage.title,
                    "authors": [str(author) for author in passage.authors],
                    'published': passage.published,
                    'link': passage.entry_id,
                    'summary': passage.summary,
                    'category': categories,
                    'keyword': [keyword for keyword in keywords if keyword.lower() in passage.summary.lower()]
                })
                result.append({
                    "title": passage.title,
                    "authors": [str(author) for author in passage.authors],
                    'published': passage.published,
                    'link': passage.entry_id,
                    'summary': passage.summary,
                    'category': categories,
                    'keyword': [keyword for keyword in keywords if keyword.lower() in passage.summary.lower()]
                })
        if(cnt%100 == 0):
            down_load(result, keywords, proxy, download_mode)
            result = []
    if not result == []:
        down_load(result, keywords, proxy, download_mode)
    print("process finished")
    return  results

def load_papers_from_db():
    import sqlite3
    cwd = os.getcwd()
    with open(os.path.join(cwd, "local.txt"), 'r') as file:
        local=file.read()
    db_path = os.path.join(local, "download.db")

    if not os.path.exists(db_path):
        print(f"Database file does not exist at: {db_path}")
    else:
        results=[]
        try:
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            query = f"SELECT * FROM papers "

            cursor.execute(query)
            rows = cursor.fetchall()

            
            for row in rows:
                results.append({
                    "title": row[1],
                    'published': row[4],
                    'link': row[0],
                    'keyword': json.loads(row[2]),
                    'local_link': row[3]
                })
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()   
    return results
        
    
        
    
