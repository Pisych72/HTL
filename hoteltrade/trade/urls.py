from django.conf.urls.static import static
from django.urls import path

from hoteltrade import settings
from .views import *

urlpatterns=[
   path('',main,name='home'),
   path('listpage/',listpage,name='listpage'),
   path('Create/<TableName>',Create,name='Create'),
   path('Delete/<TableName>/<str:pk>',Delete,name='Delete'),
   path('Update/<TableName>/<str:pk>',Update,name='Update'),
   path('Category',CategoryPage,name='Category'),
   path('UpdateCategory/<str:pk>',UpdateCategory,name='UpdateCategory'),
   path('DeleteCategory/<str:pk>',DeleteCategory,name='DeleteCategory'),
   path('Good',Goods,name='Good'),
   path('UpdateGood/<str:pk>',UpdateGoods,name='UpdateGoods'),
   path('DeleteGood/<str:pk>',DeleteGoods,name='DeleteGoods'),
   path('DocPage',DocPage,name='DocPage'),
   path('InitialDoc',InitialDoc,name='InitialDoc'),
   path('CreateInitialDoc',CreateInitialDoc,name='CreateInitialDoc'),
   path('UpdateInitialDoc/<str:pk>',UpdateInitialDoc,name='UpdateInitialDoc'),
   path('DeleteInitialDoc/<str:pk>',DeleteInitialDoc,name='DeleteInitialDoc'),
   path('DeleteDoc/<str:pk>',DeleteDoc,name='DeleteDoc'),
   path('DeleteDocString/<str:pk>',DeleteDocSting,name='DeleteDocString'),
]

if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)