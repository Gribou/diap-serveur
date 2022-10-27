from django.urls import path

from .views import LoginView, LoginCompleteView, LogoutView

app_name = "sso"
urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('login/callback/', LoginCompleteView.as_view(), name="login-complete"),
    path('logout/', LogoutView.as_view(), name="logout")
]
