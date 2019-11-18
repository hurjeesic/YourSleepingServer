from django.shortcuts import render
from .models import Activity

# Create your views here.
def index(request):
    return render(request, 'yoursleeping/index.html', {})

def data_list(request):
    datas = Activity.objects.filter().order_by('date').order_by('time')

    return render(request, 'yoursleeping/data_list.html', { 'datas' : datas })
