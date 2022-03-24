from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .forms import *
from django.db.models import Sum
import datetime
uniqueGood={}
maxvolume=None

def main(request):
    return render(request, 'trade/main.html', {'title': 'Главная страница'})

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

def GetData(request,message=''):
    unArray= []

    uniq=DocJurnal.objects.all()


    for item in uniq:
        s=str(item.title_id),item.saleprice
        if not s in unArray:
            unArray.append(s)
    for i in unArray:
        a=int(i[0])
        b=i[1]

        ostatok=DocJurnal.objects.filter(title_id=a).filter(saleprice=b).filter(typedoc=2).aggregate(Sum('volume'))
        print(ostatok)

    print(unArray)
    print(len(unArray))
    print(len(uniq))
    goodcheck=TempCheck.objects.all()
    data=DocJurnal.objects.order_by('title')
    categories=Category.objects.order_by('title').filter(photos__isnull=False).distinct()
    uniqueCat= {}
    unsortedCat={}
    for good in data:
        name = good.title
        price=good.saleprice
        goodid = good.title.id
        category=good.title.category.title
        category_id=good.title.category.id
        prihod=DocJurnal.objects.filter(title=good.title).filter(typedoc=1).filter(saleprice=price).aggregate(Sum('volume'))
        ostatok = DocJurnal.objects.filter(title=good.title).filter(typedoc=2).filter(saleprice=price).aggregate(Sum('volume'))
        spisanie = DocJurnal.objects.filter(title=good.title).filter(typedoc=3).filter(saleprice=price).aggregate(Sum('volume'))
        cash=DocJurnal.objects.filter(title=good.title).filter(typedoc=4).filter(saleprice=price).aggregate(Sum('volume'))
        term = DocJurnal.objects.filter(title=good.title).filter(typedoc=5).filter(saleprice=price).aggregate(
            Sum('volume'))
        oplata = TempCheck.objects.all().aggregate(Sum('total'))
        checkoplata=(oplata['total__sum'])
        uniqid=str(name)+str(price)
        if term['volume__sum'] == None:
          term['volume__sum']=0
        if prihod['volume__sum'] == None:
          prihod['volume__sum']=0
        if ostatok['volume__sum'] == None:
          ostatok['volume__sum']=0
        if spisanie['volume__sum'] == None:
          spisanie['volume__sum']=0
        if cash['volume__sum'] == None:
          cash['volume__sum']=0
        rest=ostatok['volume__sum'] + prihod['volume__sum'] - spisanie['volume__sum'] - cash['volume__sum'] - term['volume__sum']
        unit2 = Good.objects.get(id=goodid)
        titleunit = unit2.unit.title
        cellprice=int(price)
        uniqueGood[uniqid] = name, category, price, rest, category_id, titleunit,goodid,cellprice
        unsortedCat[category_id]=category
        uniqueCat=sorted(unsortedCat.values())
    context={'data':data,'categories':categories,'uniqueCat':uniqueCat,'uniqueGood':uniqueGood,'goodcheck':goodcheck,'checkoplata':checkoplata,'checkstring':message,
             'title':'Торговля'}
    return render(request,'trade/GetTradeCategory2.html',context)

def GoodToCheck(request,pk,price):
    cureentrecord=Good.objects.get(id=pk)
    fromjurnal=DocJurnal.objects.filter(title_id=pk).filter(saleprice=price)

    for item in fromjurnal:
        price=item.saleprice
        uniqkey=str(item.title)+str(item.saleprice)
        maxvolume = uniqueGood[uniqkey]
    try:
        temprecord=TempCheck.objects.get(idgood=pk,price=price)
        temprecord.volume = temprecord.volume
        temprecord.total = temprecord.price * temprecord.volume
        temprecord.save()
    except ObjectDoesNotExist:
        temprecord=TempCheck()
        temprecord.idgood=pk
        temprecord.title=cureentrecord.title
        temprecord.unit=cureentrecord.unit.title
        temprecord.volume=1
        temprecord.maxvolume=maxvolume[3]
        temprecord.price=price
        temprecord.total=temprecord.price*temprecord.volume
        temprecord.save()
    return GetData(request,'')

def DeleteCheckRecord(request,pk):
    curr=TempCheck.objects.get(id=pk)
    print(curr.title)
    curr.delete()
    return GetData(request,'')

