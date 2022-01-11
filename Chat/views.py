from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime
from django.db.models import Q
from Chat.models import user_1, addBot_1, template, templateProperties, aimlfile
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
import requests
import json
import os
import aiml
import shutil
k = aiml.Kernel()  
l = aiml.Kernel()


def login(request):
    if 'save' in request.session:
        return redirect("/index/")
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    data = user_1.objects.filter(Q(user_email=email) & Q(user_password=password))
    farhan = (user_1.objects.filter(user_email=email).exists())
    print(farhan)
    if len(data) == 1:
        request.session['save'] = email
        return redirect('/index')
    return render(request, 'login.html', {})


def register(request):
    name = (request.POST.get("fname", "")).capitalize()
    last = (request.POST.get("lname", "")).capitalize() 
    email = request.POST.get("email", "")
    password = request.POST.get("password", "")
    clientkey=request.POST.get('g-recaptcha-response')
    secretkey='6Lekz8sZAAAAAGzLsQFam_MfFsS64GpG3uBsTSe2'
    captchaData={
        'secret':secretkey,
        'response':clientkey
    }
    r=requests.post(' https://www.google.com/recaptcha/api/siteverify', data=captchaData)
    response=json.loads(r.text)
    varify = response['success']

    if name != '' and password != '' and last != ''and email != '' and varify:
        myuser = user_1(user_name=name, user_email=email,
                    user_password=password, user_last=last, country='india')
        myuser.save()
        return redirect('/')
    return render(request, 'register.html', {})

def email_validate (request):
    email = request.GET.get('email', None)
    print(email,'ddddddd')
    data = user_1.objects.filter(user_email=email).exists()
    return HttpResponse(data)

def index(request):
    global data1
    if 'save' not in request.session:
        return redirect('/')
    data1 = user_1.objects.filter(user_email=request.session['save'])
    bot = addbot_1.objects.filter(Q(userSession=request.session['save']) & Q(flag=0)).order_by('-pk')
    return render(request, 'index.html', {'data': data1, 'data1': bot})

def deletebot(request, id):
    data = addbot_1.objects.get(pk=id)
    data.flag = 1
    data.save()
    return redirect('/index/')


def restore(request, id):
    data = addbot_1.objects.get(pk=id)
    data.flag = 0
    data.save()
    return redirect('/index/')


def deleteforever(request, id):
    data = addbot_1.objects.get(pk=id)
    data.delete()
    shutil.rmtree('C:/Users/Farhan/Desktop/chatproj/chatproject/Chat/Users/'+data.userName)
    return redirect('/index/')


def addbot(request):
    global l
    if 'save' not in request.session:
        return redirect('/')
    username = request.POST.get("UserName", "")
    botname = request.POST.get("botname", "")
    discription = request.POST.get("botDescription", "")
    image = request.FILES.get("profilePic", '')
    template1 = request.POST.get('template', '')
    if username != '' and botname != '' and image != '':
        myuser = addbot_1(userName=username, userSession=request.session['save'], botName=botname, desc=discription, img=image)
        myuser.save()
        properties = templateProperties.objects.filter(temp_id=template1)
        file = open("Chat/Users/"+username+"/properties.txt", "wt")
        file.write('properties {  '+'\n')
        for f in properties:
            file.write(str(' '+f.property_name)+'=' +request.POST.get((str(f.property_name).replace(" ", "")), ' '))
            file.write(" ;"+'\n')
        file.write('  }')
        file.close()
        file1 = open("Chat/Users/"+username+"/personal.aiml", "wt")
        file1.write('<?xml version="1.0" encoding="UTF-8"?><aiml version="1.0">'+'\n')
        file1.write('<category>'+'\n<pattern>DO YOU KNOW MY NAME</pattern>'+'\n')
        file1.write('<template>Yes. you are '+username+ '</template> '+'\n </category> '+'\n </aiml>')
        file1.close()

        BRAIN_FILE1 = "C:/Users/Farhan/Desktop/chatproj/chatproject/Chat/Users/" +username+"/brain.dump"
        FILE = "C:/Users/Farhan/Desktop/chatproj/chatproject/Chat/Users/" +username+"/personal.aiml"
        print("Parsing aiml files")
        l.bootstrap(learnFiles=FILE)
        print("Saving brain file: " + BRAIN_FILE1)
        l.saveBrain(BRAIN_FILE1)

        return redirect('/index/')
    data = template.objects.filter()
    data1 = user_1.objects.filter(user_email=request.session['save'])
    bot = addbot_1.objects.filter(Q(userSession=request.session['save']) & Q(flag=1)).order_by('-pk')
    return render(request, 'addbot_1.html', {'data': data1, 'template': data, 'data1': bot})


