from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .forms import *
from django.db.models import Sum
from django.contrib import messages
import datetime
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import *
uniqueGood={}
unDict={}
toCheck={}
checkSumma=0
message=''
maxvolume=None

def main(request):
    gruppa = request.user.groups.all()[0]
    if request.user.is_authenticated:
        gruppa = str(request.user.groups.all()[0])
    print(type(gruppa),gruppa)
    return render(request, 'trade/main.html', {'title': 'Главная страница','gruppa':gruppa})

def listpage(request):
    return render(request, 'trade/listpage.html', {'title': 'Справочники'})

def DocPage(request):
    return render(request, 'trade/DocPage.html', {'title': 'Документы'})

def InitialDoc(request):
    InitialDoc=Doc.objects.filter(typedoc=2).order_by('-datadoc')
    return render(request, 'trade/InitialDocs.html', {'title': 'Ввод начальных остатков','doc':InitialDoc})

def ReceiptDoc(request):
    ReceiptDoc=Doc.objects.filter(typedoc=1).order_by('-datadoc')
    return render(request, 'trade/ReceiptDoc.html', {'title': 'Приходные документы','doc':ReceiptDoc})

#  новый документ Поступление:
def CreateReceiptDoc(request):
    if request.method == 'POST':
        form = ReceiptDocForm(request.POST)
        form2 = ReceiptTableForm(request.POST)
        if form.is_valid() and form2.is_valid():

            formDoc=form.save()
            formTable=form2.save(commit=False)
            formTable.iddoc_id=formDoc.id
            formTable.save()

            Doc.objects.filter(id=formDoc.id).update(buytotal=formTable.buytotal,saletotal=formTable.saletotal)
            url = reverse('UpdateReceiptDoc', kwargs={'pk': formDoc.id})
            return HttpResponseRedirect(url)
    else:
        form = ReceiptDocForm(initial={'typedoc':1})
        form2 = ReceiptTableForm(initial={'typedoc': 1 })
    return render(request,'trade/CreateReceiptDoc.html',{'title': 'Новый документ (Поступление)','form':form,'form2':form2})

# Редактирование докмента Поступление

def UpdateReceiptDoc(request,pk):
    CurrentDoc=Doc.objects.get(pk=pk)
    CurrentTable=DocJurnal.objects.filter(iddoc_id=pk)
    if request.method == 'POST':
        docheader = ReceiptDocForm(request.POST)
        if 'FormHeader' in request.POST:
            print(request.POST)
            print('YES')
            CurrentDoc.nomerdoc = request.POST.get("nomerdoc")
            CurrentDoc.datadoc = request.POST.get("datadoc")
            CurrentDoc.save()
            return redirect('ReceiptDoc')
        form = ReceiptTableForm(request.POST)


        if form.is_valid():
            formTable = form.save(commit=False)
            formTable.iddoc_id = CurrentDoc.id
            formTable.save()
            sum_buy = DocJurnal.objects.filter(iddoc_id=pk).aggregate(Sum('buytotal'))
            sum_sale = DocJurnal.objects.filter(iddoc_id=pk).aggregate(Sum('saletotal'))
            Doc.objects.filter(id=pk).update(buytotal=sum_buy['buytotal__sum'], saletotal=sum_sale['saletotal__sum'])
            if sum_sale['saletotal__sum'] == None and sum_buy['buytotal__sum'] == None:
                Doc.objects.filter(id=pk).update(buytotal=0.00, saletotal=0.00)
            url = reverse('UpdateReceiptDoc', kwargs={'pk': CurrentDoc.id})
            return HttpResponseRedirect(url)
    else:
        CurrentDoc = Doc.objects.get(pk=pk)
        CurrentTable = DocJurnal.objects.filter(iddoc_id=pk)
        sum_buy = DocJurnal.objects.filter(iddoc_id=pk).aggregate(Sum('buytotal'))
        sum_sale = DocJurnal.objects.filter(iddoc_id=pk).aggregate(Sum('saletotal'))
        Doc.objects.filter(id=pk).update(buytotal=sum_buy['buytotal__sum'],saletotal=sum_sale['saletotal__sum'])
        if sum_sale['saletotal__sum'] == None and sum_buy['buytotal__sum'] == None:
            Doc.objects.filter(id=pk).update(buytotal=0.00, saletotal=0.00)
        form = ReceiptTableForm(initial={'typedoc': 2,'iddoc_id':CurrentDoc.id })

        docheader = ReceiptDocForm(instance=CurrentDoc,initial={'typedoc':1})

    return render(request,'trade/CurrentReceiptDoc.html',{'title': 'Новый документ (Поступление)','form':form,
    'currenttable':CurrentTable,'currentdoc':CurrentDoc,'docheader':docheader})




