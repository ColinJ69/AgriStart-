from django import forms

class Address_Form(forms.Form):
    address = forms.CharField(max_length=50, label='', widget=forms.TextInput(attrs={'class':'form-control','type':'text','placeholder':'Enter valid address...'}))
    
class soil_form(forms.Form):
    N = forms.CharField(max_length=2, label='', widget=forms.TextInput(attrs={'class':'form-control','type':'text','placeholder':'Enter Nitrogen Amount','size': 500}))
    P = forms.CharField(max_length=2, label='', widget=forms.TextInput(attrs={'class':'form-control','type':'text','placeholder':'Enter Phosphorus Amount'}))
    K = forms.CharField(max_length=2, label='', widget=forms.TextInput(attrs={'class':'form-control','type':'text','placeholder':'Enter Potassium Amount'}))
    pH = forms.CharField(max_length=2, label='', widget=forms.TextInput(attrs={'class':'form-control','type':'text','placeholder':'Enter Soil pH'}))
    temperature = forms.CharField(max_length=3, label='', widget=forms.TextInput(attrs={'class':'form-control','type':'text','placeholder':'Enter Avg Temperature'}))
    

class grant_form(forms.Form):
    state_choices = (
        ('All States', 'All States'),
        ('Alabama', 'Alabama'), ('Alaska', 'Alaska'), ('Arizona', 'Arizona'), ('Arkansas', 'Arkansas'), 
        ('California', 'California'), ('Colorado', 'Colorado'), ('Connecticut', 'Connecticut'), ('Delaware', 'Delaware'), 
        ('Florida', 'Florida'), ('Georgia', 'Georgia'), ('Hawaii', 'Hawaii'), ('Idaho', 'Idaho'), ('Illinois', 'Illinois'), ('Indiana', 'Indiana'),
       ('Iowa', 'Iowa'), ('Kansas','Kansas'), ('Kentucky','Kentucky'), ('Louisiana','Louisiana'), ('Maine', 'Maine'), ('Maryland', 'Maryland'), 
        ('Massachusetts', 'Massachusetts'), ('Michigan', 'Michigan'), ('Minnesota', 'Minnesota'), ('Mississippi', 'Mississippi'), ('Missouri', 'Missouri'), ('Montana', 'Montana'), ('Nebraska', 'Nebraska'), ('Nevada', 'Nevada'), ('New Hampshire', 'New Hampshire'),
       ('New Jersey', 'New Jersey'), ('New Mexico', 'New Mexico'), ('New York', 'New York'), ('North Carolina', 'North Carolina'), ('North Dakota', 'North Dakota'), ('Ohio', 'Ohio'), ('Oklahoma', 'Oklahoma'), ('Oregon', 'Oregon'), ('Pennsylvania', 'Pennsylvania'),
      ('Rhode Island', 'Rhode Island'), ('South Carolina', 'South Carolina'), ('South Dakota', 'South Dakota'), ('Tennessee','Tennessee'), ('Texas', 'Texas'), ('Utah', 'Utah'), 
      ('Vermont', 'Vermont'), ('Virginia', 'Virginia'), ('West Virginia', 'West Virginia'), ('Wisconsin', 'Wisconsin'), ('Wyoming','Wyoming'))
    state = forms.ChoiceField(label='', choices=state_choices, widget=forms.Select(attrs={'class': 'dropdown'}), initial='All States')
    a_choices = (
    ('All areas', 'All areas'),
     ('Economic', 'Economic'),
     ('Housing', 'Housing'),
     ('Energy', 'Energy'),
     ('Water', 'Water')       
    )  
    area = forms.ChoiceField(widget=forms.Select(attrs={'class':'dropdown'}), choices=a_choices, initial='All areas', label='')
    n_choices = (
        (0, 'No'),
        (1, 'Yes'),
        )
    native = forms.ChoiceField(widget=forms.Select(attrs={'class':'dropdown'}), choices=n_choices, initial='No', label='')