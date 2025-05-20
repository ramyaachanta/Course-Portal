from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login,name='login'),
    path('doLogout',views.doLogout,name='doLogout'),
    path('home', views.home,name='home'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('studmain/', views.studmain,name='studmain'),
    path('studprofile/',views.studprofile,name='studprofile'),
    path('studDoProfile/', views.studDoProfile, name='studDoProfile'),
    path('studgradelist/',views.studgradelist,name='studgradelist'),
    path('studannouncement/',views.studannouncement,name='studannouncement'),
    path('studgocourse/',views.studgocourse,name='studgocourse'),
    path('studfaq/',views.studfaq,name='studfaq'),
    path('studcontact/',views.studcontact,name='studcontact'),
    # path('studfeed/',views.studfeed,name='studfeed'),
    path('studmodule/',views.studmodule,name='studmodule'),
    path('studassignsub/',views.studassignsub,name='studassignsub'),
    path('studgrade/',views.studgrade,name='studgrade'),
    path('studreg/',views.studreg,name='studreg'),
    path('quizdone/',views.quizdone,name='quizdone'),
    path('assigndone/',views.assigndone,name='assigndone'),
    path('feedone/',views.assigndone,name='assigndone'),
    path('submitted/', views.submitted,name='submitted'),
    path('studassignment/',views.studassignment,name='studassignment'),

     path('facmain/', views.facmain,name='facmain'),#np
    path('factest/posting/',views.posting,name='posting'),
    path('facprofile/',views.facprofile,name='facprofile'),
    path('facDoProfile/', views.facDoProfile, name='facDoProfile'),
    path('facDelMat/',views.facDelMat,name='facDelMat'),
    path('submit_marks/', views.submit_marks, name='submit_marks'),
    path('facannouncement/',views.facannouncement,name='facannouncement'),
    path('facannouncementlist/',views.facannouncementlist,name='facannouncementlist'),
    path('facgocourse/',views.facgocourse,name='facgocourse'),
    path('facfaq/',views.facfaq,name='facfaq'),
    path('facsub/',views.facsub,name='facsub'),
    path('facassign/',views.facassigning,name='facassigning'),
    path('faccontact/',views.faccontact,name='faccontact'),
    path('facupload/',views.facupload,name='facupload'),
    path('/testdone',views.testdone,name='testdone'),
    path('/assigndone',views.assigndone,name='assigndone'),
    path('/matdone',views.matdone,name='matdone'),
    path('/viewassignsub',views.viewassignsub,name='viewassignsub'),
    path('/assignmentstudlist',views.assignmentstudlist,name='assignmentstudlist'),
    path("smartchat/", views.smart_chatbot, name="smart_chatbot"),


]