# Начальные остатки новый документ:
def CreateInitialDoc(request):
    if request.method == 'POST':
        form = InitialDocForm(request.POST)
        form2 = InitialTableForm(request.POST)
        if form.is_valid() and form2.is_valid():

            formDoc=form.save()
            formTable=form2.save(commit=False)
            formTable.iddoc_id=formDoc.id
            formTable.save()

            Doc.objects.filter(id=formDoc.id).update(buytotal=formTable.buytotal,saletotal=formTable.saletotal)
            url = reverse('UpdateInitialDoc', kwargs={'pk': formDoc.id})
            return HttpResponseRedirect(url)
    else:
        form = InitialDocForm(initial={'typedoc':2,'dealer':13})
        form2 = InitialTableForm(initial={'typedoc': 2 })
    return render(request,'trade/CreateInitialDoc.html',{'title': 'Новый документ (Начальные остатки)','form':form,'form2':form2})

# Редактирование докмента начальных остатков

def UpdateInitialDoc(request,pk):
    CurrentDoc=Doc.objects.get(pk=pk)
    CurrentTable=DocJurnal.objects.filter(iddoc_id=pk)
    if request.method == 'POST':
        docheader = InitialDocForm(request.POST)
        if 'FormHeader' in request.POST:
            print(request.POST)
            print('YES')
            CurrentDoc.nomerdoc = request.POST.get("nomerdoc")
            CurrentDoc.datadoc = request.POST.get("datadoc")
            CurrentDoc.save()
            return redirect('InitialDoc')
        form = InitialTableForm(request.POST)


        if form.is_valid():
            formTable = form.save(commit=False)
            formTable.iddoc_id = CurrentDoc.id
            formTable.save()
            sum_buy = DocJurnal.objects.filter(iddoc_id=pk).aggregate(Sum('buytotal'))
            sum_sale = DocJurnal.objects.filter(iddoc_id=pk).aggregate(Sum('saletotal'))
            Doc.objects.filter(id=pk).update(buytotal=sum_buy['buytotal__sum'], saletotal=sum_sale['saletotal__sum'])
            if sum_sale['saletotal__sum'] == None and sum_buy['buytotal__sum'] == None:
                Doc.objects.filter(id=pk).update(buytotal=0.00, saletotal=0.00)
            url = reverse('UpdateInitialDoc', kwargs={'pk': CurrentDoc.id})
            return HttpResponseRedirect(url)
    else:
        CurrentDoc = Doc.objects.get(pk=pk)
        CurrentTable = DocJurnal.objects.filter(iddoc_id=pk)
        sum_buy = DocJurnal.objects.filter(iddoc_id=pk).aggregate(Sum('buytotal'))
        sum_sale = DocJurnal.objects.filter(iddoc_id=pk).aggregate(Sum('saletotal'))
        Doc.objects.filter(id=pk).update(buytotal=sum_buy['buytotal__sum'],saletotal=sum_sale['saletotal__sum'])
        if sum_sale['saletotal__sum'] == None and sum_buy['buytotal__sum'] == None:
            Doc.objects.filter(id=pk).update(buytotal=0.00, saletotal=0.00)
        form = InitialTableForm(initial={'typedoc': 2,'iddoc_id':CurrentDoc.id })

        docheader = InitialDocForm(instance=CurrentDoc,initial={'typedoc':2,'dealer':13})

    return render(request,'trade/CurrentInitialDoc.html',{'title': 'Новый документ (Начальные остатки)','form':form,
    'currenttable':CurrentTable,'currentdoc':CurrentDoc,'docheader':docheader})
# Редактирование документа поступление

