# arXivFans 中文版用户指南

ArXivFans 提供了一种高效的方式，从 arXiv 获取最新的论文，并通过电子邮件通知或网页界面进行查看。通过简单的配置和命令行操作，您可以轻松获取您所在领域的最新研究动态。

## 用户指南

本指南将帮助您了解如何使用此项目从 arXiv 获取更新，将其下载到本地，并通过电子邮件通知或本地网页界面查看结果。

---

### 第一步：安装和配置

1. **克隆代码库**：
   首先，将项目代码克隆到本地计算机。
   ```bash
   conda create -n arxivfans python=3.8
   conda activate arxivfans
   git clone <repository_url>
   cd arXivFans
   ```

2. **安装依赖项**：
   确保您的系统安装了 Python >=3.8。然后，安装所需的 Python 包：
   ```bash
   pip install .
   ```

---

### 第二步：获取 arXiv 更新

您可以通过命令行运行 `main.py` 脚本来获取 arXiv 的最新更新。

#### 快速开始
```bash
fetch --category cs.CV cs.RO --keywords "keyword1" "keyword2"
```
您可以根据需要更改 `cs.CV`、`cs.RO` 和 `keyword1`、`keyword2`。

#### 完整参数
```bash
fetch --category cs.CV cs.RO --keywords "deep learning" "radiance field" --proxy http://proxy.example.com:8080 --email_sender your_email@example.com --email_password your_password --email_receiver recipient@example.com --frequency daily --smtp_server smtp.xxx.com --smtp_port 25orxxx --days 5 --download_mode 0/1/2 --view_keywords "keyword1" "keyword2" --local ".local"
```

#### 参数说明：
##### 必要参数

- **`--category`**: 指定您想要搜索的 arXiv 类别。例如，`cs.CV`（计算机视觉）、`cs.RO`（机器人学）。
- **`--keywords`**: 根据指定的关键词过滤论文。例如，“deep learning”、“radiance field”。多个关键词用空格分隔，它们会与论文摘要匹配。

##### 可选参数
- **`--proxy`**: 如果需要网络代理访问，指定代理服务器。
- **`--email_sender`**: 用于发送通知的电子邮件地址。
- **`--email_password`**: 发送者电子邮件的 SMTP 密码。
- **`--email_receiver`**: 接收通知的电子邮件地址。
- **`--frequency`**: 使用“daily”表示每天早上8点获取更新。否则，可省略此参数。
- **`--smtp_server`**: 指定您的 SMTP 服务器地址。
- **`--smtp_port`**: 指定您的 SMTP 服务器端口。默认情况下，SMTP 通常使用端口 25，但如果使用加密（如 SSL 或 TLS），可能会使用其他端口（如 465 或 587）。
- **`--days`**: 指定查询结果的天数（建议 <=7，默认=3）。
- **`--download_mode`**: 指定下载模式：0 表示不下载，1 表示下载访问过的论文，2 表示下载所有论文（默认=1）。
- **`--view_keywords`**: 在网页上显示的论文与这些关键词相关。
- **`--local`**: （绝对路径）您希望数据库和论文保存的本地位置（默认=".local/arxivfans"）。

注意，缺少 `email_sender`、`email_password`、`email_receiver`、`smtp_server` 或 `smtp_port` 中的任何一个参数，将无法发送电子邮件通知。

#### 执行结果：

- 系统将从过去几天中，匹配指定类别和关键词的最新论文。
- 下载的论文将存储在本地。如果有更新，您将收到电子邮件通知。
- 如果使用代理服务器，请确保提供正确的代理信息。

---

### 第三步：查看结果

您可以通过以下两种方式查看结果：

#### 1. **电子邮件通知**：
   如果有符合您条件的新论文，您将收到一封包含论文标题、摘要和链接的电子邮件。

#### 2. **启动网页界面**：
   运行 `main.py` 后，`webpage.py` 脚本会自动启动一个简单的网页服务器来查看获取的论文。然后，打开浏览器访问：
   ```
   http://127.0.0.1:5000/
   ```
   该页面将显示与您指定的 `view_keywords` 相关的所有论文。点击“刷新”以更新结果，点击“链接”访问论文网站，点击“下载”下载 PDF，点击“本地链接”查看本地下载的 PDF。
   您还可以通过选择关键词复选框来筛选论文。

---

### 第四步：管理与输出

1. **数据库输出**：
   获取的论文信息存储在 `local/download.db` 目录下的 .db 文件中。请勿修改此文件。

2. **本地存储**：
   下载的论文存储在 `local/papers` 目录中，供将来参考。

---

## 常见问题

1. **如何指定多个类别或关键词？**
   - 您可以在命令行中使用空格分隔多个类别或关键词。例如：
     ```bash
     python main.py --category cs.CV cs.RO --keywords "deep learning" "radiance field"
     ```

2. **如何设置代理服务器？**
   - 如果您的网络环境需要代理，可以使用 `--proxy` 参数指定代理服务器地址和端口。例如：
     ```bash
     --proxy http://proxy.example.com:8080
     ```

3. **如何确保邮件通知发送成功？**
   - 确保您提供了正确的发送者电子邮件地址、密码和接收者电子邮件地址。如果问题仍然存在，请检查您的电子邮件设置，确保该账户允许通过应用程序发送电子邮件（例如，启用“允许不太安全的应用程序访问”）。

---

## 总结

如果您在使用此项目时遇到任何问题或有任何疑问，请随时提交问题或请求。希望您享受使用此工具的过程！
