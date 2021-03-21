from django import forms

class ProductAddForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    price = forms.DecimalField()

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 1:
            raise forms.ValidationError('Price must be at least $1')
        elif price >= 100:
            raise forms.ValidationError('Price must not be greater than $100')
        else:
            return price