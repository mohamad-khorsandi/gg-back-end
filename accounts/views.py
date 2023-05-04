from django.contrib.auth import login
from django.views import View
from .forms import UserRegistrationForm
import random
from utils import send_otp_code, Response, req_to_dict
from .models import TemporaryUser, User


class UserSignupView(View):
    form_class = UserRegistrationForm

    def post(self, request):
        form = self.form_class(req_to_dict(request))
        if not form.is_valid():
            return Response.bad_request()

        cd = form.cleaned_data
        random_code = random.randint(1000, 9999)
        print(random_code)
        send_otp_code(cd['name'], cd['email'], random_code)

        last_code = TemporaryUser.objects.filter(email=cd['email'])
        if last_code:
            last_code = last_code[0]
            last_code.code = random_code
            last_code.save()
        else:
            TemporaryUser.from_clean_data(cd, random_code).save()

        return Response.ok()


class UserVerifyCodeView(View):

    def post(self, request):
        code = int(req_to_dict(request)['code'])
        temp_user = TemporaryUser.objects.filter(code=code)

        if not len(temp_user) == 1:
            return Response.bad_request()

        main_user = temp_user[0].to_user()
        main_user.save()
        temp_user.delete()

        login(request, main_user)
        return Response.ok()


class UserLoginView(View):

    def post(self, request):
        data = req_to_dict(request)
        email = data['email']
        password = data['password']
        user = User.objects.filter(email=email, password=password)

        if not user:
            return Response.unauthorized()

        return Response.ok()
