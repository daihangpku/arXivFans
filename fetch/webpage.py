from flask import Flask, render_template_string
from src.fetch import load_papers_from_json
import os
from datetime import datetime
app = Flask(__name__)

@app.route('/')
def print_web():
    
    categories = ['cs.CV', 'cs.RO']
    cwd=os.getcwd()
    cwd=os.path.join(cwd,"output")
    
    
    updates = load_papers_from_json(cwd)
    if updates == False:
        print("请先更新")
        template = '''
            <html>
            <head>
                <title>No Available Updates, Please Update First</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        background-color: #f4f4f9;
                    }
                    .container {
                        width: 80%;
                        margin: auto;
                        overflow: hidden;
                    }
                    header {
                        background: #50b3a2;
                        color: #ffffff;
                        padding-top: 30px;
                        min-height: 70px;
                        border-bottom: #e8491d 3px solid;
                    }
                    header a {
                        color: #ffffff;
                        text-decoration: none;
                        text-transform: uppercase;
                        font-size: 16px;
                    }
                    header ul {
                        padding: 0;
                        list-style: none;
                    }
                    header li {
                        display: inline;
                        padding: 0 20px 0 20px;
                    }
                    .updates {
                        margin: 20px 0;
                        padding: 20px;
                        background: #ffffff;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    }
                   
                </style>
            </head>
            <body>
                <header>
                    <div class="container">
                        <h1>No Available Updates, Please Update First</h1>
                    </div>
                </header>
            <body>
            </html>
            '''





        return  render_template_string(template)
    
    template = '''
    <html>
    <head>
        <title>Arxiv Updates</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f9;
            }
            .container {
                width: 80%;
                margin: auto;
                overflow: hidden;
            }
            header {
                background: #50b3a2;
                color: #ffffff;
                padding-top: 30px;
                min-height: 70px;
                border-bottom: #e8491d 3px solid;
            }
            header a {
                color: #ffffff;
                text-decoration: none;
                text-transform: uppercase;
                font-size: 16px;
            }
            header ul {
                padding: 0;
                list-style: none;
            }
            header li {
                display: inline;
                padding: 0 20px 0 20px;
            }
            .updates {
                margin: 20px 0;
                padding: 20px;
                background: #ffffff;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            .update-item {
                border-bottom: 1px #cccccc solid;
                padding: 10px 0;
            }
            .update-item:last-child {
                border: none;
            }
            .update-title {
                font-size: 28px;
                font-weight: bold;
                color: #333333;
            }
            .update-authors {
                font-size: 24px;
                color: #666666;
            }
            .update-keywords {
                font-size: 24px;
                
                color: #333333;
            }
            .update-published {
                font-size: 18px;
                color: #999999;
            }
        </style>
    </head>
    <body>
        <header>
            <div class="container">
                <h1>Arxiv Updates</h1>
            </div>
        </header>
        <div class="container">
            <div class="updates">
            {% for update in updates %}
                <div class="update-item">
                    <a href="{{ update['link'] }}" class="update-title">{{ update['title'] }}</a>
                    <div class="update-authors">by {{ ', '.join(update['authors']) }}</div>
                    <div class="update-keywords">keywords: {{ ', '.join(update['keyword']) }}</div>
                    <div class="update-published">{{ update['published'] }}</div>
                </div>
            {% endfor %}
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template, updates=updates)



if __name__ == "__main__":
    with app.app_context():
        app.run(debug=False)