import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

subject_message = 'Временные технические неполадки на нашем сайте'


def get_body_message(error):
    return f"""Уважаемый Иван Иванов, \n
            Спасибо, что вы являетесь верным пользователем нашей платформы. Мы ценим ваше доверие и стремимся предоставить вам лучший опыт использования нашего сайта. \n
            Мы хотим проинформировать вас о том, что мы обнаружили некоторые технические проблемы на нашем сайте и, \n
            возможно, вы могли столкнуться с "{error}". Наши IT специалисты уже активно работают над их решением. \n
            Мы извиняемся за любые неудобства и благодарим вас за терпение. Мы обещаем максимально быстро устранить все проблемы и восстановить нормальную работу сайта. \n
            Если у вас есть какие-либо вопросы или возникли проблемы, связанные с этим, пожалуйста, \n
            не стесняйтесь обращаться в службу поддержки, и мы сделаем все возможное, чтобы помочь вам. \n
            С уважением, \n
            Портал Поставщиков"""


subject_message_resolved = 'Техническая проблема на нашем сайте устранена'
body_message_resolved = f"""Уважаемый Иван Иванов,
                        Мы рады сообщить вам, что техническая проблема на нашем сайте, о которой мы уведомляли ранее, была успешно устранена нашей командой специалистов.
                        Вы можете продолжить пользоваться всеми функциями нашего веб-сайта в обычном режиме. 
                        Мы приносим извинения за любые неудобства, которые могли быть вызваны этой неполадкой.
                        Наша команда делает все возможное, чтобы предотвратить подобные инциденты в будущем. 
                        Однако если вы обнаружите какие-либо проблемы или нештатные ситуации, просим сообщить нам об этом.
                        Ваше мнение очень важно для нас, и мы всегда готовы помочь вам. 
                        Если у вас есть вопросы или волнения, связанные с нашей платформой, пожалуйста, не стесняйтесь обращаться в нашу службу поддержки.
                        Спасибо за ваше терпение и понимание.
                        С уважением,
                        Портал Поставщиков"""


class YandexMailSender:
    def __init__(self, config: dict) -> None:
        self.smtp_username: str = config["mail"]["username"]
        self.smtp_password: str = config["mail"]["password"]
        self.smtp_server: str = 'smtp.yandex.ru'
        self.smtp_port: int = 587
        self.smtp_connection: smtplib.SMTP

    def connect(self) -> None:
        self.smtp_connection = smtplib.SMTP(self.smtp_server, self.smtp_port)
        self.smtp_connection.ehlo()
        self.smtp_connection.starttls()
        self.smtp_connection.login(self.smtp_username, self.smtp_password)

    def disconnect(self) -> None:
        self.smtp_connection.quit()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    def send_mail(self, recipient: str, subject: str, body: str, attachment: Optional[str] = None) -> None:
        msg: MIMEMultipart = MIMEMultipart()
        msg['From'] = self.smtp_username
        msg['To'] = recipient
        msg['Subject'] = subject

        # Добавление текстового содержимого
        msg.attach(MIMEText(body, 'plain'))

        if attachment:
            # Добавление вложения
            filename: str = attachment
            attachment: MIMEBase = MIMEBase('application', 'octet-stream')
            attachment.set_payload(open(filename, 'rb').read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', 'attachment', filename=filename)
            msg.attach(attachment)

        self.smtp_connection.sendmail(msg['From'], msg['To'], msg.as_string())

# if __name__ == '__main__':
#     config = {
#         'mail': {
#             'username': 'hack-mts@yandex.ru',
#             'password': 'zlhtgwnbzcwvcery'
#         }
#     }

#     recipient_email = 'hack-mts@yandex.ru'
#     recipient_name = 'Бабон Абабуев Бомбастиков'

#     error = 'SQL fucked up'
#     subject_error = 'Временные технические неполадки на нашем сайте'
#     body_error = f"""Уважаемый {recipient_name}, \n
#             Спасибо, что вы являетесь верным пользователем нашей платформы. Мы ценим ваше доверие и стремимся предоставить вам лучший опыт использования нашего сайта. \n
#             Мы хотим проинформировать вас о том, что мы обнаружили некоторые технические проблемы на нашем сайте и, \n
#             возможно, вы могли столкнуться с {error}. Наши IT специалисты уже активно работают над их решением. \n
#             Мы извиняемся за любые неудобства и благодарим вас за терпение. Мы обещаем максимально быстро устранить все проблемы и восстановить нормальную работу сайта. \n
#             Если у вас есть какие-либо вопросы или возникли проблемы, связанные с этим, пожалуйста, \n
#             не стесняйтесь обращаться в службу поддержки, и мы сделаем все возможное, чтобы помочь вам. \n
#             С уважением, \n
#             Портал Поставщиков"""

#     subject_resolved = 'Техническая проблема на нашем сайте устранена'
#     body_resolved = f"""Уважаемый {recipient_name},
#                         Мы рады сообщить вам, что техническая проблема на нашем сайте, о которой мы уведомляли ранее, была успешно устранена нашей командой специалистов.
#                         Вы можете продолжить пользоваться всеми функциями нашего веб-сайта в обычном режиме.
#                         Мы приносим извинения за любые неудобства, которые могли быть вызваны этой неполадкой.
#                         Наша команда делает все возможное, чтобы предотвратить подобные инциденты в будущем.
#                         Однако если вы обнаружите какие-либо проблемы или нештатные ситуации, просим сообщить нам об этом.
#                         Ваше мнение очень важно для нас, и мы всегда готовы помочь вам.
#                         Если у вас есть вопросы или волнения, связанные с нашей платформой, пожалуйста, не стесняйтесь обращаться в нашу службу поддержки.
#                         Спасибо за ваше терпение и понимание.
#                         С уважением,
#                         Портал Поставщиков"""

#     with YandexMailSender(config=config) as sender:
#         sender.send_mail(
#             recipient=recipient_email,
#             subject=subject_error,
#             body=body_error,
#     )
