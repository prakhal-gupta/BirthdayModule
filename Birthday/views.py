import json
from django.http  import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
import re,os,random,string
from django.core.mail import send_mail
from datetime import date



def User_registration(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        First_Name_r         = data['first_name']
        Last_Name_r          = data['last_name']
        Username_r           = data['username']
        Email_r              = data['email']
        Password_r           = data['password']
        C_Password_r         = data['C_password']

        email_condition  = "[a-zA-Z0-9\-\_\.]+@[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,3}$"
        match   = re.search(email_condition,Email_r)

        if (not First_Name_r):
            mes = {'message': 'First Name Required !'}
            return JsonResponse(mes,status=403,safe=False)

        if (not Last_Name_r):
            mes = {'message': 'Last Name Required !'}
            return JsonResponse(mes,status=403,safe=False) 

        if (not Username_r):
            mes = {   'message': 'Username Required !'}
            return JsonResponse(mes,status=403,safe=False)

        if (User.objects.filter(username = data['username'])):
            mes = {   'message': 'Username Already Exists !'}
            return JsonResponse(mes,status=403,safe=False)         

        if (not Email_r):
            mes = {  'message': 'Email Required !'}
            return JsonResponse(mes,status=403,safe=False)

        if (not match):
            mes = { 'message': 'Invalid Email !'}
            return JsonResponse(mes,status=403,safe=False)

        if (User.objects.filter(email = data['email'])):
            mes = { 'message': 'Email Already Exists !'}
            return JsonResponse(mes,status=403,safe=False)

        if (not Password_r):
            mes = { 'message': 'Password Required !'}
            return JsonResponse(mes,status=403,safe=False)

        if (len(Password_r) <=8):
            mes = { 'message': 'Password must be atlesast 8 digit long !'}
            return JsonResponse(mes,status=403,safe=False)

        if (not C_Password_r):
            mes = { 'message': 'Confirm Password Required !'}
            return JsonResponse(mes,status=403,safe=False)    

        if (Password_r != C_Password_r):
            mes = {  'message': 'Password do not Match !'}
            return JsonResponse(mes,status=403,safe=False) 
                
        else:
            User.objects.create_user(username=Username_r, password=Password_r, first_name=First_Name_r, last_name=Last_Name_r, email=Email_r)   
    
            mes = { 'message': 'User Registered Successfully !'}
            return JsonResponse(mes,status=200,safe=False)



def User_login(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)
        Email_l = data['email']
        Password_l = data['password']
        if (not Email_l):
            mes = {  'message': 'Email Required!!'}
            return JsonResponse(mes,status=403,safe=False)

        if (not Password_l):
            mes = { 'message': 'Password Required !'}
            return JsonResponse(mes,status=403,safe=False)

        if(User.objects.filter(username=Email_l).exists()):         
            user = authenticate(request,username=Email_l, password=Password_l)
            Username_l = User.objects.get(username=Email_l).email 
            if user is not None: 
                login(request, user)
                send_mail(
                    'Birthday Module Login Alert',
                        'Hi ' + Username_l +
                        '\n\nYou just loggedin into your birthday module account.'
                        '\n\nRegards,'
                        '\nDepartment Of Information Technology' ,
                    'mailsenderdjango566@gmail.com',
                    [Username_l],
                    fail_silently=False,
                )
                mes = {  'message' :'Login Successful !'}
                return JsonResponse(mes,status=200,safe=False)

            else:
                
                mes ={  'message':'Wrong Credentials !'}
                return JsonResponse(mes,status=403,safe=False)

        else:
            Username_l = User.objects.get(email=Email_l).username 
            user = authenticate(request,username=Username_l, password=Password_l)

            if user is not None:
                login(request, user)
                send_mail(
                    'Birthday Module Login Alert',
                        'Hi ' + Username_l +
                        '\n\nYou just loggedin into your birthday module account.'
                        '\n\nRegards,'
                        '\nDepartment Of Information Technology' ,
                    'mailsenderdjango566@gmail.com',
                    [Email_l],
                    fail_silently=False,
                )
                mes = { 'message' :'Login Successful !'}
                return JsonResponse(mes,status=200,safe=False)

            else:
            
                mes = { 'message':'Wrong Credentials !'}
                return JsonResponse(mes,status=403,safe=False)



def User_dash(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            
            USer = User.objects.get(user=request.user)
            Name = USer.user.first_name +" " + USer.user.last_name

            mes = { 
                "name":Name,
                "Username":USer.user.username,
                "Email":USer.user.email,
                "Dob":USer.DOB,
                'Propic' : "static/Admin-profile.png"
                }
            return JsonResponse(mes,status=200,safe=False)
        else:
            mes = { "error"   :"Unauthorised Access !"}
            return JsonResponse(mes,status=401,safe=False) 


def Logout(request):
    
    if request.user.is_authenticated:
        logout(request)
        mes = { 'message' :"Logout Sucessfull!"}
        return JsonResponse(mes,status=200,safe=False)

    else:
        mes = {  "error":"Unauthorised Access!"}
        return JsonResponse(mes,status=401,safe=False)



def Profile_Creation(request):
    if request.method == 'POST':
        # if request.user.is_authenticated:

            # data = json.loads(request.body)
            file = request.FILES

            Name_r         = request.POST['Name']
            Email_r        = request.POST['Email']
            DOB_r          = request.POST['DOB']
            Year_r         = request.POST['Current_Year']
            Designation_r  = request.POST['Designation']
            Gender_r       = request.POST['Gender']
            Category_r     = request.POST['Category']
            Profile        = file['Profile_pic']

            email_condition  = "[a-zA-Z0-9\-\_\.]+@[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,3}$"
            match   = re.search(email_condition,Email_r)

            if (not Name_r):
                mes = {'message': 'Name Required !'}
                return JsonResponse(mes,status=403,safe=False)        

            if (not Email_r):
                mes = {  'message': 'Email Required !'}
                return JsonResponse(mes,status=403,safe=False)

            if (not match):
                mes = { 'message': 'Invalid Email !'}
                return JsonResponse(mes,status=403,safe=False)

            if (User.objects.filter(email = Email_r)):
                mes = { 'message': 'Email Already Exists !'}
                return JsonResponse(mes,status=403,safe=False)

            if (not DOB_r):
                mes = { 'message': 'DOB Required !'}
                return JsonResponse(mes,status=403,safe=False)  

            if (not Gender_r):
                mes = {  'message': 'Gender Required !'}
                return JsonResponse(mes,status=403,safe=False)

            if (not Category_r):
                mes = {  'message': 'Category Required !'}
                return JsonResponse(mes,status=403,safe=False)

            else:
                DoB =DOB_r.split("-")
                New_Profile=Student_Faculty_Profile(Name=Name_r, Email=Email_r, DOB=DOB_r,DOB_month=DoB[1],DOB_day=DoB[2], Current_Year=Year_r,Designation=Designation_r, Gender=Gender_r, Category=Category_r, Profile_pic=Profile)    
                New_Profile.save()   
        
                mes = { 'message': 'Profile Created Successfully!'}
                return JsonResponse(mes,status=200,safe=False)
        
        # else:
        #     mes = { "error"   :"Unauthorised Access !"}
        #     return JsonResponse(mes,status=401,safe=False)


def Birthday_messg(request):
    if request.method == 'POST':
        # if request.user.is_authenticated:
            data = json.loads(request.body)
            Content_r         = data['Content']

            if (not Content_r):
                mes = {'message': 'Message content Required !'}
                return JsonResponse(mes,status=403,safe=False)
            if (Birthday_Message.objects.filter(Content = Content_r)):
                mes = { 'message': 'Content Already Exists !'}
                return JsonResponse(mes,status=403,safe=False)            

            else:

                New_Message=Birthday_Message(Content=Content_r) 
                New_Message.save()   
        
                mes = { 'message': 'Message Saved !'}
                return JsonResponse(mes,status=200,safe=False)
        
        # else:
        #     mes = { "error"   :"Unauthorised Access !"}
        #     return JsonResponse(mes,status=401,safe=False)


def Student_Faculty_Delete(request):
    if request.method == 'POST':
        # if request.user.is_authenticated:
                data = json.loads(request.body)
                Id_r         = data['id']

                if (not Id_r):
                    mes = {'message': 'Id Required !'}
                    return JsonResponse(mes,status=403,safe=False)        

                else:
                    for Id in Id_r:
                        user = Student_Faculty_Profile.objects.get(id=Id)
                        if len(user.Profile_pic) > 0:   
                            os.remove(user.Profile_pic.path)
                        user.delete()
            
                    mes = { 'message': 'Profile Deleted!'}
                    return JsonResponse(mes,status=200,safe=False)
            
        # else:
        #         mes = { "error"   :"Unauthorised Access !"}
        #         return JsonResponse(mes,status=401,safe=False)  


def Student_Faculty_detail(request):
    if request.method == 'GET':
        # if request.user.is_authenticated:
            
            Student = Student_Faculty_Profile.objects.filter(Category="Student")
            Student_det = list(Student.values('Name','Email','DOB','Gender','Current_Year','Profile_pic'))
            Faculty = Student_Faculty_Profile.objects.filter(Category="Faculty") 
            Faculty_det = list(Faculty.values('Name','Email','DOB','Gender','Designation','Profile_pic'))  

                
            mes={"STUDENT": Student_det,
                 "FACULTY": Faculty_det}
            return JsonResponse(mes,status=200,safe=False)
        # else:
        #     mes = { "error"   :"Unauthorised Access !"}
        #     return JsonResponse(mes,status=401,safe=False)


def Birthday_Mail(request):
    if request.method == 'GET':
        # if request.user.is_authenticated:
            user = Student_Faculty_Profile.objects.all()
            Today_date = date.today()
            for USer in user:
                Dob = USer.DOB
                if (Today_date.month==Dob.month and Today_date.day==Dob.day):
                    if(USer.Category=="Student"):
                        send_mail(
                        'Happy Birthday '+USer.Name,
                        'Dear ' + USer.Name +
                        '\n\nWe value your special day just as much as we value you. On your birthday, we send you our warmest and most heartfelt wishes.'
                        '\n\nLife is full of adventure, and you have crossed another milestone in your adventurous life. Never stop dreaming and never leave the road to success. God’s blessings are always with you"' 
                        '\n\nOur entire Department wishes you a very happy birthday and wishes you the best on your special day!'
                        '\n\nRegards,'
                        '\nDepartment Of Information Technology' ,
                        'mailsenderdjango566@gmail.com',
                        [USer.Email],
                        fail_silently=False,
                    )
                    else:
                        send_mail(
                        'Happy Birthday '+USer.Name,
                        'Dear ' + USer.Name +
                        '\n\nWe value your special day just as much as we value you. On your birthday, we send you our warmest and most heartfelt wishes.'
                        '\n\nWe are thrilled to be able to share this great day with you, and glad to have you as a valuable member of the team. We appreciate everything you’ve done to help us flourish and grow.' 
                        '\n\nOur entire Department wishes you a very happy birthday and wishes you the best on your special day!'
                        '\n\nRegards,'
                        '\nDepartment Of Information Technology' ,
                        'mailsenderdjango566@gmail.com',
                        [USer.Email],
                        fail_silently=False,
                        )

            mes={'message':"Mail Sent Successfully !"}
            return JsonResponse(mes,status=200,safe=False)
        # else:
        #     mes = { "error"   :"Unauthorised Access !"}
        #     return JsonResponse(mes,status=401,safe=False)


def Birthday_List(request):
    if request.method == 'GET':
        # if request.user.is_authenticated:
            Today_date = date.today()
            Student = Student_Faculty_Profile.objects.filter(Category="Student",DOB_day=Today_date.day,DOB_month=Today_date.month)
            Student_det = list(Student.values('Name','Email','DOB','Gender','Current_Year','Profile_pic'))
            Faculty = Student_Faculty_Profile.objects.filter(DOB_month=Today_date.month,DOB_day=Today_date.day,Category="Faculty")                
            Faculty_det = list(Faculty.values('Name','Email','DOB','Gender','Designation','Profile_pic'))
            Birthday = Birthday_Message.objects.all()
            Birthday_mess = list(Birthday.values('id','Content'))

            mes={"STUDENT": Student_det,
                "FACULTY": Faculty_det,
                "Birthday_message":Birthday_mess}
            return JsonResponse(mes,status=200,safe=False)
        # else:
        #     mes = { "error"   :"Unauthorised Access !"}
        #     return JsonResponse(mes,status=401,safe=False)
        


def Password_Forgot(request):
    if request.method=='POST':
        data = json.loads(request.body)
        Email_c = data['Email']
        user = User.objects.get(email=Email_c)
        Email_l = user.email
        user_l = user.username
        if(Email_l==Email_c):
            a=list((string.digits))
            s=""
            for i in range(6):
              b=random.choice(a)
              s+=b
            send_mail(
                    'Birthday Module Password Reset',
                    'Hi ' + user_l +
                    '\n\nAs you have requested for password reset of your account.'
                    '\n\nYour OTP for password reset of Birthday module is: ' + s +
                    '\nThe OTP is valid for 10 minutes only'
                    '\n\nRegards,'
                    '\nDepartment Of Information Technology' ,
                    'mailsenderdjango566@gmail.com',
                    [Email_l],
                    fail_silently=False,
                )
            OTP_d    = Otp_Verification.objects.filter(Email=Email_l)
            if OTP_d:
                for otp in OTP_d:
                    Em = Otp_Verification.objects.get(OTP=otp)
                    Em.delete()    
            New_OTP = Otp_Verification(Email=Email_l,OTP=s)
            New_OTP.save()
            mes = { "Message"   :"OTP sent Successfully !"}
            return JsonResponse(mes,status=200,safe=False)

        else:
            mes = { "error"   :"No Account with this email is registered!"}
            return JsonResponse(mes,status=401,safe=False)


def OTP_Verification(request):
    if request.method=='POST':
        data = json.loads(request.body)
        otp_c    = data['OTP']
        Email_c  = data['Email']
        OTP_c    = Otp_Verification.objects.get(Email=Email_c)
        OTP_d    = OTP_c.OTP
        user     = User.objects.get(email=Email_c)
        user_l   = user.username
        if(otp_c==OTP_d):
            Password_r           = data['Password']
            C_Password_r         = data['C_Password']
            if (not Password_r):
                mes = { 
                    'message': 'New Password Required!!'}
                return JsonResponse(mes,status=403,safe=False)
            if (not C_Password_r):
                mes = { 
                    'message': 'Confirm Password Required!!'}
                return JsonResponse(mes,status=403,safe=False)
            if (Password_r != C_Password_r):
                mes = {    
                    'message': 'Password do not Match!!'}
                return JsonResponse(mes,status=403,safe=False)
            
            else:
                # Password_h = update_session_auth_hash(Password_r,user)
                user.set_password(Password_r)
                user.save()
                send_mail(
                'Birthday Module Password Changed',
                'Hi ' + user_l +
                '\n\nAs per your request Password for your Birthday Module Account is changed Successfully.'
                '\n\nKindly use new Password for further login.'
                '\n\nRegards,'
                '\nDepartment Of Information Technology' ,
                'mailsenderdjango566@gmail.com',
                [Email_c],
                fail_silently=False,
            )
                if OTP_d:   
                    OTP_c.delete()
                mes = { 
                    'message' :'Password Changed Successfully!'}
                return JsonResponse(mes,status=200,safe=False)

        else:
            mes = { 
                    'Error' :'Incorrect OTP'}
            return JsonResponse(mes,status=401,safe=False)


def Password_Change(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            Pre_Password = data['Prev_Password']
            if (not Pre_Password):
                mes = { 
                    'message': 'Previous Password Required!!'}
                return JsonResponse(mes,status=403,safe=False)
            user = User.objects.get(user=request.user)
            # Password_c = user.password
            user_l = user.username
            Password_cr  = authenticate(request.user,username=user_l,password=Pre_Password)
            if (Password_cr):

                Password_r           = data['Password']
                C_Password_r         = data['C_Password']
                if (not Password_r):
                    mes = { 
                        'message': 'New Password Required!!'}
                    return JsonResponse(mes,status=403,safe=False)
                if (not C_Password_r):
                    mes = { 
                        'message': 'Confirm Password Required!!'}
                    return JsonResponse(mes,status=403,safe=False)

                if(Pre_Password == Password_r):
                    mes = { 
                        'message' :'Please Enter different Password from Previous One!!'}
                    return JsonResponse(mes,status=403,safe=False)  
                if (Password_r != C_Password_r):
                    mes = {    
                        'message': 'Password do not Match!!'}
                    return JsonResponse(mes,status=403,safe=False)
                
                else:
                    user.set_password(Password_r)
                    user.save()
                    send_mail(
                    'Birthday Module Password Changed',
                    'Hi ' + user_l +
                    '\n\nAs per your request Password for your Birthday Module Account is changed Successfully.'
                    '\n\nKindly use new Password for further login.'
                    '\n\nRegards,'
                    '\nDepartment Of Information Technology' ,
                    'mailsenderdjango566@gmail.com',
                    [data['email']],
                    fail_silently=False,
                )
                    mes = { 
                        'message' :'Password Changed Successfully!'}
                    return JsonResponse(mes,status=200,safe=False)

            else:
                    mes = { 
                        'message' :'Previous Password doesnot Match!!'
                }
            return JsonResponse(mes,status=403,safe=False)

        else:
            mes = { "error"   :"Unauthorised Access !"}
            return JsonResponse(mes,status=401,safe=False)

       
            

        


