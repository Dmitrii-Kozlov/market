from django import forms

class NewSellerForm(forms.Form):
    agreed = forms.BooleanField(label='Agreed to terms', widget=forms.CheckboxInput)