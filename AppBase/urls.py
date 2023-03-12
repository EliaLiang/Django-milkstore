from django.urls import path
from django.conf import settings
from django.conf.urls import url, include
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from AppBase import  views
urlpatterns = [
    url(r"^index$", views.IndexView.as_view(), name="base_index"),  # 主页
    url(r"^register$", views.RegistAPIView.as_view(), name="api_register"),
    url(r"^login$", views.LoginAPIView.as_view(), name="api_login"),
    url(r"^findpassword$", views.FindPassword, name="api_findpassword"),
]
