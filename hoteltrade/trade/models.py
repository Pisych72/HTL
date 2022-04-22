from django.db import models
# Единицы измерения
class Unit(models.Model):
    title = models.CharField(max_length=100,verbose_name='Наименование')
    def __str__(self):
        return self.title
    class Meta:
        verbose_name='Единица измерения'
        verbose_name_plural='Единицы измерения'
        ordering=['title',]
# Категории
class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование')
    photo = models.ImageField(upload_to='photo',blank=True)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name='Категория'
        verbose_name_plural='Категории'
        ordering=['title',]

#Виды оплаты
class Pay(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование')

#Операции
class Operation(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование')

#Поставщики
class Saler(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование')
    def __str__(self):
        return self.title
    class Meta:
        verbose_name='Поставщик'
        verbose_name_plural='Поставщики'
        ordering=['title',]

# Организации
class Customer(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование')
    def __str__(self):
        return self.title
    class Meta:
        verbose_name='Организация'
        verbose_name_plural='Организации'
        ordering=['title',]
# Товары
class Good(models.Model):
    title=models.CharField(max_length=100,verbose_name='Наименование')
    unit=models.ForeignKey(Unit,on_delete=models.PROTECT,verbose_name='Единица измерения')
    category=models.ForeignKey(Category,on_delete=models.PROTECT,verbose_name='Категория',related_name='photos')
    def __str__(self):
        return self.title
    class Meta:
        verbose_name='Товар'
        verbose_name_plural='Товары'
        ordering=['title',]

    # Тип документа


class TypeDoc(models.Model):
    title = models.CharField(max_length=70, verbose_name='Тип документа')

    def __str__(self):
        return self.title


# Журнал документов

class Doc(models.Model):
    nomerdoc=models.CharField(max_length=20,verbose_name="Номер документв")
    datadoc=models.DateField(verbose_name='Дата документа')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Создан')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Обновлен')
    dealer=models.ForeignKey(Saler,verbose_name='Поставщик',on_delete=models.PROTECT)
    buytotal=models.DecimalField(max_digits=8,decimal_places=2,default=0.00)
    saletotal=models.DecimalField(max_digits=8,decimal_places=2,default=0.00)
    transaction=models.BooleanField(verbose_name='Проведен',default=False)
    typedoc=models.ForeignKey(TypeDoc,verbose_name='Тип документа',on_delete=models.PROTECT)
    user=models.CharField(max_length=100,verbose_name='Пользователь',blank=True,null=True,default='')
    def __str__(self):
        return str(self.nomerdoc)
    class Meta:
        verbose_name='Документ'
        verbose_name_plural='Документы'



# Журнал табличной части документов
class DocJurnal(models.Model):
    iddoc=models.ForeignKey(Doc,verbose_name='Документ',on_delete=models.CASCADE)
    title=models.ForeignKey(Good,verbose_name='Наименование товара',on_delete=models.CASCADE)
    volume=models.FloatField(blank=True)
    buyprice=models.FloatField(blank=True)
    percent=models.FloatField(blank=True)
    saleprice=models.FloatField(blank=True)
    buytotal=models.FloatField(blank=True)
    saletotal=models.FloatField(blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Создан')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Обновлен')
    typedoc=models.IntegerField(null=True)
    nomercheck=models.IntegerField(blank=True,null=True,verbose_name='Номер чека')
    user = models.CharField(max_length=100, verbose_name='Пользователь', blank=True, null=True, default='')
    class Meta:
        verbose_name='Наименование'
        verbose_name_plural='Наименования'
        ordering=['title',]
# Номер чека
class Check(models.Model):
    nomercheck=models.IntegerField()
    def __str__(self):
        return str(self.nomercheck)
# Временная таблица
class TempCheck(models.Model):
    idgood=models.IntegerField()
    title=models.CharField(max_length=100)
    unit=models.CharField(max_length=50)
    volume=models.FloatField(blank=True)
    price=models.FloatField(blank=True)
    total=models.FloatField(blank=True)
    maxvolume=models.FloatField(blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Создан')
    def __str__(self):
        return self.title



