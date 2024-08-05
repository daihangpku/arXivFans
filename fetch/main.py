import argparse
import subprocess
import multiprocessing
import schedule
import time
from datetime import datetime
from src.fetch import fetch_arxiv_updates
from src.send_email import send_email
from src.download import down_load 
from src.download_entry import entry
from src.download import is_paper_in_db
from src.download import init_db

def multi_processing(results, categories, keywords, proxy):
    processes = []
    for category in categories:
        p = multiprocessing.Process(target=down_load, args=(results, keywords, proxy))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
def fetch_job(categories, keywords, proxy, email_sender, email_password, email_receiver):
    results = fetch_arxiv_updates(categories, keywords, days=7)
   
    init_db()
    new_papers = [paper for paper in results if not is_paper_in_db(paper['link'])]
    entry(new_papers,keywords)

    send_email(new_papers, email_sender, email_password, email_receiver)
    #"daihang2300012956@163.com""YKMFASYCKWRMKCEU"
    
    
    multi_processing(results, categories, keywords, proxy)
    print("updated")
    print(str(datetime.now().date()))
def main():
    parser = argparse.ArgumentParser(description='Process category and keywords.')
    parser.add_argument('--category', nargs='+', default=['cs.CV', 'cs.RO'], help='List of categories')
    parser.add_argument('--keywords', nargs='+', default=['radiance field',"deep learning"], help='List of keywords')
    parser.add_argument('--proxy', type=str, default="", help='Proxy settings')
    parser.add_argument('--email_sender', type=str, required=True, help='Sender email address')
    parser.add_argument('--email_password', type=str, required=True, help='Sender email password')
    parser.add_argument('--email_receiver', type=str, required=True, help='Receiver email address')
    parser.add_argument('--frequency', type=str, default="", help='regular update')
    args = parser.parse_args()
    categories = args.category
    keywords = args.keywords
    proxy = args.proxy
    email_sender = args.email_sender
    email_password = args.email_password
    email_receiver = args.email_receiver
    print(keywords)
    print(categories)
    frequency = args.frequency
    if frequency.lower() == "daily":
        schedule.every().day.at("08:00").do(fetch_job, categories, keywords, proxy, email_sender, email_password, email_receiver)
        print("scheduled at 8 a.m. everyday\n")
        while True:
            schedule.run_pending()
            
            time.sleep(60)
    else:
        fetch_job(categories, keywords, proxy, email_sender, email_password, email_receiver)
        
    subprocess.run(['python', 'webpage.py'])


if __name__=="__main__":
    main()