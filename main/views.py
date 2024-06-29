from django.shortcuts import render
from .forms import Address_Form, soil_form, grant_form
from .analyze import get_score, get_recommendations, disease_detection, recommend_grants
import urllib.parse

# Create your views here.
def home(request):
    return render(request, 'homepage.html')
def score(request):
    if request.method == 'POST':
        form = Address_Form(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            
            
            clean_address = urllib.parse.quote(address, safe='/', encoding=None, errors=None)
           
            final_score, attrs, city, miles = get_score(clean_address)
            

            context = {
                'average_temp': round(attrs['temperature'],1),
                'soil_temp': attrs['s_temp'],
                'soil_moist': attrs['soil_moist'],
                'climate': attrs['climate'],
                'score': final_score,
                'form': form,
                'city': city,
                'miles': miles
            }
            return render(request, 'scorepage.html', context=context)
        
                
        
    
    form = Address_Form()
        
    context = {
        'form':form
        }
    return render(request, 'startpage.html', context=context)
def recommendation(request):
    if request.method == 'POST':
        form = soil_form(request.POST)
        if form.is_valid():
            N = form.cleaned_data['N']
            P = form.cleaned_data['P']
            K = form.cleaned_data['K']
            pH = form.cleaned_data['pH']
            temperature = form.cleaned_data['temperature']
            recommendations = get_recommendations(N, P, K, pH, temperature)
            crops = list(recommendations.keys())
            fertilizers = list(recommendations.values())

            return render(request, 'recommendations.html', {'crops': zip(crops, fertilizers), 'submitted': True})
        
    form = soil_form()
    return render(request, 'recommendations.html', {'form':form, 'submitted': False})

def detection(request):
    if request.GET.get('Scan') == 'Scan':
        results = disease_detection()
        print(results)
        return render(request, 'detection.html', {'result': results, 'submitted':True})
    return render(request, 'detection.html', {'submitted': False})


def grants(request):
    if request.method == 'POST':
        form = grant_form(request.POST)
        if form.is_valid():
            state = form.cleaned_data['state']
            area = form.cleaned_data['area']
            native = form.cleaned_data['native']
            print(state, area, native)
            grants = recommend_grants(state, area, native)
            grant_names = [grants['Name'].iloc[0], grants['Name'].iloc[1], grants['Name'].iloc[2]]
            grant_amounts =[grants['Amount'].iloc[0], grants['Amount'].iloc[1], grants['Amount'].iloc[2]]
            grants = zip(grant_names, grant_amounts)
 
            
            context = {
                'grants': grants,
                'form': form,
                'submitted': True
                }
            return render(request, 'grants.html', context=context)
    form = grant_form()
    context = {'form':form, 'submitted': False}
    return render(request, 'grants.html', context=context)
def tutorials(request):
    return render(request, 'tutorials.html')
def growing(request):
    return render(request, 'growing.html')
def sustainable(request):
    return render(request, 'sustainable.html')