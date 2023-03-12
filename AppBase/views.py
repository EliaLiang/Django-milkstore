from AppBase.base import  *
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login,logout
import  random
from AppBase.sendEmail import *
# Create your views here.

# index
@method_decorator(checkLogin, name='dispatch')
class IndexView(View):
    def get(self, request):
        print('request.user', request.user.username)
        print('request.user', request.user.id)
        # check whether the anonymous
        print('request.user', request.user.is_anonymous)
        username = request.user.username
        return render(request, "error.html",
                      {"code": 200, "message": username})


#login
class LoginView(View):
    def get(self,request):
        return render(request, "login.html", {"index": 99})
    def post(self,request):
        username = request.POST.get('username',"")
        # check whether username and pwd are legal
        password = request.POST.get('password',"")
        # check data
        if not all([username, password]):
            return render(request, "error.html",{"code":500,"message":"username or password is empty"})
        #Query username according to the input username (it can be email, mobile phone number, and username, all of which are unique values)
        try:
            user = models.UserDict.objects.get(Q(phone=username) | Q(email=username) | Q(username=username))
        except models.UserDict.DoesNotExist:  
            # catch all exceptions except those related to program exit sys.exit()
            return render(request, "error.html",{"code":500,"message":"user doesn't exist"})
        #verify password
        user = authenticate(username=user.username, password=password)  # verify user
        if user:
            login(request, user)  # login
            request.session['username'] = username
            return redirect('/index')
        return render(request, "error.html",{"code":500,"message":"wrong password"})

#log out
class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect("/login")


#signup
class RegistView(View):
    def post(self,request):
        username = request.POST.get('username',"")
        useremail = request.POST.get('email')
        password = request.POST.get('password')
        role= request.POST.get('role')
        if username=="":
            username=useremail
        if not all([useremail, password]):
            return render(request, "error.html",{"code":500,"message":"No username or password entered"})
        # check whether username already exist
        users = models.UserDict.objects.filter(Q(username=username) | Q(email=useremail))
        if len(users) <= 0:
            user=models.UserDict.objects.create_user(username=username, email=useremail, phone=username, password=password,role=role)
            login(request, user)  # login
            return redirect("/index")
        else:
            return render(request, "error.html",{"code":500,"message":"Email address has been registered"})


class RegistAPIView(View):
    def post(self,request):
        username = request.POST.get('name',"")
        useremail = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        if username=="":
            username=useremail
        if not all([useremail, password]):
            return errorResponseCommon({},"No username or password entered")
        # check repeat username
        users = models.UserDict.objects.filter(Q(username=username) | Q(email=useremail))
        if len(users) <= 0:
            # send signup email
            res ="success" ###SendEmail(useremail, "word")
            if res == "success":
                # random photo
                iocnList = models.AppDefaultIocn.objects.all()
                if len(iocnList) > 0:
                    iocnIndex = random.randint(0, len(iocnList)-1)
                    user = models.UserDict.objects.create_user(username=username, email=useremail, phone="",role=role,
                                                               password=password, img=iocnList[iocnIndex].img)
                else:
                    user = models.UserDict.objects.create_user(username=username, email=useremail, phone="",role=role,
                                                               password=password)
                login(request, user)  # login
                return successResponseCommon({"url": "/shop/index"}, "success signup")
            else:
                return errorResponseCommon({}, "email verify lose")



        else:
            #Precisely what has been registered
            if len(models.UserDict.objects.filter(Q(username=username)))>0:
                return errorResponseCommon({}, "User name has been registered")
            return errorResponseCommon({},"Email has been registered")

class LoginAPIView(View):
    def post(self,request):
        username = request.POST.get('username',"")
        # Determine whether the user name and password are valid users
        password = request.POST.get('password',"")
        # Data verification
        if not all([username, password]):
            return errorResponseCommon({},"No username or password entered")
        #Query username according to the input username (it can be email, mobile phone number, and username, all of which are unique values)
        try:
            user = models.UserDict.objects.get(Q(phone=username) | Q(email=username) | Q(username=username))
        except models.UserDict.DoesNotExist:  
            return errorResponseCommon({},"User doesn't exist")
        #verify password
        user = authenticate(username=user.username, password=password)  # verify user
        if user:
            login(request, user)  # login
            request.session['username'] = username
            return successResponseCommon({"url":"/index"},"success login")
        return errorResponseCommon({},"wrong password")

def FindPassword(request):
    #find password back
    email=request.GET.get('email',"")
    try:
        u = models.UserDict.objects.get(email=email)
    except models.UserDict.DoesNotExist:  # catch exception
        return errorResponseCommon({}, "Email not registered")
    code = "".join([str(random.randint(0, 9)) for _ in range(6)])
    u.set_password(code)
    u.save()
    res = SendEmail(email, "Recover password", "Your login password has been reset to:"+code)
    if res == "success":
        return successResponseCommon({},"The login password has been sent to your email, please check it!")
    else:
        return errorResponseCommon({},"Failed to retrieve password, contact me")


class ProfileView(View):
    def get(self, request):
        return render(request, "VersionApp/profile.html", {"index": 99})


@method_decorator(checkLogin, name='dispatch')
class UserInfoView(View):
    def get(self, request):
        id = request.GET.get("id", 0)
        if id==0:
            id=request.user.id
        return render(request, "ShoppingApp/user_info.html", {"id": id})

class UserInfoDataView(View):
    def get(self, request):
        id = request.GET.get("id", 0)
        user=UserDict.objects.get(id=id)
        data={"id":user.id,"username":user.username,"email":user.email,"phone":user.phone,"img":user.img.url}
        return successResponseCommon(
            {"items": data, "pages": 1, "curpage": 1,
             "sumNum": 1,
             "nodataflag": 1})
    def post(self,request):
        #modify user's information
        data = request.POST
        id = data.get('id', 0)
        username = data.get("username", "")
        email = data.get("email", "")
        phone = data.get("phone", "")
        psd = data.get("psd", "")
        dataitem = models.UserDict.objects.get(id=id)
        dataitem.username = username
        if psd != "123456":
            dataitem.set_password(psd)
        dataitem.email = email
        dataitem.phone = phone
        if request.FILES:
            pic = request.FILES.get('pic')
            dataitem.img = pic
        dataitem.save()
        return successResponseCommon({}, "Successfully modified!")
