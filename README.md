# arXivFans

## User Guide

This guide will help you step by step to understand how to use this project to fetch updates from arXiv, download them locally, and view the results either via email notifications or a local web interface.

---

### Step 1: Installation and Configuration

1. **Clone the Repository**:
   First, you need to clone the project code to your local computer.
   ```bash
   git clone <repository_url>
   cd fetch
   ```

2. **Install Dependencies**:
   Ensure that your system has Python 3 installed. Then, install the required Python packages for the project:
   ```bash
   pip install -r requirements.txt
   ```

---

### Step 2: Fetching arXiv Updates

You can fetch arXiv updates by running the `main.py` script from the command line. Below is an example command:

```bash
python main.py --category cs.CV cs.RO --keywords "deep learning" "radiance field" --proxy proxy.example.com:8080 --email_sender your_email@example.com --email_password your_password --email_receiver recipient@example.com
```

#### Parameter Explanation:

- **`--category`**: Specifies the arXiv categories you want to search. For example, `cs.CV` (Computer Vision), `cs.RO` (Robotics).
- **`--keywords`**: Filters the papers based on specified keywords. For example, "deep learning", "radiance field".
- **`--proxy`**: (Optional) Specify a proxy server for network access if needed.
- **`--email_sender`**: The email address from which notifications will be sent.
- **`--email_password`**: The SMTP password for the sending email **SMTP**.
- **`--email_receiver`**: The email address where notifications will be received.

#### Execution Results:

- The system will fetch the latest papers from arXiv that match the specified categories and keywords.
- The downloaded papers will be stored locally, and an email notification will be sent to you if there are updates.
- If you use a proxy server, ensure that you provide the correct proxy information.

---

### Step 3: Viewing the Results

You can view the results in two ways:

#### 1. **Email Notifications**:
   If there are new papers that match your criteria, you will receive an email containing the titles, abstracts, and links to the papers.

#### 2. **Starting the Web Interface**:
   After running `main.py`, the `webpage.py` script will automatically start a simple web server to conveniently view the papers fetched that day. 
   Then, open your browser and visit the following address:
   ```
   http://127.0.0.1:5000/
   ```
   This page will display all the papers that match your criteria. If there are no updates, the page will prompt you to fetch updates first.

   You can also run `webpage.py` again to view the results multiple times:
   ```bash
   python webpage.py
   ```

---

### Step 4: Management and Output

1. **JSON Output**:
   The fetched paper information is stored in JSON files in the `output` directory, making it easy to access and manage later.

2. **Local Storage**:
   The downloaded papers are stored locally in the `./fetch/paper` directory, organized by category and keywords for future reference.

---

## Frequently Asked Questions

1. **How to specify multiple categories or keywords?**
   - You can specify multiple categories or keywords by separating them with spaces in the command line. For example:
     ```bash
     python main.py --category cs.CV cs.RO --keywords "deep learning" "radiance field"
     ```

2. **How to set up a proxy server?**
   - If your network environment requires a proxy, you can specify the proxy server address and port using the `--proxy` parameter. For example:
     ```bash
     --proxy proxy.example.com:8080
     ```

3. **How to ensure email notifications are sent correctly?**
   - Make sure you provide the correct sender email address, password, and recipient email address. If issues persist, check your email settings to ensure the account allows sending emails via applications (e.g., enabling "Allow less secure apps" access).

---

## Summary

This project provides an efficient way to fetch the latest papers from arXiv, with options to view them via email notifications or a web interface. With simple configuration and command-line operations, you can easily stay updated on the latest research in your field.

If you have any questions or encounter issues while using the project, feel free to submit an issue or pull request. Enjoy using the tool!
