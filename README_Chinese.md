# arXivFans

该项目为获取arXiv最新论文并通过电子邮件通知或网页界面进行查看提供了一种有效的方法。通过简单的配置和命令行操作，您可以轻松获取自己领域的最新研究动态。

## 用户指南

本指南将帮助您了解如何使用此项目从arXiv获取更新，将其下载到本地，并通过电子邮件通知或本地网页界面查看结果。

---

### 步骤 1：安装和配置

1. **克隆仓库**：
   首先，将项目代码克隆到您的本地机器上。
   ```bash
   git clone <repository_url>
   cd arXivFans
   ```

2. **安装依赖**：
   确保您的系统上安装了Python >=3.8。然后，安装所需的Python包：
   ```bash
   pip install .
   ```

---

### 步骤 2：获取arXiv更新

您可以通过命令行运行`main.py`脚本来获取arXiv的更新。

#### 快速开始
```bash
python main.py --category cs.CV cs.RO --keywords "keyword1" "keyword2"  
```
您可以根据需要更改cs.CV cs.RO "keyword1" "keyword2"。

#### 全部参数
```bash
python fetcharxiv/main.py --category cs.CV cs.RO --keywords "deep learning" "radiance field" --proxy http://proxy.example.com:8080 --email_sender your_email@example.com --email_password your_password --email_receiver recipient@example.com --frequency daily --smtp_server smtp.xxx.com --smtp_port 25orxxx --days 5 --download_mode 0/1/2 --view_keywords "keyword1" "keyword2" --local ".local"
```

#### 参数说明：
##### 必要参数

- **`--category`**：指定您想要搜索的arXiv分类。例如，`cs.CV`（计算机视觉），`cs.RO`（机器人学）。
- **`--keywords`**：根据指定的关键词过滤论文。例如，“deep learning”，“radiance field”。多个关键词用空格分隔，它们将与论文摘要进行匹配。

##### 可选参数
- **`--proxy`**：如果需要网络访问，请指定代理服务器。
- **`--email_sender`**：用于发送通知的电子邮件地址。
- **`--email_password`**：发送电子邮件的SMTP密码。
- **`--email_receiver`**：接收通知的电子邮件地址。
- **`--frequency`**：使用“daily”每天早上8点获取更新。否则，省略此参数。
- **`--smtp_server`**：指定您的SMTP服务器地址。
- **`--smtp_port`**：指定您的SMTP服务器端口。此参数用于指定SMTP服务器的端口号。默认情况下，SMTP通常使用端口25，但如果使用加密（如SSL或TLS），则可能使用其他端口（如465或587）。
- **`--days`**：指定查询结果的天数（建议<=7，默认=3）。
- **`--download_mode`**：指定下载模式：0表示不下载，1表示下载访问过的论文，2表示下载所有论文（默认=1）。
- **`--view_keywords`**：您希望在网页上显示与这些关键词相关的论文。
- **`--local`**：（绝对路径）指定数据库和论文的保存位置（默认=".local"）。
- 请注意，如果缺少`email_sender`、`email_password`、`email_receiver`、`smtp_server`或`smtp_port`中的任何参数，将无法发送电子邮件通知。

#### 执行结果：

- 系统将从过去几天中获取符合指定分类和关键词的最新论文。
- 下载的论文将保存在本地。如果有更新，您将收到电子邮件通知。
- 如果使用代理服务器，请确保提供正确的代理信息。

---

### 步骤 3：查看结果

您可以通过两种方式查看结果：

#### 1. **电子邮件通知**：
   如果有符合您条件的新论文，您将收到包含论文标题、摘要和链接的电子邮件。

#### 2. **启动网页界面**：
   运行`main.py`后，`webpage.py`脚本会自动启动一个简单的网页服务器以查看获取的论文。然后，打开浏览器并访问：
   ```
   http://127.0.0.1:5000/
   ```
   该页面将显示所有符合您`view_keywords`的论文。点击“refresh”以更新结果，点击“link”访问论文网站，点击“download”下载PDF，点击“local link”查看本地下载的PDF。
   您还可以通过选择关键词复选框来过滤论文。

---

### 步骤 4：管理和输出

1. **数据库输出**：
   获取的论文信息存储在`local/download.db`目录中的`.db`文件中。请勿修改此文件。

2. **本地存储**：
   下载的论文存储在`local/papers`目录中，供日后参考。

---

## 常见问题

1. **如何指定多个类别或关键词？**
   - 您可以在命令行中用空格分隔多个类别或关键词。例如：
     ```bash
     python main.py --category cs.CV cs.RO --keywords "deep learning" "radiance field"
     ```

2. **如何设置代理服务器？**
   - 如果您的网络环境需要代理，请使用`--proxy`参数指定代理服务器地址和端口。例如：
     ```bash
     --proxy http://proxy.example.com:8080
     ```

3. **如何确保正确发送电子邮件通知？**
   - 确保您提供了正确的发件人电子邮件地址、密码和收件人电子邮件地址。如果问题仍然存在，请检查您的电子邮件设置，以确保帐户允许通过应用程序发送电子邮件（例如，启用“允许不太安全的应用”访问）。

---

## 总结
如果在使用项目过程中遇到任何问题或有任何疑问，请随时提交问题或请求合并。希望您享受使用此工具的过程！
