from django import forms


class NewSellerForm(forms.Form):
    storename = forms.CharField(max_length=100, label='store name')
    location = forms.CharField(max_length=100,label='location')
    agree = forms.BooleanField(label='Agree to Terms', widget=forms.CheckboxInput)
