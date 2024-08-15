# arXivFans

This project provides an effective way to fetch the latest papers from arXiv and view them through email notifications or a web interface. With simple configuration and command-line operations, you can easily stay updated with the latest research in your field.

## User Guide

This guide will help you understand how to use this project to fetch updates from arXiv, download them locally, and view the results through email notifications or a local web interface.

---

### Step 1: Installation and Configuration

1. **Clone the Repository**:
   First, clone the project code to your local machine.
   ```bash
   git clone <repository_url>
   cd arXivFans
   ```

2. **Install Dependencies**:
   Ensure you have Python >=3.8 installed on your system. Then, install the required Python packages:
   ```bash
   pip install .
   ```

---

### Step 2: Fetch arXiv Updates

You can fetch arXiv updates by running the `main.py` script from the command line. 

#### Quick Start
```bash
python main.py --category cs.CV cs.RO --keywords "keyword1" "keyword2"  
```
You can change cs.CV cs.RO "keyword1" "keyword2" as you want.

#### Full Args
```bash
python fetcharxiv/main.py --category cs.CV cs.RO --keywords "deep learning" "radiance field" --proxy http://proxy.example.com:8080 --email_sender your_email@example.com --email_password your_password --email_receiver recipient@example.com --frequency daily --smtp_server smtp.xxx.com --smtp_port 25orxxx --days 5 --download_mode 0/1/2 --view_keywords "keyword1" "keyword2" --local ".local"
```

#### Parameter Description:
##### Necessary

- **`--category`**: Specify the arXiv categories you want to search. For example, `cs.CV` (Computer Vision), `cs.RO` (Robotics).
- **`--keywords`**: Filter papers based on specified keywords. For example, "deep learning", "radiance field". Separate multiple keywords with spaces; they will be matched against the paper abstracts.

##### Optional
- **`--proxy`**: Specify a proxy server if required for network access.
- **`--email_sender`**: Email address for sending notifications.
- **`--email_password`**: SMTP password for the sender email.
- **`--email_receiver`**: Email address for receiving notifications.
- **`--frequency`**: Use "daily" to fetch updates daily at 8 AM. Otherwise, omit this parameter.
- **`--smtp_server`**: Specify your SMTP server address.
- **`--smtp_port`**: Specify your SMTP server port. This parameter is used to specify the port number of the SMTP server. By default, SMTP usually uses port 25, but if using encryption (like SSL or TLS), other ports (e.g., 465 or 587) may be used.
- **`--days`**: Specify the number of days to query results for (recommended <=7,default=3).
- **`--download_mode`**: Specify the download mode: 0 for no download, 1 for downloading accessed papers, 2 for downloading all papers(default=1).
- **`--view_keywords`**: the keywords you want the papers on webpage to be relevant to.
- **`--local`**: (absolute path)where you want your database and paper to be save(default=".local"). 
- Note that missing any of the parameters `email_sender`, `email_password`, `email_receiver`, `smtp_server`, or `smtp_port` will prevent email notifications from being sent.

#### Execution Result:

- The system will fetch the latest papers from the past few days that match the specified categories and keywords.
- Downloaded papers will be stored locally. If there are updates, an email notification will be sent to you.
- If using a proxy server, ensure you provide the correct proxy information.

---

### Step 3: View Results

You can view results in two ways:

#### 1. **Email Notifications**:
   If there are new papers that match your criteria, you will receive an email with the paper titles, abstracts, and links.

#### 2. **Start the Web Interface**:
   After running `main.py`, the `webpage.py` script will automatically start a simple web server to view the fetched papers. Then, open your browser and visit:
   ```
   http://127.0.0.1:5000/
   ```
   This page will display all papers that match your view_keywords. Click "refresh" to update the results, click "link" to visit the paper's website, click "download" to download PDF, and click "local link" to view the locally downloaded PDF.
   You can also filter the papers by selecting keywords checkboxes.


---

### Step 4: Management and Output

1. **Database Output**:
   The fetched paper information is stored in a .db file in the `local/download.db` directory. Please do not modify this file.

2. **Local Storage**:
   Downloaded papers are stored in the `local/papers` directory for future reference.

---

## FAQ

1. **How to specify multiple categories or keywords?**
   - You can separate multiple categories or keywords with spaces in the command line. For example:
     ```bash
     python main.py --category cs.CV cs.RO --keywords "deep learning" "radiance field"
     ```

2. **How to set up a proxy server?**
   - If your network environment requires a proxy, use the `--proxy` parameter to specify the proxy server address and port. For example:
     ```bash
     --proxy http://proxy.example.com:8080
     ```

3. **How to ensure email notifications are sent correctly?**
   - Make sure you provide the correct sender email address, password, and recipient email address. If problems persist, check your email settings to ensure the account allows sending emails through applications (e.g., enable "Allow less secure apps" access).

---

## Summary
If you encounter any issues or have any questions while using the project, feel free to submit an issue or pull request. Enjoy using this tool!