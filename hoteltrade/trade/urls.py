from django.conf.urls.static import static
from django.urls import path

from hoteltrade import settings
from .views import *

urlpatterns=[
   path('',loginUser,name='loginUser'),
   path('out/',UserOut,name='UserOut'),
   path('main/',main,name='home'),
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
   path('DeleteRDoc/<str:pk>',DeleteRDoc,name='DeleteRDoc'),
   path('DeleteDocString/<str:pk>',DeleteDocSting,name='DeleteDocString'),
   path('UpdateDocString/<str:pk>',UpdateDocString,name='UpdateDocString'),
   path('ReceiptDoc',ReceiptDoc,name='ReceiptDoc'),
   path('CreateReceiptDoc',CreateReceiptDoc,name='CreateReceiptDoc'),
   path('UpdateReceiptDoc/<str:pk>',UpdateReceiptDoc,name='UpdateReceiptDoc'),
   path('DeleteReceiptDoc/<str:pk>',DeleteReceiptDoc,name='DeleteReceiptDoc'),

   path('UpdateReceiptDoc/<str:pk>', UpdateReceiptDoc, name='UpdateReceiptDoc'),
   path('UpdateReceiptDocString/<str:pk>',UpdateReceiptDocString,name='UpdateReceiptDocString'),
   path('DeleteRDocString/<str:pk>',DeleteRDocSting,name='DeleteRDocString'),
   path('GetData',GetData,name='GetData'),
   path('GoodToCheck/<str:pk>/<str:price>',GoodToCheck,name='GoodToCheck'),
   path('DeleteCheckRecord/<str:pk>/<str:price>',DeleteCheckRecord,name='DeleteCheckRecord'),
   path('IncVolume/<str:pk>/<str:price>',IncVolume,name='IncVolume'),
   path('DecVolume/<str:pk>/<str:price>', DecVolume, name='DecVolume'),
   path('DeleteCheck',DeleteCheck,name='DeleteCheck'),
   path('CashCheck/<mode>',CashCheck,name='CashCheck'),

   path('CheckJurnal',CheckJurnal,name='CheckJurnal'),
   path('Proba/<str:pk>',Proba,name='Proba'),
]

if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)