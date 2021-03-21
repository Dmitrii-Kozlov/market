from django import forms
from .models import Product

PUBLICH_CHOISES = (
    ('publish', 'Publish'),
    ('draft', 'Draft')
)
class ProductAddForm(forms.Form):
    title = forms.CharField(label='Your Title', widget=forms.TextInput(
        attrs={
        "class": "my-class",
        "placeholder": "Title"
    }))
    description = forms.CharField(widget=forms.Textarea(
        attrs={
            "placeholder": "Description"
        }
    ))
    price = forms.DecimalField()
    publish = forms.ChoiceField(choices=PUBLICH_CHOISES, widget=forms.RadioSelect)

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 1:
            raise forms.ValidationError('Price must be at least $1')
        elif price >= 100:
            raise forms.ValidationError('Price must not be greater than $100')
        else:
            return price

class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "title", "description", "price"
        ]
        # widgets = {"description": forms.Textarea(attrs={
        #     "placeholder": "Description"
        # })}
    publish = forms.ChoiceField(choices=PUBLICH_CHOISES, widget=forms.RadioSelect)
    description = forms.CharField(widget=forms.Textarea(
        attrs={
            "placeholder": "New Description"
        }
    ))
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 1:
            raise forms.ValidationError('Price must be at least $1')
        elif price >= 100:
            raise forms.ValidationError('Price must not be greater than $100')
        else:
            return price