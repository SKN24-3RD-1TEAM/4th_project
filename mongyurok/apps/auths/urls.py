from django.urls import path
from . import views

app_name = 'auths'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('sign/', views.sign_view, name='sign'),
    # path('sign/sign-form/', views.signup_view, name='sign-form'),
    path('find/', views.password_find, name='find'),
    path("find/reset/", views.password_reset, name="password_reset"),
]