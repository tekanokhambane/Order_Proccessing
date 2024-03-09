from django.urls import path
from .views import SessionLoginView, BasicLoginView

urlpatterns = [
    path("login/session/", SessionLoginView.as_view(), name="session_login"),
    path("login/basic/", BasicLoginView.as_view(), name="basic_login"),
]
