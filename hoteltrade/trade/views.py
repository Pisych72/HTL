from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *
from .forms import *
from django.db.models import Sum


def main(request):
    return render(request, 'trade/main.html', {'title': 'Главная страница'})

def listpage(request):
    return render(request, 'trade/listpage.html', {'title': 'Справочники'})
def DocPage(request):
    return render(request, 'trade/DocPage.html', {'title': 'Документы'})
def InitialDoc(request):
    InitialDoc=Doc.objects.filter(typedoc=2).order_by('-datadoc')
    return render(request, 'trade/InitialDocs.html', {'title': 'Ввод начальных остатков','doc':InitialDoc})

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
#global sum_buy
#global sum_sale
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

def DeleteInitialDoc(request,pk):
    CurrentDoc = Doc.objects.get(pk=pk)
    CurrentTable = DocJurnal.objects.filter(iddoc_id=pk)
    return render(request,'trade/DeleteInitialDoc.html',{'title': 'Удаление документа (Начальные остатки)',
    'currenttable':CurrentTable,'currentdoc':CurrentDoc,})

def DeleteDoc(request,pk):
    CurrentDoc = Doc.objects.get(pk=pk)
    CurrentDoc.delete()
    return redirect('InitialDoc')

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

