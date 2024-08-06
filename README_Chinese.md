# arXivFans

## 用户指南

本指南将逐步帮助您了解如何使用此项目从arXiv获取更新，将其下载到本地，并通过电子邮件通知或本地Web界面查看结果。

---

### 步骤1：安装和配置

1. **克隆仓库**：
   首先，您需要将项目代码克隆到本地计算机。
   ```bash
   git clone <repository_url>
   cd fetch
   ```

2. **安装依赖项**：
   确保您的系统已安装Python >=3.8。然后，安装项目所需的Python包：
   ```bash
   pip install -r requirements.txt
   ```

---

### 步骤2：获取arXiv更新

您可以通过在命令行运行`main.py`脚本来获取arXiv更新。以下是示例命令：

```bash
python main.py --category cs.CV cs.RO --keywords "deep learning" "radiance field" --proxy proxy.example.com:8080 --email_sender your_email@example.com --email_password your_password --email_receiver recipient@example.com --frequency daily --smtp_server smtp.xxx.com --smtp_port 25orxxx
```

#### 参数说明：

- **`--category`**：指定您要搜索的arXiv分类。例如，`cs.CV`（计算机视觉），`cs.RO`（机器人学）。
- **`--keywords`**：根据指定的关键词过滤论文。例如，“deep learning”，“radiance field”。
- **`--proxy`**：（可选）如果需要网络访问代理，请指定代理服务器。
- **`--email_sender`**：发送通知的电子邮件地址。
- **`--email_password`**：发送电子邮件的SMTP密码。
- **`--email_receiver`**：接收通知的电子邮件地址。
- **`--frequency`**：如果希望每日更新，则使用“daily”。否则，忽略此参数。
- **`--smtp_server`**：指定您的 SMTP 服务器地址。
- **`--smtp_port`**：指定您的 SMTP 服务器端口。这个参数用于指定 SMTP 服务器的端口号。默认情况下，SMTP 通常使用端口 25，但如果使用加密（如 SSL 或 TLS），可能会使用其他端口（例如 465 或 587）。

#### 执行结果：

- 系统将获取过去7天内符合指定分类和关键词的最新论文。
- 下载的论文将存储在本地，如果有更新，将向您发送电子邮件通知。
- 如果使用代理服务器，请确保提供正确的代理信息。

---

### 步骤3：查看结果

您可以通过两种方式查看结果：

#### 1. **电子邮件通知**：
   如果有符合您条件的新论文，您将收到包含论文标题、摘要和链接的电子邮件。

#### 2. **启动Web界面**：
   运行`main.py`后，`webpage.py`脚本会自动启动一个简单的Web服务器，以便查看当天获取的论文。然后，打开浏览器并访问以下地址：
   ```
   http://127.0.0.1:5000/
   ```
   此页面将显示所有符合您条件的论文。如果没有更新，页面会提示您先获取更新。

   您还可以多次运行`webpage.py`查看结果：
   ```bash
   python webpage.py
   ```

---

### 步骤4：管理和输出

1. **JSON输出**：
   获取的论文信息存储在`./fetch/output`目录中的JSON文件中，方便以后访问和管理。

2. **本地存储**：
   下载的论文存储在`./fetch/paper`目录中，按类别和关键词组织，便于日后参考。

---

## 常见问题

1. **如何指定多个类别或关键词？**
   - 您可以在命令行中用空格分隔多个类别或关键词。例如：
     ```bash
     python main.py --category cs.CV cs.RO --keywords "deep learning" "radiance field"
     ```

2. **如何设置代理服务器？**
   - 如果您的网络环境需要代理，可以使用`--proxy`参数指定代理服务器地址和端口。例如：
     ```bash
     --proxy proxy.example.com:8080
     ```

3. **如何确保电子邮件通知正确发送？**
   - 请确保您提供了正确的发送者电子邮件地址、密码和接收者电子邮件地址。如果问题仍然存在，请检查您的电子邮件设置以确保账户允许通过应用程序发送电子邮件（例如，启用“允许不太安全的应用程序”访问）。

---

## 总结

该项目提供了一种有效的方式从arXiv获取最新论文，并通过电子邮件通知或Web界面查看。通过简单的配置和命令行操作，您可以轻松掌握您领域的最新研究动态。

如果您在使用项目时有任何问题或遇到问题，请随时提交问题或拉取请求。希望您喜欢使用这个工具！