def fetchProperties(request):
    id = request.GET.get('template', None)
    i = 0
    Name = template.objects.get(pk=id)
    data = "<h3>Edit Properties</h3><p><b><i>" + \
        Name.templateName + "</i></b></p><br>"
    data += '<table class="table table-bordered" cellpadding="5">'
    data += "<tr><th>Sr.</th><th>Property</th><th>Value</th></tr>"

    properties = templateProperties.objects.filter(temp_id=id)
    for x in properties:
        data += '<tr>'
        i += 1
        data += "<td>"+str(i)+"</td>"
        if(x.property_type == 'gender'):
            data += '<td>' + x.property_name + '</td><td><input name="' + str(x.property_name).replace(" ", "") + '" type="radio" id="Male" value="Male"/> Male <input name="' + str(
                x.property_name).replace(" ", "") + '" type="radio" id="Female" value="Female"/> Female</td>'
        elif(x.property_type == 'textarea'):
            data += '<td>' + x.property_name + '</td><td><textarea name="' + \
                str(x.property_name).replace(" ", "") + \
                '" id="address"></textarea></td>'
        else:
            data += '<td>' + x.property_name + '</td><td><input name="' + \
                str(x.property_name).replace(" ", "") + '" type="' + \
                x.property_type + '" id="name" /></td>'
    return HttpResponse(data)


def editAIML(request):
    if 'save' not in request.session:
        return redirect('/')
    data1 = user_1.objects.filter(user_email=request.session['save'])
    bot = addbot_1.objects.filter(
        Q(userSession=request.session['save']) & Q(flag=0)).order_by('-pk')
    file = request.GET.get('username', '')
    bot1 = addbot_1.objects.filter(userName=file)
    for x in bot1:
        if x.userName == file:
            entries = os.listdir(
                'C:/Users/Farhan/Desktop/chatproj/chatproject/Chat/Users/'+file)
            entries.remove('profilePic')
            return render(request, 'editaiml.html', {'data': data1, 'data1': bot, 'filename': entries, 'path': file})

    return render(request, 'editaiml.html', {'data': data1, 'data1': bot})


def file(request):
    path = request.GET.get('file', '')
    data = open('Chat/Users/'+path, 'rt')
    data1 = data.read()
    return HttpResponse(data1)


def form(request, username, filename):
    value = request.GET.get('value', '')
    data = request.GET.get('rename', '')
    if len(value) != 0 and filename != 'null':
        data = open('Chat/Users/'+username+'/'+data, 'wt')
        data.write(value)
        data.close


def trash(request):
    if 'save' not in request.session:
        return redirect('/')
    data1 = user_1.objects.filter(user_email=request.session['save'])
    bot = addbot_1.objects.filter(
        Q(userSession=request.session['save']) & Q(flag=1)).order_by('-pk')
    return render(request, 'trash.html', {'data': data1, 'data1': bot})


def logout(request):
    del request.session['save']
    return redirect('/')


def validate_username(request):
    username = request.GET.get('username', None)
    data = addbot_1.objects.filter(userName=username).exists()
    return HttpResponse(data)


def globalsearch(request):
    username = request.GET.get('search', None).upper()
    sql = "SELECT * FROM `chat_addbot` WHERE `flag`=0 AND `botName` LIKE '%" + username + "%' "
    data1 = addbot_1.objects.raw(sql)
    data = ''
    for x in data1:
        data += '<a href="#" class="list-group-item list-group-item-action"><img src="/media/' + \
            str(x.img)+'" class="thumb-sm img-circle bx-s" /> &nbsp &nbsp &nbsp<span>' + \
            x.botName+'</span></a>'
    return HttpResponse(data)


def search(request):
    if 'save' not in request.session:
        return redirect('/')
    prof = user_1.objects.filter(user_email=request.session['save'])
    search = request.GET.get('gsearch', '')
    data = addbot_1.objects.filter(Q(botName=search) & Q(
        flag=0) & Q(userSession=request.session['save']))
    data1 = addbot_1.objects.filter(Q(botName=search) & Q(flag=0))
    for x in data:
        if search == x.botName:
            length = len(data)
            print(search)
            return render(request, 'search.html', {'data1': data, 'length': length, 'search': search, 'data': prof})
    for x in data1:
        if search == x.botName:
            length = len(data1)
            print(search)
            return render(request, 'search1.html', {'data1': data1, 'length': length, 'search': search, 'data': prof})
    return render(request, 'notfound.html', {'search': search, 'data1': data, 'data': prof})


