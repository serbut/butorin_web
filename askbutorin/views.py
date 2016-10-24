from django.shortcuts import render

# Create your views here.
def get_params(request):
        return render(request, 'get_params.html', {})
