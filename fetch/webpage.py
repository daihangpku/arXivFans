from flask import Flask, render_template_string, jsonify, request, send_from_directory
from src.fetch import load_papers_from_db
import os
from src.download import save_paper
global download_mode
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
    </style>
</head>
<body>
    <div class="container">
        <h1>Paper List</h1>
        <button class="refresh-button" onclick="fetchUpdates()">Refresh</button>
        <div class="checkbox-group" id="checkbox-group">
            <!-- 动态复选框项将被添加到这里 -->
        </div>
        <table>
            <thead>
                <tr>
                    <th>Title</th>
                    <th>Published date</th>
                    <th>Keywords</th>
                    <th>Link</th>
                    <th>Local link</th>
                </tr>
            </thead>
            <tbody id="paper-table-body">
                <!-- 论文行将被添加到这里 -->
            </tbody>
        </table>
    </div>

    <script>
        let currentSelectedKeywords = [];

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

                    console.log("Results:", results);  // 调试行，打印结果

                    // 提取唯一的关键词 
                    const keywords = [...new Set(results.flatMap(paper => paper.keywords))];
                    
                    // 保存当前选择的关键词
                    const checkboxes = document.querySelectorAll('input[name="keyword"]:checked');
                    currentSelectedKeywords = Array.from(checkboxes).map(checkbox => checkbox.value);

                    // 加载复选框
                    const checkboxGroup = document.getElementById('checkbox-group');
                    checkboxGroup.innerHTML = '';
                    keywords.forEach(keyword => {
                        const checkboxItem = document.createElement('div');
                        checkboxItem.className = 'checkbox-item';

                        const checkbox = document.createElement('input');
                        checkbox.type = 'checkbox';
                        checkbox.name = 'keyword';
                        checkbox.value = keyword;

                        const label = document.createElement('label');
                        label.className = 'checkbox-label';
                        label.textContent = keyword;

                        checkboxItem.appendChild(checkbox);
                        checkboxItem.appendChild(label);
                        checkboxGroup.appendChild(checkboxItem);

                        // 恢复复选框状态
                        if (currentSelectedKeywords.includes(keyword)) {
                            checkbox.checked = true;
                        }

                        // 添加复选框更改事件监听器
                        checkbox.addEventListener('change', updateTable);
                    });

                    // 更新表格
                    function updateTable() {
                        const tableBody = document.getElementById('paper-table-body');
                        tableBody.innerHTML = '';

                        const selectedKeywords = Array.from(document.querySelectorAll('input[name="keyword"]:checked'))
                                                      .map(checkbox => checkbox.value);

                        const filteredPapers = selectedKeywords.length > 0 ? 
                            results.filter(paper =>   paper.keywords.some(keyword => selectedKeywords.includes(keyword))) :
                            results;

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
                            if (paper.local_link) {
                                const localLink = document.createElement('a');
                                localLink.href = `/local-files/${paper.local_link}`;
                                localLink.textContent = "Local Link";
                                localLink.target = "_blank";
                                localLinkCell.appendChild(localLink);
                            } else {
                                localLinkCell.textContent = "N/A";
                            }
                            row.appendChild(localLinkCell);

                            tableBody.appendChild(row);
                        });
                    }

                    // 初始表格加载
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

        // 初始加载
        document.addEventListener('DOMContentLoaded', fetchUpdates);

        // 每当点击刷新按钮时获取更新
        document.addEventListener('click', event => {
            if (event.target.matches('.refresh-button')) {
                fetchUpdates();
            }
        });
    </script>
</body>
</html>
    '''
    return render_template_string(template, updates=updates)

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

@app.route('/local-files/<path:filename>')
def serve_local_files(filename):
    cwd = os.getcwd()
    local_files_directory = os.path.join(cwd, "papers")
    return send_from_directory(local_files_directory, filename)
import sys
if __name__ == "__main__":
    download_mode = sys.argv[1]
    print(download_mode)
    with app.app_context():
        app.run(debug=True)
