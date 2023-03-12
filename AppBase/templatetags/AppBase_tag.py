from django import  template
from django.utils.safestring import mark_safe
from AppBase import models
from django.db.models import Q
from django.db.models import F
register=template.Library()

@register.filter   #过滤器 入参只能一个或没有
def multi(x,y):
    return x*y

@register.simple_tag() # 自定义标签 入参无限制  只能在 {% %} 中使用
def active_tag(index,serial_no):
    return "active" if index==serial_no else "noactive"


@register.inclusion_tag('myBlog/Inclusiontemplate/footerside.html')  #底部版权信息
def footersidetag():
    try:
        Myselfinfo = models.systemInfo.objects.get(name='footer_text')
    except models.systemInfo.DoesNotExist:
        Myselfinfo_memo="Copyright © 2020 LittleTortise. All rights reserved."
    else:
        Myselfinfo_memo = Myselfinfo.value

    return {'Myselfinfo_memo':Myselfinfo_memo}



@register.simple_tag() # 自定义标签 入参无限制  只能在 {% %} 中使用
def sitetitle_tag():
    #获取网站名称
    try:
        appNameSet = models.AppSettings.objects.get(Q(key="AppName"))
    except models.AppSettings.DoesNotExist:  # 可以捕获除与程序退出sys.exit()相关之外的所有异常
        return "XX网"
    return appNameSet.value