def UpdateReceiptDoc(request,pk):
    CurrentDoc=Doc.objects.get(pk=pk)
    CurrentTable=DocJurnal.objects.filter(iddoc_id=pk)
    if request.method == 'POST':
        docheader = ReceiptDocForm(request.POST)
        if 'FormHeader' in request.POST:
            print(request.POST)
            print('YES')
            CurrentDoc.nomerdoc = request.POST.get("nomerdoc")
            CurrentDoc.datadoc = request.POST.get("datadoc")
            dealer=Saler.objects.get(id=request.POST.get("dealer"))
            CurrentDoc.dealer=dealer
            CurrentDoc.save()
            return redirect('ReceiptDoc')
        form = ReceiptTableForm(request.POST)


        if form.is_valid():
            formTable = form.save(commit=False)
            formTable.iddoc_id = CurrentDoc.id
            formTable.save()
            sum_buy = DocJurnal.objects.filter(iddoc_id=pk).aggregate(Sum('buytotal'))
            sum_sale = DocJurnal.objects.filter(iddoc_id=pk).aggregate(Sum('saletotal'))
            Doc.objects.filter(id=pk).update(buytotal=sum_buy['buytotal__sum'], saletotal=sum_sale['saletotal__sum'])
            if sum_sale['saletotal__sum'] == None and sum_buy['buytotal__sum'] == None:
                Doc.objects.filter(id=pk).update(buytotal=0.00, saletotal=0.00)
            url = reverse('UpdateReceiptDoc', kwargs={'pk': CurrentDoc.id})
            return HttpResponseRedirect(url)
    else:
        CurrentDoc = Doc.objects.get(pk=pk)
        CurrentTable = DocJurnal.objects.filter(iddoc_id=pk)
        sum_buy = DocJurnal.objects.filter(iddoc_id=pk).aggregate(Sum('buytotal'))
        sum_sale = DocJurnal.objects.filter(iddoc_id=pk).aggregate(Sum('saletotal'))
        Doc.objects.filter(id=pk).update(buytotal=sum_buy['buytotal__sum'],saletotal=sum_sale['saletotal__sum'])
        if sum_sale['saletotal__sum'] == None and sum_buy['buytotal__sum'] == None:
            Doc.objects.filter(id=pk).update(buytotal=0.00, saletotal=0.00)
        form = ReceiptTableForm(initial={'typedoc': 1,'iddoc_id':CurrentDoc.id })

        docheader = ReceiptDocForm(instance=CurrentDoc,initial={'typedoc':1})

    return render(request,'trade/CurrentReceiptDoc.html',{'title': 'Новый документ (Поступление)','form':form,
    'currenttable':CurrentTable,'currentdoc':CurrentDoc,'docheader':docheader})

def UpdateDocString(request,pk):
    id = DocJurnal.objects.get(pk=pk)
    CurrentTable = DocJurnal.objects.filter(iddoc_id=id.iddoc_id)
    CurrentDoc = Doc.objects.get(pk=id.iddoc_id)
    if request.method == 'POST':
        docheader = InitialDocForm(request.POST)
        if 'FormHeader' in request.POST:
            print(request.POST)
            print('YES')
            CurrentDoc.nomerdoc = request.POST.get("nomerdoc")
            CurrentDoc.datadoc = request.POST.get("datadoc")
            CurrentDoc.save()
            return redirect('InitialDoc')
        form = InitialTableForm(request.POST)
        if form.is_valid():
            print(request.POST)
            CurrentString=DocJurnal.objects.get(pk=pk)
            CurrentString.title_id=request.POST.get("title")
            CurrentString.volume=request.POST.get("volume")
            CurrentString.percent = request.POST.get("percent")
            CurrentString.saleprice = request.POST.get("saleprice")
            CurrentString.buyprice = request.POST.get("buyprice")
            CurrentString.buytotal = request.POST.get("buytotal")
            CurrentString.saletotal = request.POST.get("saletotal")

            CurrentString.save()
            sum_buy = DocJurnal.objects.filter(iddoc_id=id.iddoc_id).aggregate(Sum('buytotal'))
            sum_sale = DocJurnal.objects.filter(iddoc_id=id.iddoc_id).aggregate(Sum('saletotal'))

            Doc.objects.filter(id=id.iddoc_id).update(buytotal=sum_buy['buytotal__sum'], saletotal=sum_sale['saletotal__sum'])
            if sum_sale['saletotal__sum'] == None and sum_buy['buytotal__sum'] == None:
                Doc.objects.filter(id=pk).update(buytotal=0.00, saletotal=0.00)
            url = reverse('UpdateInitialDoc', kwargs={'pk': CurrentDoc.id})
            return HttpResponseRedirect(url)
    else:
        id = DocJurnal.objects.get(pk=pk)
        CurrentTable = DocJurnal.objects.filter(iddoc_id=id.iddoc_id)
        CurrentDoc = Doc.objects.get(pk=id.iddoc_id)
        sum_buy = DocJurnal.objects.filter(iddoc_id=id.iddoc_id).aggregate(Sum('buytotal'))
        sum_sale = DocJurnal.objects.filter(iddoc_id=id.iddoc_id).aggregate(Sum('saletotal'))
        Doc.objects.filter(id=id.iddoc_id).update(buytotal=sum_buy['buytotal__sum'], saletotal=sum_sale['saletotal__sum'])
        if sum_sale['saletotal__sum'] == None and sum_buy['buytotal__sum'] == None:
            Doc.objects.filter(id=id.iddoc_id).update(buytotal=0.00, saletotal=0.00)
        form = InitialTableForm(instance=id)
        docheader = InitialDocForm(instance=CurrentDoc, initial={'typedoc': 2, 'dealer': 13})
    return render(request, 'trade/UpdateInitialDoc.html', {'title': 'Новый документ (Начальные остатки)', 'form': form,
                                                            'currenttable': CurrentTable, 'currentdoc': CurrentDoc,
                                                            'docheader': docheader})

