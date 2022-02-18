import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from decouple import config

class Gmail:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.stmp_server = 'smtp.gmail.com'
        self.stmp_port = 587
        self.stmp_user = config('MAIL_USER')
        self.stmp_password = config('MAIL_PASSWORD')


    def send(self, to_address: str):
        from_address = self.stmp_user
        subject = 'ランキング入り証明スクリーンショットを送付いたします。'
        body = """
            <html>
                <body>
                    <p>ランキングのスクリーンショットです。</p>
                    <p>ご確認お願いいたします。</p>
                </body>
            </html>
        """

        filepath = f"image/{self.file_name}"
        filename = os.path.basename(filepath)

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = from_address
        msg['To'] = ','.join(to_address)
        msg.attach(MIMEText(body, 'html'))

        with open(filepath, 'rb') as f:
            mb = MIMEApplication(f.read())

        mb.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(mb)

        s = smtplib.SMTP(self.stmp_server, self.stmp_port)
        s.starttls()
        s.login(self.stmp_user, self.stmp_password)
        s.sendmail(from_address, to_address, msg.as_string())
        s.quit()

        print("メールを送信しました。")