def chatbot(request, id):
    global k
    global l
    data = addbot_1.objects.filter(pk=id)
    if 'save' not in request.session:
        return redirect('/')
    BRAIN_FILE = "brain.dump"
    for x in data:
        print(x.userName)
        BRAIN_FILE1 = "C:/Users/Farhan/Desktop/chatproj/chatproject/Chat/Users/" +x.userName+"/brain.dump"
    if os.path.exists(BRAIN_FILE1):
        print("Loading from brain file: " + BRAIN_FILE1)
        l.loadBrain(BRAIN_FILE1)
    if os.path.exists(BRAIN_FILE):
        print("Loading from brain file: " + BRAIN_FILE)
        k.loadBrain(BRAIN_FILE)
    else:
        print("Parsing aiml files")
        k.bootstrap(learnFiles='std-startup.aiml', commands="load aiml b")
        print("Saving brain file: " + BRAIN_FILE)
        k.saveBrain(BRAIN_FILE)
    return render(request, 'chatbox.html', {'data1': data})


def chatbotinput(request):
    global k
    global l
    chat = request.GET.get('username', None)
    data = l.respond(chat)
    if (data)=='':
        data = k.respond(chat)
    return HttpResponse(data)


def uploadaimlfile(request, username):
    uploadfile = request.FILES.get('uploadfile', None)
    if request.method == "POST":
        myfile = aimlfile(file=uploadfile, name=username)
        myfile.save()
    return redirect('/editaiml?username='+username)


def filedelete(request, username, filename):
    data = aimlfile.objects.filter(name=username)
    for x in data:
        if x == username:
            data.delete()
    os.remove(
        'C:/Users/Farhan/Desktop/chatproj/chatproject/Chat/Users/'+username+'/'+filename)
    return redirect('/editaiml?username='+username)


def rename_file(request, username, filename):
    data = request.GET.get('rename', '')
    os.rename(r'Chat/Users/'+username+'/'+filename,
              r'Chat/Users/'+username+'/'+data)
    return HttpResponse(data)


def filecheck(request, folder):
    existfile = request.GET.get('check_rename', '')
    if os.path.exists('C:/Users/Farhan/Desktop/chatproj/chatproject/Chat/Users/'+folder+'/'+existfile):
        data = 'yes'
        return HttpResponse(data)
    data = 'no'
    return HttpResponse(data)


def newfile(request, folder):
    no1 = request.GET.get('name', '')
    no = int(no1)
    if (no) == 0:
        file = 'untitled'
    else:
        file = 'untitled'+str(no)
    if os.path.exists('C:/Users/Farhan/Desktop/chatproj/chatproject/Chat/Users/'+folder+'/'+file):
        entries = os.listdir(
            'C:/Users/Farhan/Desktop/chatproj/chatproject/Chat/Users/'+folder)
        for x in entries:
            if x == 'untitled'+str(no) or x == 'untitled':
                (no) += 1
        return HttpResponse('{"data": true,"no": '+str(no)+'}')
    return HttpResponse('{"data": false,"no": '+str(no)+',"file": "'+file+'"}')
def profile(request,id):
    data1 = user_1.objects.filter(id=id)
    for x in data1:
        email=x.user_email
        fname=(x.user_name)[0]
        lname=(x.user_last)[0]
    data=addbot_1.objects.filter(userSession=email)
    length=[]
    for x in (data):
        length.append(x.userName)
    count=len(length)
    return render(request, 'profile.html', {'data':data1,'fname':fname,'lname':lname,'count':count})
def help(request,id):
    data1 = user_1.objects.filter(id=id)
    return render(request, 'help.html', {'data':data1})
def faq(request,id):
    data1 = user_1.objects.filter(id=id)
    return render(request, 'frequentlyask.html', {'data':data1})
def resetpassword (request):
    return render(request, 'resetpassword.html',{})
def editintro (request, id):
    frename = request.POST.get('firstname')
    lrename= request.POST.get('lastname')
    country= request.POST.get('country')
    data=user_1.objects.filter(id=id)

    return render(request, 'editintro.html',{'data':data} )