# Редактирование строки приходного документа

def UpdateReceiptDocString(request,pk):
    id = DocJurnal.objects.get(pk=pk)
    CurrentTable = DocJurnal.objects.filter(iddoc_id=id.iddoc_id)
    CurrentDoc = Doc.objects.get(pk=id.iddoc_id)
    if request.method == 'POST':
        docheader = ReceiptDocForm(request.POST)
        if 'FormHeader' in request.POST:
            print(request.POST)
            CurrentDoc.nomerdoc = request.POST.get("nomerdoc")
            CurrentDoc.datadoc = request.POST.get("datadoc")
            dealer = Saler.objects.get(id=request.POST.get("dealer"))
            CurrentDoc.dealer = dealer

            CurrentDoc.save()
            return redirect('ReceiptDoc')
        form = ReceiptTableForm(request.POST)
        if form.is_valid():
            print(request.POST)
            CurrentString=DocJurnal.objects.get(pk=pk)
            CurrentString.title_id=request.POST.get("title")
            CurrentString.volume=request.POST.get("volume")
            CurrentString.percent = request.POST.get("percent")
            CurrentString.saleprice = request.POST.get("saleprice")
            CurrentString.buyprice = request.POST.get("buyprice")
            CurrentString.buytotal = request.POST.get("buytotal")
            CurrentString.saletotal = request.POST.get("saletotal")

            CurrentString.save()
            sum_buy = DocJurnal.objects.filter(iddoc_id=id.iddoc_id).aggregate(Sum('buytotal'))
            sum_sale = DocJurnal.objects.filter(iddoc_id=id.iddoc_id).aggregate(Sum('saletotal'))

            Doc.objects.filter(id=id.iddoc_id).update(buytotal=sum_buy['buytotal__sum'], saletotal=sum_sale['saletotal__sum'])
            if sum_sale['saletotal__sum'] == None and sum_buy['buytotal__sum'] == None:
                Doc.objects.filter(id=pk).update(buytotal=0.00, saletotal=0.00)
            url = reverse('UpdateReceiptDoc', kwargs={'pk': CurrentDoc.id})
            return HttpResponseRedirect(url)
    else:
        id = DocJurnal.objects.get(pk=pk)
        CurrentTable = DocJurnal.objects.filter(iddoc_id=id.iddoc_id)
        CurrentDoc = Doc.objects.get(pk=id.iddoc_id)
        sum_buy = DocJurnal.objects.filter(iddoc_id=id.iddoc_id).aggregate(Sum('buytotal'))
        sum_sale = DocJurnal.objects.filter(iddoc_id=id.iddoc_id).aggregate(Sum('saletotal'))
        Doc.objects.filter(id=id.iddoc_id).update(buytotal=sum_buy['buytotal__sum'], saletotal=sum_sale['saletotal__sum'])
        if sum_sale['saletotal__sum'] == None and sum_buy['buytotal__sum'] == None:
            Doc.objects.filter(id=id.iddoc_id).update(buytotal=0.00, saletotal=0.00)
        form = ReceiptTableForm(instance=id)
        docheader = ReceiptDocForm(instance=CurrentDoc, initial={'typedoc': 1})
    return render(request, 'trade/UpdateReceiptDoc.html', {'title': 'Новый документ (Поступление)', 'form': form,
                                                            'currenttable': CurrentTable, 'currentdoc': CurrentDoc,
                                                            'docheader': docheader})


