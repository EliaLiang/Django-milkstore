from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
import smtplib
from AppBase import models


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def SendEmail(mailTo,title,mailContent):
    try:
        # get sender information
        fromUserInfos = models.EmailSendFromDefaultSettings.objects.all()
        if len(fromUserInfos) <= 0:
            return "The user's information is empty"
        defaultFromUserInfo = fromUserInfos[0]
        password = defaultFromUserInfo.userPassword
        from_addr = defaultFromUserInfo.formUser

        # get email information

        smtp_server = defaultFromUserInfo.smtpServer
        to_addr = mailTo
        msg = MIMEMultipart()
        msgText = MIMEText(mailContent, 'html', 'utf-8')
        msg.attach(msgText)
        msg['From'] = _format_addr('%s <%s>' % (defaultFromUserInfo.userShowName, defaultFromUserInfo.formUser))
        msg['To'] = mailTo
        msg['Subject'] = Header(title, 'utf-8').encode()
        # # attact files
        # filepath = emailRecordInfo.mailAttchment.path
        # filename = emailRecordInfo.mailAttchment.name
        #
        # attach = MIMEText(open(filepath, 'rb').read(), 'base64', 'utf-8')
        # attach["Content-Type"] = 'application/octet-stream'
        # attach["Content-Disposition"] = 'attachment; filename=' + filename
        # msg.attach(attach)

        # send email
        server = smtplib.SMTP(smtp_server, 25)
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
        return "success"
    except Exception as e:
        return str(e)


