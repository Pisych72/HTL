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