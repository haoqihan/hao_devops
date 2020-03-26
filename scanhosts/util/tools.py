from django.core.mail import send_mail
import time


class Sendmail:
    """
    发送邮件
    """
    def __init__(self, receive_addr, sub_info, content_info):
        sub_date = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
        self.receive_addr = receive_addr
        self.sub_info = sub_info + sub_date
        self.content_info = content_info

    def send(self):
        try:
            send_mail(
                subject=self.sub_info,
                message=self.content_info,
                from_email="18233027057@163.com",
                recipient_list=self.receive_addr,
                fail_silently=False)
            return True
        except Exception as e:
            print(e)
            return False
