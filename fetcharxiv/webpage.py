from flask import Flask, render_template_string, jsonify, request, send_from_directory
from .src.fetch import load_papers_from_db
import os
from .src.download import save_paper
import webbrowser
import sys
import threading
global download_mode
global keywords_show

app = Flask(__name__)

def get_updates():
    updates = load_papers_from_db()
    if not updates:
        return []
    updates.sort(key=lambda x: x['published'], reverse=True)
    return updates

def handle_link_click(url):
    if download_mode == "1" or download_mode == "2":
        save_paper(url)
    return {"status": "success", "message": f"Handled link click for {url}"}

def handle_download(url):
    filename = save_paper(url)
    return {"status": "success", "message": f"Paper downloaded from {url}", "local_link": filename}

@app.route('/')
def index():
    updates = get_updates()
    template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Paper List</title>
    <style>
        body {
            font-size: 20px;
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            margin: 0;
            padding: 20px;
        }
        h1 {
            text-align: center;
        }
        .container {
            max-width: 1800px;
            margin: 0 auto;
            background: #fff;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .checkbox-group {
            max-height: 150px;
            overflow-y: auto;
            border: 1px solid #ddd;
            padding: 10px;
            margin-bottom: 20px;
        }
        .checkbox-item {
            display: flex;
            align-items: center;
            margin: 5px 0;
        }
        .checkbox-item input {
            margin-right: 10px;
        }
        .checkbox-label {
            font-size: 1.1em;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        table, th, td {
            border: 1px solid #ddd;
        }
        th, td {
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        tr:hover {
            background-color: #f1f1f1;
        }
        .refresh-button {
            display: block;
            margin: 20px auto;
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 1em;
        }
        .refresh-button:hover {
            background-color: #45a049;
        }
        .download-button {
            display: inline-block;
            padding: 5px 10px;
            background-color: #2196F3;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.9em;
        }
        .download-button:hover {
            background-color: #1E88E5;
        }
        .local-link-cell {
            width: 150px; 
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Paper List</h1>
        <button class="refresh-button" onclick="fetchUpdates()">Refresh</button>
        <div class="checkbox-group" id="checkbox-group">
            <!-- Dynamic checkbox items will be added here -->
        </div>
        <table>
            <thead>
                <tr>
                    <th>Title</th>
                    <th>Published date</th>
                    <th>Keywords</th>
                    <th>Link</th>
                    <th class="local-link-cell">Local link</th>
                </tr>
            </thead>
            <tbody id="paper-table-body">
                <!-- Paper rows will be added here -->
            </tbody>
        </table>
    </div>

    <script>
        let currentSelectedKeywords = [];
        const keywordsShow = {{ keywords_show|tojson }};

        function fetchUpdates() {
            fetch('/get-updates')
                .then(response => response.json())
                .then(updates => {
                    const results = updates.map(paper => ({
                        title: paper['title'],
                        published: paper['published'],
                        keywords: paper['keyword'],
                        link: paper['link'],
                        local_link: paper['local_link']
                    }));

                    console.log("Results:", results);  // Debug line to print results

                    // Extract unique keywords and filter by keywordsShow
                    const keywords = [...new Set(results.flatMap(paper => paper.keywords))]
                        .filter(keyword => keywordsShow.includes(keyword));

                    // Save currently selected keywords
                    const checkboxes = document.querySelectorAll('input[name="keyword"]:checked');
                    currentSelectedKeywords = Array.from(checkboxes).map(checkbox => checkbox.value);

                    // Load checkboxes
                    const checkboxGroup = document.getElementById('checkbox-group');
                    checkboxGroup.innerHTML = '';
                    keywords.forEach(keyword => {
                        const checkboxItem = document.createElement('div');
                        checkboxItem.className = 'checkbox-item';

                        const checkbox = document.createElement('input');
                        checkbox.type = 'checkbox';
                        checkbox.name = 'keyword';
                        checkbox.value = keyword;
                        checkbox.checked = true; // Default all checkboxes to checked

                        const label = document.createElement('label');
                        label.className = 'checkbox-label';
                        label.textContent = keyword;

                        checkboxItem.appendChild(checkbox);
                        checkboxItem.appendChild(label);
                        checkboxGroup.appendChild(checkboxItem);

                        // Restore checkbox state
                        if (currentSelectedKeywords.includes(keyword)) {
                            checkbox.checked = true;
                        }

                        // Add change event listener
                        checkbox.addEventListener('change', updateTable);
                    });

                    // Update table
                    function updateTable() {
                        const tableBody = document.getElementById('paper-table-body');
                        tableBody.innerHTML = '';

                        const selectedKeywords = Array.from(document.querySelectorAll('input[name="keyword"]:checked'))
                                                      .map(checkbox => checkbox.value);

                        const filteredPapers = selectedKeywords.length > 0 ? 
                            results.filter(paper => paper.keywords.some(keyword => selectedKeywords.includes(keyword))) :
                            [];

                        filteredPapers.forEach(paper => {
                            const row = document.createElement('tr');

                            const titleCell = document.createElement('td');
                            titleCell.textContent = paper.title;
                            row.appendChild(titleCell);

                            const publishedCell = document.createElement('td');
                            publishedCell.textContent = paper.published;
                            row.appendChild(publishedCell);

                            const keywordCell = document.createElement('td');
                            keywordCell.textContent = paper.keywords;
                            row.appendChild(keywordCell);

                            const linkCell = document.createElement('td');
                            const link = document.createElement('a');
                            link.href = paper.link;
                            link.textContent = "Link";
                            link.target = "_blank";
                            link.addEventListener('click', (event) => {
                                event.preventDefault();
                                handleLinkClick(paper.link, link.href);
                            });
                            linkCell.appendChild(link);
                            row.appendChild(linkCell);

                            const localLinkCell = document.createElement('td');
                            localLinkCell.className = 'local-link-cell';
                            if (paper.local_link) {
                                const localLink = document.createElement('a');
                                localLink.href = `/local-files/${paper.local_link}`;
                                localLink.textContent = "Local Link";
                                localLink.target = "_blank";
                                localLinkCell.appendChild(localLink);
                            } else {
                                const downloadButton = document.createElement('button');
                                downloadButton.className = 'download-button';
                                downloadButton.textContent = 'Download';
                                downloadButton.addEventListener('click', () => handleDownload(paper.link, downloadButton));
                                localLinkCell.appendChild(downloadButton);
                            }
                            row.appendChild(localLinkCell);

                            tableBody.appendChild(row);
                        });
                    }

                    // Initial table load
                    updateTable();
                });
        }

        function handleLinkClick(url, href) {
            fetch('/handle-link-click', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: url })
            })
            .then(response => response.json())
            .then(data => {
                console.log("Link click handled:", data);
                window.open(href, '_blank');
            });
        }

        function handleDownload(url, button) {
            button.textContent = 'Downloading...';
            button.disabled = true;
            fetch('/handle-download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: url })
            })
            .then(response => response.json())
            .then(data => {
                console.log("Download handled:", data);
                if (data.status === "success") {
                    const localLink = document.createElement('a');
                    localLink.href = `/local-files/${data.local_link}`;
                    localLink.textContent = "Local Link";
                    localLink.target = "_blank";
                    button.parentElement.appendChild(localLink);
                    button.remove();
                } else {
                    button.textContent = 'Download';
                    button.disabled = false;
                }
            });
        }

        // Initial load
        document.addEventListener('DOMContentLoaded', fetchUpdates);

        // Fetch updates when refresh button is clicked
        document.addEventListener('click', event => {
            if (event.target.matches('.refresh-button')) {
                fetchUpdates();
            }
        });
    </script>
</body>
</html>
    '''
    return render_template_string(template, updates=updates, keywords_show=keywords_show)

@app.route('/get-updates')
def get_updates_route():
    updates = get_updates()
    return jsonify(updates)

@app.route('/handle-link-click', methods=['POST'])
def handle_link_click_route():
    data = request.get_json()
    url = data.get('url')
    result = handle_link_click(url)
    return jsonify(result)

@app.route('/handle-download', methods=['POST'])
def handle_download_route():
    data = request.get_json()
    url = data.get('url')
    result = handle_download(url)
    return jsonify(result)

@app.route('/local-files/<path:filename>')
def serve_local_files(filename):
    cwd = os.getcwd()
    with open(os.path.join(cwd, "local.txt"), 'r') as file:
        local= file.read()
    local_files_directory = os.path.join(local, "papers")
    return send_from_directory(local_files_directory, filename)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")



if __name__ == "__main__":
    download_mode = sys.argv[1]
    length = int(sys.argv[2])
    keywords_show = []
    for i in range(3, 3+length):
        keywords_show.append(sys.argv[i])
    print(keywords_show)
    
    print(download_mode)
    
    threading.Timer(1, open_browser).start()  # 自动打开浏览器
    with app.app_context():
        app.run(debug=True)
