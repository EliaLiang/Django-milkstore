from AppBase.base import  *
from django.utils.decorators import method_decorator
from ShoppingApp import  models
from AppBase.models import AppMenuDict
from django.core import serializers
from django.contrib.auth import authenticate, login,logout
# Create your views here.
from django.db.models import Max
from django.utils import timezone

def redictIndex(request):
    #The default page is the first item in the configuration
    defaulturl="/shop/index"
    return  redirect(defaulturl)
# index
@method_decorator(checkLogin, name='dispatch')
class IndexView(View):
    def get(self, request):
        print('request.user', request.user.username)
        print('request.user', request.user.id)
        # judge whether it is anonymous
        print('request.user', request.user.is_anonymous)
        username = request.user.username
        return render(request, "ShoppingApp/index.html",{"code": 200, "curUrl": "/ver/index"})
#product list
class GoodsListView(View):
    def get(self,request):
        #Get a list of product information
        searchName = request.GET.get("searchKey", "")
        dataList = models.GoodsRecord.objects.filter(Q(name__contains=searchName)&Q(delete_flag=0))
        data = []
        for item in dataList:
            data.append({"id": item.id, "name": item.name, "description": item.description,
                         "userName": item.creator.username,"goodsPic":item.pic.url,"price":str(item.price),"oldPrice":str(item.oldprice),
                         "userImage": item.creator.img.url, "createTime": timeConverStr(item.create_time)})

        return successResponseCommon(
            {"items": data, "pages": 1, "curpage": 1,
             "sumNum": len(dataList),
             "nodataflag": 1})

#add good
@method_decorator(checkLogin, name='dispatch')
class AddGoodsView(View):
    def get(self, request):
        print('request.user', request.user.username)
        print('request.user', request.user.id)
        # judge whether it is anonymous
        print('request.user', request.user.is_anonymous)
        username = request.user.username
        return render(request, "ShoppingApp/add_goods.html",{"code": 200})
    def post(self,request):
        #publish good
        name=request.POST.get("name","")
        price=request.POST.get("price",0)
        nums =int(request.POST.get("nums",0))
        description = request.POST.get("description", "")
        if request.FILES:
            pic = request.FILES.get('pic')
            goodRec=models.GoodsRecord(name=name,price=price,nums=nums,description=description,pic=pic,creator=request.user)
        else:
            goodRec = models.GoodsRecord(name=name, price=price, nums=nums, description=description,creator=request.user)
        goodRec.save()
        return successResponseCommon({}, "Success upload!")

#Products I posted
@method_decorator(checkLogin, name='dispatch')
class MyGoodsView(View):
    def get(self, request):
        return render(request, "ShoppingApp/my_goods.html", {"code": 200})


class MyGoodsDataView(View):
    def get(self, request):
        searchName = request.GET.get("searchKey", "")
        dataList = models.GoodsRecord.objects.filter(Q(creator=request.user)&Q(delete_flag=0)&Q(name__contains=searchName))
        data = []
        for item in dataList:
            data.append({"id": item.id, "name": item.name, "description": item.description,"nums": str(item.nums),
                         "userName": item.creator.username, "goodsPic": item.pic.url, "price": str(item.price),
                         "oldPrice": str(item.oldprice),
                         "userImage": item.creator.img.url, "createTime": timeConverStr(item.create_time)})

        return successResponseCommon(
            {"items": data, "pages": 1, "curpage": 1,
             "sumNum": len(dataList),
             "nodataflag": 1})
    def delete(self,request):
        data=json.loads(request.body)
        id=data.get('id',0)
        dataitem = models.GoodsRecord.objects.get(id=id)
        dataitem.delete_flag = 1
        dataitem.save()
        return successResponseCommon({},"Success delete！")
    def post(self,request):
        data = request.POST
        id = data.get('id', 0)
        name = data.get("name", "")
        price = data.get("price", 0)
        nums = int(data.get("nums", 0))
        description = data.get("description", "")
        dataitem = models.GoodsRecord.objects.get(id=id)
        dataitem.name=name
        if dataitem.price != price:
            dataitem.oldprice = dataitem.price
        dataitem.price = price
        dataitem.nums = nums
        dataitem.description = description
        if request.FILES:
            pic = request.FILES.get('pic')
            dataitem.pic=pic
        dataitem.save()
        return successResponseCommon({}, "Success edit！")



#Add item to cart
class AddGoodsToCar(View):
    def post(self,request):
        data = request.POST
        id = data.get('id', 0)
        #Query product information by id
        dataitem = models.GoodsRecord.objects.get(id=id)
        #Check whether the shopping cart has this item
        ShoppingCarList=models.ShoppingCar.objects.filter(Q(creator=request.user) & Q(goods=dataitem))
        if len(ShoppingCarList)>0:
            ShoppingCarList.update(nums=F('nums') + 1)
        else:
            models.ShoppingCar.objects.create(goods=dataitem,nums=1,creator=request.user)
        return successResponseCommon({}, "Add to cart！")



