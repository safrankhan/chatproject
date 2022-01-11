from django.db import models
from django.db.models import Model
from datetime import datetime
# Create your models here.
class user_1(Model):
    user_id=models.AutoField
    user_name=models.CharField(max_length=100)
    user_last=models.CharField(max_length=100)
    user_email=models.CharField(max_length=100)
    user_password=models.CharField(max_length=100)
    country=models.CharField(max_length=100, default='')
    def __str__(self):
        return self.user_name

def upload_location(instance, filename):
    return '%s/%s/%s' %(instance.userName,'profilePic',filename)

class addBot_1(Model):
    userName=models.CharField(max_length=100, unique=True ) 
    userSession=models.CharField(max_length=100)
    botName=models.CharField(max_length=100)
    desc=models.TextField()
    img=models.ImageField(upload_to=upload_location, null=True , blank=True)
    date = models.DateTimeField(default=datetime.now(), blank=True)  
    flag=models.BooleanField(default=0, blank=True)    
    def __str__(self):
        return self.userName

class template(Model):
    id=models.AutoField
    templateName=models.CharField(max_length=100)
    desc=models.TextField()
    def __str__(self):
        return self.templateName
         
class templateProperties(Model):
    id=models.AutoField
    temp_id=models.IntegerField(default=0)
    property_name = models.CharField(max_length=100)
    property_type = models.CharField(max_length=100)
    def __str__(self):
        return str(self.temp_id) + " " + str(self.property_name)
        
def upload_file(instance, filename):
    print("filename", instance.name,filename)
    return '%s/%s' %(instance.name,filename)

class aimlfile(Model):
    name=models.CharField(max_length=10, null=True)
    file=models.FileField(upload_to=upload_file, null=True , blank=True)
    def __str__(self):
        return str(self.file)
        