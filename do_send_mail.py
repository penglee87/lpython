import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

# 设置发件人、收件人的邮箱地址和密码
sender_email = "380517767@qq.com"
receiver_email = "penglee87@163.com"
password = "******"  #注意是授权码而不是邮箱密码

# 创建邮件内容
message = MIMEText("这是一封测试邮件。", "plain", "utf-8")
message['From'] = formataddr((str(Header("你的名字", 'utf-8')), sender_email))  # 发送者
message['To'] = formataddr((str(Header("接收者名字", 'utf-8')), receiver_email))  # 接收者
message['Subject'] = Header("邮件标题", 'utf-8')  # 邮件标题

# 登录并发送邮件
try:
    smtp_server = smtplib.SMTP("smtp.qq.com", 587)  # 使用端口587
    smtp_server.starttls()
    smtp_server.login(sender_email, password)
    smtp_server.sendmail(sender_email, receiver_email, message.as_string())
    smtp_server.quit()
    print("邮件发送成功")
except Exception as e:
    print("邮件发送失败")
    print(e)