@method_decorator(checkLogin, name='dispatch')
#shopping cart
class ShoppingCarView(View):
    def get(self, request):
        return render(request, "ShoppingApp/shopping_cart.html", {"code": 200})
    def post(self,request):
        #Shopping cart generates an order
        data = request.POST
        items = data.get('items', "")
        items=items.split('|')
        #calculate
        costs= data.get('totalPrice',0)
        nums=data.get('totalNum',0)
        BillRecordMainrec=models.BillRecordMain.objects.create(costs=costs,nums=nums,creator=request.user)
        for item in items:
            if item!="":
                # Query shopping cart by id
                id=int(item)
                dataitem = models.ShoppingCar.objects.get(id=id)
                models.BillRecordSub.objects.create(main_rec=BillRecordMainrec,goods=dataitem.goods,nums=dataitem.nums,costs=dataitem.nums*dataitem.goods.price)
                dataitem.delete()
        return successResponseCommon({"id":BillRecordMainrec.id}, "Success create order!")

class ShoppingCarDataView(View):
    def get(self, request):
        #Query the current user's shopping cart information
        dataList = models.ShoppingCar.objects.filter( Q(creator=request.user) )
        data = []
        for item in dataList:
            data.append({"id": item.id, "pro_name": item.goods.name, "pro_description": item.goods.description, "pro_num": int(item.nums),
                          "pro_img": item.goods.pic.url, "pro_price": float(item.goods.price),
                         })
        return successResponseCommon(
            {"items": data, "pages": 1, "curpage": 1,
             "sumNum": len(dataList),
             "nodataflag": 1})
    def delete(self,request):
        data = json.loads(request.body.decode("utf-8"), encoding="utf-8")
        id = data.get('id', 0)
        dataitem = models.ShoppingCar.objects.get(id=id)
        dataitem.delete()
        return successResponseCommon({}, "Success delete！")
    def post(self,request): #increase decrease quantity
        data = request.POST
        id = data.get('id', 0)
        nums = data.get('nums', 0)
        dataitem = models.ShoppingCar.objects.get(id=id)
        dataitem.nums=nums
        dataitem.save()
        return successResponseCommon({}, "Success edit！")


class ShoppingBillDetailView(View):
    def get(self,request):
        id= request.GET.get("id", 0)
        BillRecordMainrec = models.BillRecordMain.objects.get(id=id)
        return render(request, "ShoppingApp/bill_detail.html", {"billId": id,"bill_status":BillRecordMainrec.bill_status})


class ShoppingBillDetailDataView(View):
    def get(self, request):
        id = request.GET.get("id", 0)
        BillRecordMainrec = models.BillRecordMain.objects.get(id=id)
        #Get order details data
        dataList = models.BillRecordSub.objects.filter(Q(main_rec=BillRecordMainrec))
        data = []
        for item in dataList:
            data.append({"id": item.id, "pro_name": item.goods.name, "pro_description": item.goods.description,
                         "pro_num": int(item.nums),
                         "pro_img": item.goods.pic.url, "pro_price": float(item.goods.price),
                         })
        return successResponseCommon(
            {"items": data, "pages": 1, "curpage": 1,
             "sumNum": len(dataList),
             "nodataflag": 1})
    def post(self,request): #pay
        data = request.POST
        id = data.get('id', 0)
        dataitem = models.BillRecordMain.objects.get(id=id)
        dataitem.bill_status="已支付"
        dataitem.save()
        return successResponseCommon({}, "Success edit！")


class MyBillsView(View):
    def get(self, request):
        return render(request, "ShoppingApp/my_bills.html", {"code": 200})


class MyBillsDataView(View):
    def get(self, request):
        searchName = request.GET.get("searchKey", "")
        dataList = models.BillRecordMain.objects.filter(Q(creator=request.user))
        data = []
        for item in dataList:
            data.append({"id": item.id,  "nums": str(item.nums),
                         "price": str(item.costs),
                         "bill_status": str(item.bill_status),
                          "createTime": timeConverStr(item.create_time)})

        return successResponseCommon(
            {"items": data, "pages": 1, "curpage": 1,
             "sumNum": len(dataList),
             "nodataflag": 1})

    def delete(self, request):
        data = json.loads(request.body)
        id = data.get('id', 0)
        dataitem = models.BillRecordMain.objects.get(id=id)
        dataitem.delete()
        return successResponseCommon({}, "Success delete！")


class CreateMyBillsView(View):
    def post(self,request):
        #Shopping cart generates an order
        data = request.POST
        id = data.get('id', "")
        #Query products
        goodsitem=models.GoodsRecord.objects.get(id=id)
        #calculate
        costs= goodsitem.price
        nums=1
        BillRecordMainrec=models.BillRecordMain.objects.create(costs=costs,nums=nums,creator=request.user)
        models.BillRecordSub.objects.create(main_rec=BillRecordMainrec,goods=goodsitem,nums=nums,costs=costs)
        return successResponseCommon({"id":BillRecordMainrec.id}, "Success create order!")