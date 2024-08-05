from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
from email.mime.multipart import MIMEMultipart

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def send_email(updates, from_addr, password, to_addr):
    subject = "Newest & Latest arXiv Updates"
    body = "\n".join([f"Title: {update['title']}\nKeyword: {update['keyword']}\nPublished: {update['published']}\nLink: {update['link']}\n" for update in updates])
    smtp_server = "smtp.163.com"

    msg = MIMEMultipart()
    msg['From'] = _format_addr('user <%s>' % from_addr)
    msg['To'] = _format_addr('user <%s>' % to_addr)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))


    
        
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()