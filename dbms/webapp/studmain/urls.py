from django.urls import reverse
from django.urls import path
from . import views

urlpatterns = [
    path('submitted/', views.submitted,name='submitted'),
    path('', views.studmain,name='studmain'),
    path('studprofile/',views.studprofile,name='studprofile'),
    path('studtest/',views.studtest,name='studtest'),
    path('studannouncement/',views.studannouncement,name='studannouncement'),
    path('studgocourse/',views.studgocourse,name='studgocourse'),
    path('studfaq/',views.studfaq,name='studfaq'),
    path('studcontact/',views.studcontact,name='studcontact'),
    path('studfeed/',views.studfeed,name='studfeed'),
    path('studmodule/',views.studmodule,name='studmodule'),
    path('studassignsub/',views.studassignsub,name='studassignsub'),
    path('studpro/',views.studpro,name='studpro'),
    path('studgrade/',views.studgrade,name='studgrade'),
    path('studreg/',views.studreg,name='studreg'),
    path('quizdone/',views.quizdone,name='quizdone'),
    path('assigndone/',views.assigndone,name='assigndone'),
    path('feedone/',views.assigndone,name='assigndone'),

]

