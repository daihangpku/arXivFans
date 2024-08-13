from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
from email.mime.multipart import MIMEMultipart

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def send_email(updates, from_addr, password, to_addr, smtp_server, smtp_port):
    subject = "Newest & Latest arXiv Updates"
    body = "\n".join([f"Title: {update['title']}\nKeyword: {update['keyword']}\nPublished: {update['published']}\nLink: {update['link']}\n" for update in updates])

    msg = MIMEMultipart()
    msg['From'] = _format_addr('ArXivFans <%s>' % from_addr)
    msg['To'] = _format_addr('Dear user <%s>' % to_addr)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        #server.starttls()
        server.login(from_addr, password)

        server.sendmail(from_addr, [to_addr], msg.as_string())
        print("message sent successfully")
        server.quit()
    except smtplib.SMTPAuthenticationError as e:
        print("incorrect password")
        print("fail to send the email")
    except Exception as e:
        print(f"error: {e}")
