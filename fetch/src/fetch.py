import arxiv
from datetime import datetime, timedelta
import json
import os
def fetch_arxiv_updates(categories, keywords, days = 7):
    search_query = ' OR '.join([f'cat:{cat}' for cat in categories])
    search = arxiv.Search(search_query,max_results = 1000,sort_by = arxiv.SortCriterion.SubmittedDate)
    
    results = []
    for passage in search.results():
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
    
    return  results

def load_papers_from_json(file_path):
    nowtime = datetime.now().date()
    
    os.makedirs(file_path, exist_ok=True)
    papers = []
    all_files_and_dirs = os.listdir(file_path)
    all_files = [f for f in all_files_and_dirs if os.path.isfile(os.path.join(file_path, f)) and str(nowtime) in f]
    if len(all_files) == 0:
        return False
    for f in all_files:
        with open(os.path.join(file_path, f), 'r', encoding='utf-8') as file:
            paper = json.load(file)
            for p in paper:
                papers.append(p)
            
    return papers
        
    
        
    