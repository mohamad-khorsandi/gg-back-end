import json

from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse


# todo utils should move to apps

def send_otp_code(name, email, code):
    subject = 'کد تایید ثبت نام در GG'
    message = f'« Green Garden » \n 🪴رایحه گیاهان را در امتداد مسیرت استشمام کن🪴 \n کد تایید ثبت نام شما: {code}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(subject, message, email_from, recipient_list)


def req_to_dict(request):
    body_unicode = request.body.decode('utf-8')
    return json.loads(body_unicode)

