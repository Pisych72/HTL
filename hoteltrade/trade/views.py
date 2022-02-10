from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .forms import *


def main(request):
    return render(request, 'trade/main.html', {'title': 'Главная страница'})

def listpage(request):
    return render(request, 'trade/listpage.html', {'title': 'Справочники'})
def DocPage(request):
    return render(request, 'trade/DocPage.html', {'title': 'Документы'})
def InitialDoc(request):

    return render(request, 'trade/InitialDocs.html', {'title': 'Ввод начальных остатков'})
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

