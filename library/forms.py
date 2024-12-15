# forms.py

from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, label='Arama', widget=forms.TextInput(attrs={'placeholder': 'Kitap veya yazar ara...', 'class': 'input'}))
