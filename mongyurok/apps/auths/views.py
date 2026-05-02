from django.shortcuts import render

def login_view(request):
    return render(request, 'auths/login.html')

def sign_view(request):
    return render(request, 'auths/sign.html')

# def sign_form_view(request):
#     return render(request, 'auths/signup.html')

def password_find(request):
    return render(request, "auths/find.html")

def password_reset(request):
    return render(request, "auths/password_reset.html")