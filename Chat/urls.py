from django.urls import path
from . import views
from django.conf.urls import url
urlpatterns = [
    path('',views.login,name='index'),
    path('register/',views.register,name='register'),
    path('index/',views.index,name='index'),
    path('addbot/',views.addbot,name='addbot'),
    url(r'^chatbot/(\w+)/',views.chatbot,name='chatbot'),
    url(r'^ajax/chatbotinput/',views.chatbotinput,name='chatbotinput'),
    path('editaiml/',views.editAIML,name='editAIML'),
    path('trash/',views.trash,name='trash'),
    path('logout/',views.logout,name='logout'),
    url(r'^addbot/fetchProperties/$',views.fetchProperties,name='fetchProperties'),
    url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
    url(r'/delete/(\d+)/',views.deletebot, name='deletebot'),
    url(r'/restore/(\d+)/',views.restore, name='restorebot'),
    url(r'/deleteforever/(\d+)/',views.deleteforever, name='deleteforever'),
    url(r'^ajax_calls/search/',views.globalsearch, name='globalsearch'),   
    path('search/',views.search,name='search'),
    path('filevalue/',views.file,name='file'),
    url(r'^uploadaimlfile/(.+)/',views.uploadaimlfile,name='uploadaimlfile'),
    url(r'^form/submission/(.+)/(.+)/',views.form,name='form'),
    url(r'^filedelete/(.+)/(.+)/',views.filedelete,name='filedelete'),
    url(r'^save/rename_file/(.+)/(.+)/',views.rename_file,name='rename_file'),
    url(r'^ajax/newfile/(.+)/',views.newfile,name='newfile'),
    url(r'^filename/check/(.+)/',views.filecheck,name='newfile'),
    url(r'profile/(.+)/',views.profile,name='profile'),
    url(r'help/(.+)/',views.help,name='help'),
    url(r'faq/(.+)/',views.faq,name='faq'),
    path('resetpassword/',views.resetpassword,name='resetpassword'),
    url(r'^ajax/validate_email/',views.email_validate,name='email_validate'),
    url(r'editintro/(.+)/', views.editintro, name='editintro')
    
    
    
    # path('editAIML/',views.editAIML,name='editAIML'),s





]