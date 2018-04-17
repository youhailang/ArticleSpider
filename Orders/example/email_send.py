import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

my_sender = 'webmaster@play.cn'  # 发件人邮箱账号
my_pass = '###########'  # 发件人邮箱密码(当时申请smtp给的口令)
recv_user = '906669319@qq.com'  # 收件人邮箱账号，我这边发送给自己

def mail():
  res = True
  try:
    msg = MIMEText('填写邮件内容', 'plain', 'utf-8')
    msg['From'] = formataddr(["发件人昵称", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
    msg['To'] = formataddr(["收件人昵称", recv_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
    msg['Subject'] = "邮件主题-测试"  # 邮件的主题，也可以说是标题
    server = smtplib.SMTP("163.177.90.125", 25)  # 发件人邮箱中的SMTP服务器，端口是465
    server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
    server.sendmail(my_sender, [recv_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
    server.quit()  # 关闭连接
  except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的 res=False
    print(e)
    res = False
  return res

ret = mail()
if ret:
  print("邮件发送成功")
else:
  print("邮件发送失败")
