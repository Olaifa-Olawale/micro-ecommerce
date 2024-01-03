from django import forms
from .models import Product


#input_css_class = "form-control"
input_css_class = "bg-gray-700 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"

class ProductForm(forms.ModelForm):
    # name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    class Meta:
        model = Product
        fields = ['name', 'handle', 'price']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.field:
            self.fields[field].widget.attrs['class'] = input_css_class
        