from django.urls import path
from .views import SessionLoginView, SessionUserView

urlpatterns = [
    path("login/", SessionLoginView.as_view(), name="session_login"),
    path("user/", SessionUserView.as_view(), name="session_user"),
]
