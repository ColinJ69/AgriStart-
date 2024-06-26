from django import forms

class Address_Form(forms.Form):
    address = forms.CharField(max_length=50, label='', widget=forms.TextInput(attrs={'class':'form-control','type':'text','placeholder':'Enter valid address...'}))
    
class soil_form(forms.Form):
    N = forms.CharField(max_length=2)
    P = forms.CharField(max_length=2)
    K = forms.CharField(max_length=2)
    pH = forms.CharField(max_length=2)
    temperature = forms.CharField(max_length=3)
    

class grant_form(forms.Form):
    state = forms.CharField(max_length=15, label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your state name'}))
    a_choices = (
    ('All areas', 'All areas'),
     ('Economic', 'Economic'),
     ('Housing', 'Housing'),
     ('Energy', 'Energy'),
     ('Water', 'Water')       
    )  
    area = forms.ChoiceField(widget=forms.Select(attrs={'class':'dropdown'}), choices=a_choices, initial='All areas', label='')
    n_choices = (
        ('No', 0),
        ('Yes', 1),
        )
    native = forms.ChoiceField(widget=forms.Select(attrs={'class':'dropdown'}), choices=n_choices, initial='No', label='')