def IncVolume(request,pk):
    curr = TempCheck.objects.get(id=pk)
    if curr.volume < curr.maxvolume:
        curr.volume=curr.volume+1

    curr.total=curr.volume*curr.price
    curr.save()
    return GetData(request,'')

def DecVolume(request,pk):
    curr = TempCheck.objects.get(id=pk)
    if curr.volume !=1:
       curr.volume=curr.volume-1
       curr.total=curr.volume*curr.price
       curr.save()
    return GetData(request,'')

def DeleteCheck(request):
    items=TempCheck.objects.all()
    items.delete()
    return GetData(request,'Продажа отменена')
def DeleteCheck4(request):
    items=TempCheck.objects.all()
    items.delete()
    return GetData(request,'Чек проведен')

def CashCheck(request):
# меняем номер чека
    nomer=Check.objects.get(pk=1)
    nomer.nomercheck=nomer.nomercheck+1
    nomer.save()
# записываем чек в журнал документов
    tempcheck=TempCheck.objects.aggregate(Sum('total'))
    tempDoc=Doc()
    tempDoc.typedoc=TypeDoc.objects.get(pk=4)
    tempDoc.datadoc=datetime.date.today()
    tempDoc.saletotal=tempcheck['total__sum']
    tempDoc.nomerdoc=nomer.nomercheck
    tempDoc.dealer_id=13
    tempDoc.save()
# записываем позиции товаров в общий журнал
    tdoc=Doc.objects.filter(typedoc=4).last()
    print(tdoc.id)
# вот здесь цикл:
    tcheck=TempCheck.objects.all()
    for tcheck1 in tcheck:
        print(tcheck1.title)
        tgood=Good.objects.get(id=tcheck1.idgood)
        tjurnal=DocJurnal()
        tjurnal.title_id=tgood.id
        tjurnal.volume=tcheck1.volume
        tjurnal.buyprice=0
        tjurnal.buytotal=0
        tjurnal.percent=0
        tjurnal.saleprice=tcheck1.price
        tjurnal.saletotal=tcheck1.total
        tjurnal.iddoc_id=tdoc.id
        tjurnal.typedoc=4
        tjurnal.nomercheck=tdoc.nomerdoc
        tjurnal.save()
    return DeleteCheck4(request)
def TerminalCheck(request):
# меняем номер чека
    nomer=Check.objects.get(pk=1)
    nomer.nomercheck=nomer.nomercheck+1
    nomer.save()
# записываем чек в журнал документов
    tempcheck=TempCheck.objects.aggregate(Sum('total'))
    tempDoc=Doc()
    tempDoc.typedoc=TypeDoc.objects.get(pk=5)
    tempDoc.datadoc=datetime.date.today()
    tempDoc.saletotal=tempcheck['total__sum']
    tempDoc.nomerdoc=nomer.nomercheck
    tempDoc.dealer_id=13
    tempDoc.save()
# записываем позиции товаров в общий журнал
    tdoc=Doc.objects.filter(typedoc=5).last()
    print(tdoc.id)
# вот здесь цикл:
    tcheck=TempCheck.objects.all()
    for tcheck1 in tcheck:
        print(tcheck1.title)
        tgood=Good.objects.get(id=tcheck1.idgood)
        tjurnal=DocJurnal()
        tjurnal.title_id=tgood.id
        tjurnal.volume=tcheck1.volume
        tjurnal.buyprice=0
        tjurnal.buytotal=0
        tjurnal.percent=0
        tjurnal.saleprice=tcheck1.price
        tjurnal.saletotal=tcheck1.total
        tjurnal.iddoc_id=tdoc.id
        tjurnal.typedoc=5
        tjurnal.nomercheck=tdoc.nomerdoc
        tjurnal.save()
    return DeleteCheck4(request)

def CheckJurnal(request):
    uniqdate=[]
    checkitem=DocJurnal.objects.exclude(typedoc=1).exclude(typedoc=2).exclude(typedoc=3)
    checkdoc=Doc.objects.exclude(typedoc=1).exclude(typedoc=2).exclude(typedoc=3).order_by('-datadoc')

    for item in checkdoc:
        if not item.datadoc in uniqdate:
            uniqdate.append(item.datadoc)

    context = {'checkitem': checkitem, 'checkdoc': checkdoc,'uniqdate':uniqdate}
    return render(request,'trade/CheckJurnal.html',context)