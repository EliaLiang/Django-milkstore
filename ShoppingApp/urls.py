from django.urls import path
from django.conf import settings
from django.conf.urls import url, include
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from ShoppingApp import  views
from AppBase.views import UserInfoView,UserInfoDataView

urlpatterns = [
    url(r"^index$", views.IndexView.as_view(), name="shop_index"),  # 主页
    url(r"^goodslist$", views.GoodsListView.as_view(), name="shop_goodslist"),#主页商品列表
    url(r"^mygoods$", views.MyGoodsView.as_view(), name="shop_mygoods"),#我发布的商品
    url(r"^mygoodsdata$", views.MyGoodsDataView.as_view(), name="shop_mygoodsdata"),  # 我发布的商品
    url(r"^addgoods$", views.AddGoodsView.as_view(), name="shop_addgoods"),#发布商品
    url(r"^shoppingcar$", views.ShoppingCarView.as_view(), name="shop_shoppingcar"),#购物车
    url(r"^shoppingcardata$", views.ShoppingCarDataView.as_view(), name="shop_shoppingcardata"),  # 购物车数据
    url(r"^addshoppingcar$", views.AddGoodsToCar.as_view(), name="shop_addshoppingcar"),  # 加入购物车
    url(r"^createmybills$", views.CreateMyBillsView.as_view(), name="shop_createmybills"),  #直接下单
    url(r"^shoppingbilldetail$", views.ShoppingBillDetailView.as_view(), name="shop_shoppingbilldetail"),  # 订单详情
    url(r"^shoppingbilldetaildata$", views.ShoppingBillDetailDataView.as_view(), name="shop_shoppingbilldetaildata"),  # 订单数据详情
    url(r"^mybills$", views.MyBillsView.as_view(), name="shop_mybills"),  # 我的订单
    url(r"^mybillsdata$", views.MyBillsDataView.as_view(), name="shop_mybillsdata"),  # 我的订单数据
    url(r"^userinfo$", UserInfoView.as_view(), name="shop_userinfo"),#用户信息
    url(r"^userinfodata$", UserInfoDataView.as_view(), name="shop_userinfodata")

]
