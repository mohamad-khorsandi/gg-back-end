import json
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse


def send_otp_code(name, email, code):
    subject = 'کد تایید ثبت نام در GG'
    message = f'« Green Garden » \n 🪴رایحه گیاهان را در امتداد مسیرت استشمام کن🪴 \n کد تایید ثبت نام شما: {code}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(subject, message, email_from, recipient_list)


def req_to_dict(request):
    body_unicode = request.body.decode('utf-8')
    return json.loads(body_unicode)


class Response:
    def __init__(self):
        self.is_ok = None
        self.code = None

    @classmethod
    def bad_request(cls):
        obj = Response()
        obj.is_ok = False
        obj.code = 400
        return JsonResponse(obj.__dict__, safe=False)

    @classmethod
    def ok(cls):
        obj = Response()
        obj.is_ok = True
        obj.code = 200
        return JsonResponse(obj.__dict__, safe=False)

    @classmethod
    def unauthorized(cls):
        obj = Response()
        obj.is_ok = False
        obj.code = 401
        return JsonResponse(obj.__dict__, safe=False)

    @classmethod
    def not_found(cls):
        obj = Response()
        obj.is_ok = False
        obj.code = 404
        return JsonResponse(obj.__dict__, safe=False)

    @classmethod
    def ok_login(cls, token):
        obj = Response()
        obj.is_ok = True
        obj.code = 200
        obj.token = token
        return JsonResponse(obj.__dict__, safe=False)