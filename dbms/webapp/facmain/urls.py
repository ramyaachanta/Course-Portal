from django.urls import path
from facmain.views import facassigning
from . import views

urlpatterns = [
    path('', views.facmain,name='facmain'),#np
    #path('facsub/facassigning/', views.facmain,name='facmain'),#np
    #path('facassigning/', views.facmain,name='facmain'),#np

    path('factest/posting/',views.posting,name='posting'),
    path('facprofile/',views.facprofile,name='facprofile'),
    path('factest/',views.factest,name='factest'),
    path('facannouncement/',views.facannouncement,name='facannouncement'),
    path('facgocourse/',views.facgocourse,name='facgocourse'),
    path('facfaq/',views.facfaq,name='facfaq'),
    path('facsub/',views.facsub,name='facsub'),
    path('facassign/',views.facassigning,name='facassigning'),
    path('faccontact/',views.faccontact,name='faccontact'),
    path('facupload/',views.facupload,name='facupload'),
    path('/testdone',views.testdone,name='testdone'),
    path('/assigndone',views.assigndone,name='assigndone'),
    path('/matdone',views.matdone,name='matdone'),
    path('/ans',views.ans,name='ans'),
    
]
