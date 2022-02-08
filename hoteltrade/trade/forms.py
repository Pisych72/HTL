from django import forms
from .models import *

class UnitForm(forms.ModelForm):
   class Meta:
      model = Unit
      fields = ['title']
      widgets = {
      'title': forms.TextInput(attrs={'class':'form-input','style':'width:758px'}),
      }

class SalerForm(forms.ModelForm):
   class Meta:
      model = Saler
      fields = ['title']
      widgets = {
      'title': forms.TextInput(attrs={'class': 'form-input','style':'width:758px' }),
      }

class CustomerForm(forms.ModelForm):
   class Meta:
      model = Customer
      fields = ['title']
      widgets = {
      'title': forms.TextInput(attrs={'class': 'form-input','style':'width:758px' }),
      }

class PayForm(forms.ModelForm):
   class Meta:
      model = Pay
      fields = ['title']
      widgets = {
      'title': forms.TextInput(attrs={'class': 'form-input','style':'width:758px' }),
      }





# Категории
class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['title','photo',]
        widgets={
           'title':forms.TextInput(attrs={'class':'form-input','style':'width:455px;margin-right:10px'}),
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
          'style': 'width:440px;margin-right:2px;'}),
         'unit': forms.Select(attrs={'class': 'form-input','style': 'margin-left:5px;margin-right:2px'}),
         'category': forms.Select(attrs={'class': 'form-input','style': 'margin-left:6px;margin-right:2px'}),

      }
   def __init__(self, *args, **kwargs):
      super(GoodForm, self).__init__(*args, **kwargs)
      self.fields['unit'].empty_label = ''
      self.fields['category'].empty_label = ''