def DeleteInitialDoc(request,pk):
    CurrentDoc = Doc.objects.get(pk=pk)
    CurrentTable = DocJurnal.objects.filter(iddoc_id=pk)
    return render(request,'trade/DeleteInitialDoc.html',{'title': 'Удаление документа (Начальные остатки)',
    'currenttable':CurrentTable,'currentdoc':CurrentDoc,})

def DeleteReceiptDoc(request,pk):
    CurrentDoc = Doc.objects.get(pk=pk)
    CurrentTable = DocJurnal.objects.filter(iddoc_id=pk)
    return render(request,'trade/DeleteReceiptDoc.html',{'title': 'Удаление документа (Поступление)',
    'currenttable':CurrentTable,'currentdoc':CurrentDoc,})

def DeleteDoc(request,pk):
    CurrentDoc = Doc.objects.get(pk=pk)
    CurrentDoc.delete()
    return redirect('InitialDoc')
def DeleteRDoc(request,pk):
    CurrentDoc = Doc.objects.get(pk=pk)
    CurrentDoc.delete()
    return redirect('ReceiptDoc')
# Удаление строки из документа
def DeleteDocSting(request,pk):
    deleteString= DocJurnal.objects.get(pk=pk)
    iddoc=deleteString.iddoc_id
    deleteString.delete()
    sum_buy = DocJurnal.objects.filter(iddoc_id=iddoc).aggregate(Sum('buytotal'))
    sum_sale = DocJurnal.objects.filter(iddoc_id=iddoc).aggregate(Sum('saletotal'))
    Doc.objects.filter(id=iddoc).update(buytotal=sum_buy['buytotal__sum'], saletotal=sum_sale['saletotal__sum'])
    if sum_sale['saletotal__sum']==None and sum_buy['buytotal__sum'] == None:
        Doc.objects.filter(id=iddoc).update(buytotal=0.00, saletotal=0.00)


    return redirect('UpdateInitialDoc',iddoc)

# Удаление записи из документа Приход
def DeleteRDocSting(request,pk):
    deleteString= DocJurnal.objects.get(pk=pk)
    iddoc=deleteString.iddoc_id
    deleteString.delete()
    sum_buy = DocJurnal.objects.filter(iddoc_id=iddoc).aggregate(Sum('buytotal'))
    sum_sale = DocJurnal.objects.filter(iddoc_id=iddoc).aggregate(Sum('saletotal'))
    Doc.objects.filter(id=iddoc).update(buytotal=sum_buy['buytotal__sum'], saletotal=sum_sale['saletotal__sum'])
    if sum_sale['saletotal__sum']==None and sum_buy['buytotal__sum'] == None:
        Doc.objects.filter(id=iddoc).update(buytotal=0.00, saletotal=0.00)


    return redirect('UpdateReceiptDoc',iddoc)

# Создание записей в справочниках
def Create(request, TableName):
    if TableName == 'Unit':
        title = 'Единицы измерения'
    if TableName == 'Saler':
        title = 'Поставщики'
    if TableName == 'Pay':
        title = 'Виды оплаты'
    if TableName == 'Customer':
        title = 'Организации'
    data = eval(TableName).objects.all()

    FormName = eval(TableName + 'Form')
    if request.method == 'POST':
        form = FormName(request.POST)
        if form.is_valid():
            try:
                form.save()
                form = FormName()
                return redirect('Create', TableName)
            except:
                form.add_error(None, 'Ошибка добавления ')
    else:
        form = FormName()
    return render(request, 'trade/Create.html', {'title': title, 'form': form, 'data': data, 'tableName': TableName})

