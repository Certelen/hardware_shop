from django import forms


class SearchForm(forms.Form):
    search_product = forms.CharField(
        label='search_product', max_length=50, required=False)
