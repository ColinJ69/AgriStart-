from django.shortcuts import render
from .forms import Address_Form, soil_form, grant_form
from .analyze import get_score, get_recommendations, disease_detection, recommend_grants
import urllib.parse

# Create your views here.

def home(request):
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
            return render(request, 'homepage.html', context=context)
        
                
        
    
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
            print(recommendations)
            return render(request, 'recommendations.html', {'fertilizer': recommendations.keys(), 'crops': recommendations.values()})
        
    form = soil_form()
    return render(request, 'recommendations.html', {'form':form})

def detection(request):
    if request.GET.get('Scan') == 'Scan':
        results = disease_detection()
        print(results)
        return render(request, 'detection.html', {'result': results})
    return render(request, 'detection.html')


def grants(request):
    if request.method == 'POST':
        form = grant_form(request.POST)
        if form.is_valid():
            state = form.cleaned_data['state']
            area = form.cleaned_data['area']
            native = form.cleaned_data['native']
            grants = recommend_grants(state, area, native)
            context = {
                'grants': grants,
                'form': form
                }
            return render(request, 'grants.htmml', context=context)
    form = grant_form()
    context = {'form':form}
    return render(request, 'grants.html', context=context)
def tutorials(request):
    return render(request, 'tutorials.html')
def growing(request):
    return render(request, 'growing.html')
def sustainable(request):
    return render(request, 'sustainable.html')