# Удаление из справочника
def Delete(request, TableName, pk):
    if TableName == 'Unit':
        title = 'Единицы измерения'
    if TableName == 'Saler':
        title = 'Поставщики'
    if TableName == 'Pay':
        title = 'Виды оплаты'
    if TableName == 'Customer':
        title = 'Организации'
    unit = eval(TableName).objects.get(pk=pk)
    data = eval(TableName).objects.all()

    FormName = eval(TableName + 'Form')
    if request.method == 'POST':
        form = FormName(request.POST, instance=unit)
        if form.is_valid():
            try:
                unit.delete()
                form = FormName()
                return redirect('Create', TableName)
            except:
                form.add_error(None, 'Ошибка добавления ')
    else:
        form = FormName(instance=unit)
    return render(request, 'trade/Delete.html', {'title': title, 'form': form, 'data': data, 'tableName': TableName})

# Обновление справочника
def Update(request, TableName, pk):
    if TableName == 'Unit':
        title = 'Единицы измерения'
    if TableName == 'Saler':
        title = 'Поставщики'
    if TableName == 'Pay':
        title = 'Виды оплаты'
    if TableName == 'Customer':
        title = 'Организации'
    unit = eval(TableName).objects.get(pk=pk)
    data = eval(TableName).objects.all()

    FormName = eval(TableName + 'Form')
    if request.method == 'POST':
        form = FormName(request.POST, instance=unit)
        if form.is_valid():
            try:
                unit.save()
                form = FormName()
                return redirect('Create', TableName)
            except:
                form.add_error(None, 'Ошибка обновления ')
    else:
        form = FormName(instance=unit)
    return render(request, 'trade/Update.html', {'title': title, 'form': form, 'data': data, 'tableName': TableName})

def CategoryPage(request):
    data=Category.objects.all()
    form = CategoryForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('Category')
    else:
        form = CategoryForm()
        data = Category.objects.all()
        context = {'data': data, 'form': form,'title':'Категории'}
        return render(request, "trade/Category.html", context)

def UpdateCategory(request,pk):
    data = Category.objects.all()
    unit = Category.objects.get(pk=pk)
    form = CategoryForm(request.POST, request.FILES,instance=unit)
    if form.is_valid():
        form.save()
        return redirect('Category')
    else:
        form = CategoryForm(instance=unit)
        data = Category.objects.all()
        context = {'data': data, 'form': form, 'title': 'Категории'}
        return render(request, "trade/UpdateCategory.html", context)

def DeleteCategory(request,pk):
    data = Category.objects.all()
    unit = Category.objects.get(pk=pk)
    form = CategoryForm(request.POST, request.FILES,instance=unit)
    if form.is_valid():
        unit.delete()
        return redirect('Category')
    else:
        form = CategoryForm(instance=unit)
        data = Category.objects.all()
        context = {'data': data, 'form': form, 'title': 'Категории'}
        return render(request, "trade/DeleteCategory.html", context)

# Вывод товаров
def Goods(request):
    category=Category.objects.filter(photos__isnull=False).distinct()
    unit=Unit.objects.all()
    good=Good.objects.all()
    title='Номенклатура'
    if request.method == 'POST':
        form = GoodForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                form = GoodForm()
                return redirect('Good')
            except:
                form.add_error(None, 'Ошибка добавления ')
    else:
        form = GoodForm()
    return render(request, 'trade/Good.html', {'title': title, 'form': form, 'category': category, 'unit': unit,'goods':good})

# Обновление товаров
def UpdateGoods(request,pk):
    category=Category.objects.filter(photos__isnull=False).distinct()
    unit=Unit.objects.all()
    good=Good.objects.all()
    goodunit=Good.objects.get(pk=pk)
    title='Номенклатура'
    if request.method == 'POST':
        form = GoodForm(request.POST,instance=goodunit)
        if form.is_valid():
            try:
                form.save()
                form = GoodForm()
                return redirect('Good')
            except:
                form.add_error(None, 'Ошибка добавления ')
    else:
        form = GoodForm(instance=goodunit)
    return render(request, 'trade/UpdateGood.html', {'title': title, 'form': form, 'category': category, 'unit': unit,'goods':good})

