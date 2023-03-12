"""DemoSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls import url,include
from django.conf.urls.static import static
from DemoSite import  views
from AppBase.views import  LoginView,RegistView,LogoutView,ProfileView
from ShoppingApp.views import redictIndex


urlpatterns = [
    url(r"^admin", admin.site.urls),
    url(r"^$", redictIndex),  # 默认重定向到主页
    url(r"^login", LoginView.as_view(),name="login"),
    url(r"^registe", RegistView.as_view(),name="registe"),
    url(r"^logout", LogoutView.as_view(), name="logout"),
    url(r"^profile", ProfileView.as_view(), name="profile"),
    url(r"^index", redictIndex,name="index"),
    url(r"^api/", include('AppBase.urls')),  # 将以base/开头的路由分发到 AppBase.urls文件  进行第二次分发
    url(r"^shop/", include('ShoppingApp.urls')),
    url(r"^(?!media)", views.error404, name="error404"),  # 排除图片资源 其他未定义转到404错误页面  (django自带404错误调试模式不能用)
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
