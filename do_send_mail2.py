import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import threading

# 设置发件人、收件人的邮箱地址和密码
sender_email = "380517767@qq.com"
receiver_email = "penglee87@163.com"
password = "******"  # 注意是授权码而不是邮箱密码

# 创建邮件内容
message = MIMEText("这是一封测试邮件。", "plain", "utf-8")

# 发送者名称和邮箱地址
name = "你的名字"
sender = formataddr((name, sender_email))

# 接收者名称和邮箱地址
receiver_name = "接收者名字"
receiver = formataddr((receiver_name, receiver_email))

message['From'] = sender  # 发送者
message['To'] = receiver  # 接收者
message['Subject'] = Header("邮件标题", "utf-8")  # 邮件标题

def send_mail():
    try:
        smtp_server = smtplib.SMTP("smtp.qq.com", 587)  # 使用端口587
        smtp_server.starttls()
        smtp_server.login(sender_email, password)
        smtp_server.sendmail(sender_email, receiver_email, message.as_string())
        print("邮件发送成功")
        smtp_server.quit()
    except Exception as e:
        print("邮件发送失败")
        print(e)

# 创建一个线程来异步发送邮件
thread = threading.Thread(target=send_mail)
thread.start()  # 启动线程

print("邮件发送线程已启动，可以继续执行其他任务")