# Удаление товаров
def DeleteGoods(request,pk):
    category=Category.objects.filter(photos__isnull=False).distinct()
    unit=Unit.objects.all()
    good=Good.objects.all()
    goodunit=Good.objects.get(pk=pk)
    title='Номенклатура'
    if request.method == 'POST':
        form = GoodForm(request.POST,instance=goodunit)
        if form.is_valid():
            try:
                goodunit.delete()
                form = GoodForm()
                return redirect('Good')
            except:
                form.add_error(None, 'Ошибка добавления ')
    else:
        form = GoodForm(instance=goodunit)
    return render(request, 'trade/DeleteGood.html', {'title': title, 'form': form, 'category': category, 'unit': unit,'goods':good})

# Получение товаров и категорий в наличии
def GetData(request,msg=''):
    unfilter=DocJurnal.objects.values_list('title_id__title','saleprice','title_id__unit__title','title_id__category__title','title_id','title_id__category','title_id__category__photo').distinct()
    TempGood.objects.all().delete()
    for i in unfilter:
        prihod = DocJurnal.objects.filter(title_id=i[4],saleprice=i[1],typedoc=1).aggregate(summa=Sum('volume'))
        ost = DocJurnal.objects.filter(title_id=i[4], saleprice=i[1], typedoc=2).aggregate(summa=Sum('volume'))
        spis = DocJurnal.objects.filter(title_id=i[4], saleprice=i[1], typedoc=3).aggregate(summa=Sum('volume'))
        nal = DocJurnal.objects.filter(title_id=i[4], saleprice=i[1], typedoc=4).aggregate(summa=Sum('volume'))
        term = DocJurnal.objects.filter(title_id=i[4], saleprice=i[1], typedoc=5).aggregate(summa=Sum('volume'))
        otmena = DocJurnal.objects.filter(title_id=i[4], saleprice=i[1], typedoc=6).aggregate(summa=Sum('volume'))

        ost['summa']=0.0 if ost['summa'] == None else ost['summa']
        prihod['summa'] = 0.0 if prihod['summa'] == None else prihod['summa']
        spis['summa'] = 0.0 if spis['summa'] == None else spis['summa']
        nal['summa'] = 0.0 if nal['summa'] == None else nal['summa']
        term['summa'] = 0.0 if term['summa'] == None else term['summa']
        otmena['summa'] = 0.0 if otmena['summa'] == None else otmena['summa']
        kolv=ost['summa']+prihod['summa']-spis['summa']-nal['summa']-term['summa']+otmena['summa']

        if TempGood.objects.filter(title=i[0],price=i[1]).exists()==False:
            if kolv != 0:
                toPage = TempGood()
                toPage.idgood =i[4]
                toPage.title=i[0]
                toPage.price=i[1]
                toPage.unit=i[2]
                toPage.category=i[3]
                toPage.photo=i[6]
                toPage.kolvo=kolv
                toPage.save()
                toPage.save()
    tmpGood=TempGood.objects.all()
    uncategory=TempGood.objects.values_list('category','photo').distinct()
    return render(request,'trade/GetTradeCategory2.html',{'tmpGood':tmpGood,'uncategory':sorted(uncategory)})

def Proba(request,pk):
    return GetData(request)

def GoodToCheck(request,pk,price):

    dict_key=str(pk+price)

    toCheck[dict_key] ={
        'title':unDict[dict_key][0],
        'title_id':unDict[dict_key][1],
        'price':unDict[dict_key][2],
        'category':unDict[dict_key][3],
        'unit':unDict[dict_key][4],
        'ostatok':unDict[dict_key][6],
        'volume': 1,
         }
    toCheck[dict_key]['total']=toCheck[dict_key]['price']*toCheck[dict_key]['volume']


    return GetData(request)

def DeleteCheckRecord(request,pk,price):
    del toCheck[str(pk)+str(price)]
    return GetData(request)

def IncVolume(request,pk,price):
    dict_key = str(pk + price)
    print(toCheck[dict_key])
    if toCheck[dict_key]['volume'] < toCheck[dict_key]['ostatok']:
       toCheck[dict_key]['volume'] +=1
       toCheck[dict_key]['total']=toCheck[dict_key]['price']*toCheck[dict_key]['volume']
    return GetData(request)

