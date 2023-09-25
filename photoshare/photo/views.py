from email.message import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import category,Photo
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CustomUser
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .utils import pagination
from django.template.loader import get_template
from xhtml2pdf import pisa
# Create your views here.

def loginuser(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']
        
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('gallery')
        
        messages.warning(request,"Bad login credentials")

    u=User.objects.all()
    return render(request,'photos/login.html',{'page':page , 'user':u})

def logoutuser(request):
    logout(request)
    return redirect('login')

def registeruser(request):
    page = 'register'
    form=CustomUser()
    context = {'form':form, 'page':page}
    if request.method=="POST":
        form = CustomUser(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            user = authenticate(request,username=user.username,password=request.POST['password1'])
            welcome(user.username,user.email)

            if user is not None:
                login(request,user)
                return redirect('gallery')
        
        else:
            context = {'form':form, 'page':page}
            return render(request, 'photos/login.html',context)
    return render(request, 'photos/login.html',context)

@login_required(login_url='login')
def gallery(request):
    categories=category.objects.all()
    u=User.objects.all()
    z=0
    if(len(u)==1):
        z=1
    Cate = request.GET.get('c')
    if Cate == None:
        p=Photo.objects.all()
    elif Cate == 'myphotos':
        a=request.user
        p=Photo.objects.filter(user=a)
        context={'categories':categories,'photos':p,'user':u ,'z':z}
        return render(request,'photos/gallery.html',context)
    else:
        p=Photo.objects.filter(category__name=Cate)
        context={'categories':categories,'photos':p,'user':u ,'z':z}
        return render(request,'photos/gallery.html',context)
       
    page = request.GET.get('page')
    p,custom_range = pagination(request,page,p)
    

    context={'categories':categories,'photos':p,'user':u ,'z':z, 'custom_range':custom_range}
    return render(request,'photos/gallery.html',context)

@login_required(login_url='login')
def view(request,pk):
    categories=category.objects.all()
    p=Photo.objects.get(id=pk)
    u=User.objects.all()
    z=a=0
    if(len(u)==1):
        z=1
    if p.user == request.user:
        a=1
    context={'photos':p ,'categories':categories,'user':u,'z':z,'a':a}
    return render(request,'photos/photo.html',context)

@login_required(login_url='login')
def send(request,pk):
    if request.method == 'POST':
        mail = request.POST['mail']
        m = Photo.objects.get(id=pk)
        template_path = 'photos/pdf1.html'
        context = {'user': m}
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="a.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)

        k = EmailMessage(
        'Welcome To PhotoShare ',
        'Photos From PhotoShare' ,
        settings.EMAIL_HOST_USER,
        [mail],
        )
        k.attach('a.pdf',response.getvalue(),'application/pdf')
        k.send()


        # create a pdf
        pisa_status = pisa.CreatePDF(
        html, dest=response)
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
        
    return render(request,'photos/send.html')

def sendimage(request):
    print(90)
    m = User.objects.all()
    template_path = 'photos/pdf1.html'
    context = {'user': m}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="a.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


    

@login_required(login_url='login')
def add(request):
    categori=category.objects.all()
    u=User.objects.all()
    z=0
    if(len(u)==1):
        z=1
    context={'categories':categori , 'user':u,'z':z}
    if request.method == 'POST':
        data=request.POST
        image = request.FILES.get('image')
    
        if data['category']=='none' and data['category_new']=='':
            messages.warning(request,"Please enter an category")
            return render(request,'photos/add.html',context)
        
        if data['category']!='none' and data['category_new']!='':
            messages.warning(request,"Please enter single category field")
            return render(request,'photos/add.html',context)

        if data['category'] != 'none':
            Category = category.objects.get(id=data['category'])

        if data['category_new'] != '':
            Category , created= category.objects.get_or_create(name=data['category_new']) 

        photo = Photo.objects.create(
            category=Category,
            user=request.user,
            description = data['description'],
            image=image,
        )

        return redirect('gallery')
    return render(request,'photos/add.html',context)

def welcome(username,usermail):
    messages_mail = "Hello "+username+" , we are glad to see you here" 
    send_mail(
        'Welcome To PhotoShare ',
        messages_mail,
        settings.EMAIL_HOST_USER,
        [usermail],
        fail_silently=False,
    )

def delete(request,pk):
    p = Photo.objects.get(id=pk)
    u=User.objects.all()
    categori=category.objects.all()
    z=0
    if(len(u)==1):
        z=1
    context = {'photo' : p , 'categories':categori , 'user':u,'z':z}
    return render(request,'photos/confirm_delete.html',context)

def delet(request,pk):
    p = Photo.objects.get(id=pk)
    p.delete()
    return redirect('gallery')

def delete_cat(request,pk):
    cat = category.objects.get(id=pk)
    p=Photo.objects.filter(category__name=cat)
    u=User.objects.all()
    z=0
    if(len(u)==1):
        z=1
    context = {'cat' : p , 'c':1 , 'user':u , 'c' : cat, 'z':z}
    return render(request,'photos/confirm_delete.html',context)

def del_user(request,pk):
    p=Photo.objects.filter(user__username=pk)
    u=User.objects.all()
    z=0
    if(len(u)==1):
        z=1
    context = {'cat' : p , 'user':u , 'z':z,'pk':pk}
    return render(request,'photos/delete_user.html',context)

def confirm_delete_cat(request,pk):
    c = category.objects.get(id=pk)
    c.delete()
    return redirect('gallery')
    
def confirm_delete_user(request,pk):
    photo = Photo.objects.filter(user__username=pk)
    for p in photo:
        p.delete();
    u=User.objects.get(username=pk)
    u.delete()
    return redirect('gallery')