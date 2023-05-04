from django.shortcuts import render, redirect
from django.views import View


class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'home/home.html')
        else:
            return redirect('accounts:user_register')
