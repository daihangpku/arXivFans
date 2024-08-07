import argparse
import subprocess
import multiprocessing
import schedule
import time
from datetime import datetime
from src.fetch import fetch_arxiv_updates
from src.send_email import send_email
from src.download import is_paper_in_db
from src.download import init_db


def fetch_job(categories, keywords, proxy, email_sender, email_password, email_receiver, smtp_server, smtp_port):
    results = fetch_arxiv_updates(categories, keywords, proxy, days=7)
   
    init_db()
    new_papers = [paper for paper in results if not is_paper_in_db(paper['link'])]

    if email_sender == "" or email_password == "" or email_receiver == "" or smtp_server == "" or smtp_port == "":
        print("incomplete info for sending email")
    else:
        send_email(new_papers, email_sender, email_password, email_receiver, smtp_server, smtp_port)
    
    
    print("updated")
    print(str(datetime.now().date()))

def build_web():
    time.sleep(1)
    subprocess.run(['python', 'fetch/webpage.py'])

def main():
    parser = argparse.ArgumentParser(description='Process category and keywords.')
    parser.add_argument('--category', nargs='+', default=['cs.CV', 'cs.RO'], help='List of categories')
    parser.add_argument('--keywords', nargs='+', default=['radiance field',"deep learning"], help='List of keywords')
    parser.add_argument('--proxy', type=str, default="", help='Proxy settings')
    parser.add_argument('--email_sender', type=str, default="", help='Sender email address')
    parser.add_argument('--email_password', type=str, default="", help='Sender email password')
    parser.add_argument('--email_receiver', type=str, default="", help='Receiver email address')
    parser.add_argument('--frequency', type=str, default="", help='regular update')
    parser.add_argument('--smtp_server', type=str, default="", help="your smtp server's address")
    parser.add_argument('--smtp_port', type=str, default="", help='smtp port')
    args = parser.parse_args()
    categories = args.category
    keywords = args.keywords
    proxy = args.proxy
    email_sender = args.email_sender
    email_password = args.email_password
    email_receiver = args.email_receiver
    smtp_server = args.smtp_server
    smtp_port = args.smtp_port
    frequency = args.frequency
    print(f"you are searching {categories} for {keywords}.")

    if frequency.lower() == "daily":
        schedule.every().day.at("08:00").do(fetch_job, categories, keywords, proxy, email_sender, email_password, email_receiver, smtp_server, smtp_port)
        print("scheduled at 8 a.m. everyday\n")
        while True:
            schedule.run_pending()
            
            time.sleep(60)
    else:
        p = multiprocessing.Process(target = build_web)
        p.start()
        print(f"主进程正在运行 ")
        fetch_job(categories, keywords, proxy, email_sender, email_password, email_receiver, smtp_server, smtp_port)
        p.join()
        
    

if __name__=="__main__":
    main()