def DecVolume(request,pk,price):
    dict_key = str(pk + price)
    if toCheck[dict_key]['volume'] !=1:
       toCheck[dict_key]['volume'] -=1
       toCheck[dict_key]['total']=toCheck[dict_key]['price']*toCheck[dict_key]['volume']
    #curr = TempCheck.objects.get(id=pk)
    #if curr.volume !=1:
     #  curr.volume=curr.volume-1
      # curr.total=curr.volume*curr.price
      # curr.save()
    return GetData(request)

def DeleteCheck(request):
    toCheck.clear()
    return GetData(request,'Оплата отменена...')


def DeleteCheck4(request):
    toCheck.clear()
    return GetData(request,'Оплата проведена!')

def CashCheck(request,mode):
# меняем номер чека
    nomer=Check.objects.get(pk=1)
    nomer.nomercheck=nomer.nomercheck+1
    nomer.save()
    #print(toCheck)
    tmp = list(toCheck.keys())
    Summa = 0
    for i in tmp:
        Summa = Summa + (toCheck[i]['total'])
    checkSumma = Summa

    #print(checkSumma)
# записываем чек в журнал документов
    #tempcheck=TempCheck.objects.aggregate(Sum('total'))
    tempDoc=Doc()
    tempDoc.typedoc=TypeDoc.objects.get(pk=mode)
    tempDoc.datadoc=datetime.date.today()
    tempDoc.saletotal=checkSumma
    tempDoc.nomerdoc=nomer.nomercheck
    tempDoc.dealer_id=13
    if request.user.is_authenticated:
        tempDoc.user=request.user.last_name
    tempDoc.save()
# записываем позиции товаров в общий журнал
    tdoc=Doc.objects.filter(typedoc=mode).last()
    for tcheck1 in toCheck.values():
       tgood=Good.objects.get(id=tcheck1['title_id'])
       tjurnal=DocJurnal()
       tjurnal.title_id=tgood.id
       tjurnal.volume=tcheck1['volume']
       tjurnal.buyprice=0
       tjurnal.buytotal=0
       tjurnal.percent=0
       tjurnal.saleprice=tcheck1['price']
       tjurnal.saletotal=tcheck1['total']
       tjurnal.iddoc_id=tdoc.id
       tjurnal.typedoc=mode
       tjurnal.nomercheck=tdoc.nomerdoc
       if request.user.is_authenticated:
           tjurnal.user = request.user.last_name
       tjurnal.save()

    return DeleteCheck4(request)



def CheckJurnal(request):
    daysumcash=0
    uniqdate=[]
    uniqsum={}
    dateArray=[]
    checkitem=DocJurnal.objects.exclude(typedoc=1).exclude(typedoc=2).exclude(typedoc=3)
    checkdoc=Doc.objects.exclude(typedoc=1).exclude(typedoc=2).exclude(typedoc=3).order_by('-datadoc')

    for item in checkdoc:
        if not item.datadoc in uniqdate:
            uniqdate.append(item.datadoc)

    for undata in uniqdate:

        if undata in uniqdate:

            cashsum = Doc.objects.filter(typedoc=4).order_by('-datadoc').filter(datadoc=undata).aggregate(Sum('saletotal'))
            cashterm = Doc.objects.filter(typedoc=5).order_by('-datadoc').filter(datadoc=undata).aggregate(
                Sum('saletotal'))
            dateArray.append(undata)
            if cashsum['saletotal__sum'] == None:
                cashsum['saletotal__sum']=0
            if cashterm['saletotal__sum'] == None:
                cashterm['saletotal__sum']=0
            uniqsum[undata]={
                'nal':float(cashsum['saletotal__sum']),
                'bank':float(cashterm['saletotal__sum'])}



    listsum=[[key,value] for key,value in uniqsum.items()]
    print(uniqsum)
    context = {'checkitem': checkitem, 'checkdoc': checkdoc,'uniqdate':uniqdate,'uniqsum':uniqsum,'dateArray':dateArray,'listsum':listsum}

    return render(request,'trade/CheckJurnal.html',context)

def loginUser(request):
    if request.method=='POST':
        form=UserLoginForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('home')
    else:
        form=UserLoginForm()
    return render(request,'trade/loginUser.html',{"form":form})

def UserOut(request):
    logout(request)
    return redirect('loginUser')
