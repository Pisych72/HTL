from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя',widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='Пароль',widget=forms.PasswordInput(attrs={'class':'form-control'}))


class UnitForm(forms.ModelForm):
   class Meta:
      model = Unit
      fields = ['title']
      widgets = {
      'title': forms.TextInput(attrs={'class':'form-input','style':'width:804px;border-radius:5px;border:none'}),
      }

class SalerForm(forms.ModelForm):
   class Meta:
      model = Saler
      fields = ['title']
      widgets = {
      'title': forms.TextInput(attrs={'class': 'form-input','style':'width:804px;border-radius:5px;border:none' }),
      }

class CustomerForm(forms.ModelForm):
   class Meta:
      model = Customer
      fields = ['title']
      widgets = {
      'title': forms.TextInput(attrs={'class': 'form-input','style':'width:804px;border-radius:5px;border:none' }),
      }

class PayForm(forms.ModelForm):
   class Meta:
      model = Pay
      fields = ['title']
      widgets = {
      'title': forms.TextInput(attrs={'class': 'form-input','style':'width:804px;border-radius:5px;border:none' }),
      }





# Категории
class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['title','photo',]
        widgets={
           'title':forms.TextInput(attrs={'class':'form-input','style':'width:465px;margin-right:10px;border-radius:5px;border:none'}),
           'photo':forms.FileInput(attrs={'style':'color:Grey'}),
        }



# Товары
class GoodForm(forms.ModelForm):
   class Meta:
      model = Good
      # fields='__all__'
      fields = ['title', 'unit', 'category']

      widgets = {
         'title': forms.TextInput(attrs={'class': 'form-input','placeholder':'Введите наименование товара...',
          'style': 'width:500px;margin-right:2px;border:none;border-radius:5px'}),
         'unit': forms.Select(attrs={'class': 'form-input','style': 'margin-left:5px;'
         'margin-right:2px;border:none;border-radius:5px'}),
         'category': forms.Select(attrs={'class': 'form-input','style': 'margin-left:6px;margin-right:2px;border:none;border-radius:5px'}),

      }
   def __init__(self, *args, **kwargs):
      super(GoodForm, self).__init__(*args, **kwargs)
      self.fields['unit'].empty_label = ''
      self.fields['category'].empty_label = ''


class MyDateInput(forms.DateInput):
   input_type = 'date'
   format = '%d-%m-%Y'

# Ввод остатков шапка
class InitialDocForm(forms.ModelForm):
   class Meta:
      model=Doc
      fields=['nomerdoc','datadoc','dealer','typedoc','id']
      widgets={
            'nomerdoc':forms.TextInput(attrs={'class':'righttext','style':'width:75px;'}),
            'datadoc':MyDateInput(attrs={'class':'righttext','style':'width:140px;'}),
            'dealer':forms.HiddenInput(),
            'typedoc': forms.HiddenInput(),
          'id': forms.HiddenInput(),
        }

# Ввод остатков табличная часть
class InitialTableForm(forms.ModelForm):
   class Meta:
      model=DocJurnal
      fields=['title','volume','buyprice','percent','saleprice','buytotal','saletotal','typedoc',]
      widgets = {
                 'typedoc': forms.NumberInput(attrs={'style':'display:None'}),
                 'volume': forms.NumberInput(attrs={ 'class':'righttext','min': 0, 'value': 1,
                                                    'oninput': 'getResult()', 'step': 'any','style':'width:75px;'}),
                 'title': forms.Select(attrs={'class':'formselect'}),
                 'buyprice': forms.NumberInput(
                     attrs={'class':'righttext', 'min': 0, 'step': 'any','value': 1, 'oninput': 'getResult()','style':'width:75px;'}),
                 'saleprice': forms.NumberInput(
                     attrs={ 'class':'righttext','min': 0, 'step': 'any','value': 1, 'oninput': 'getResult()', 'style':'width:75px;' }),
                 'percent': forms.NumberInput(
                     attrs={'class':'righttext', 'min': 0,'step': 'any', 'value': 20, 'oninput': 'getResult()', 'style':'width:75px;' }),
                 'buytotal': forms.NumberInput(
                     attrs={'class':'righttext', 'min': 0,'step': 'any','value': 1, 'style':'width:75px;' }),
                 'saletotal': forms.NumberInput(
                     attrs={'class':'righttext', 'min': 0, 'step': 'any', 'value': 1,'style':'width:75px;' }),
                 }


# Поступление шапка
class ReceiptDocForm(forms.ModelForm):
   class Meta:
      model=Doc
      fields=['nomerdoc','datadoc','dealer','typedoc','id']
      widgets={
            'nomerdoc':forms.TextInput(attrs={'class':'righttext','style':'width:75px;'}),
            'datadoc':MyDateInput(attrs={'class':'righttext','style':'width:140px;'}),
            'dealer':forms.Select(attrs={'class':'formselect'}),
            'typedoc': forms.HiddenInput(),
          'id': forms.HiddenInput(),
        }


# Поступление табличная часть
class ReceiptTableForm(forms.ModelForm):
   class Meta:
      model=DocJurnal
      fields=['title','volume','buyprice','percent','saleprice','buytotal','saletotal','typedoc',]
      widgets = {
                 'typedoc': forms.NumberInput(attrs={'style':'display:None'}),
                 'volume': forms.NumberInput(attrs={ 'class':'righttext','min': 0, 'value': 1,
                                                    'oninput': 'getResult()', 'step': 'any','style':'width:75px;'}),
                 'title': forms.Select(attrs={'class':'formselect'}),
                 'buyprice': forms.NumberInput(
                     attrs={'class':'righttext', 'min': 0, 'step': 'any','value': 1, 'oninput': 'getResult()','style':'width:75px;'}),
                 'saleprice': forms.NumberInput(
                     attrs={ 'class':'righttext','min': 0, 'step': 'any','value': 1, 'oninput': 'getResult()', 'style':'width:75px;' }),
                 'percent': forms.NumberInput(
                     attrs={'class':'righttext', 'min': 0,'step': 'any', 'value': 20, 'oninput': 'getResult()', 'style':'width:75px;' }),
                 'buytotal': forms.NumberInput(
                     attrs={'class':'righttext', 'min': 0,'step': 'any','value': 1, 'style':'width:75px;' }),
                 'saletotal': forms.NumberInput(
                     attrs={'class':'righttext', 'min': 0, 'step': 'any', 'value': 1,'style':'width:75px;' }),
                 }

