from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Activity
from .forms import ActivityForm
from .serializers import ActivitySerializer

# 참고 : https://inma.tistory.com/88
class ActivityList(APIView):
    def post(self, request, format=None):
        serializers = ActivitySerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        queryset = Activity.objects.all()
        serializers = ActivitySerializer(queryset, many=True)
        return Response(serializers.data)

# 실습용 - 실제로 사용하지는 않음
class ActivityDetail(APIView):
    def get_object(self, pk):
        try:
            return Activity.objects.get(pk=pk)
        except Activity.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        activity = self.get_object(pk)
        serializers = ActivitySerializer(activity)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        activity = self.get_object(pk)
        serializers = ActivitySerializer(activity, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        activity=self.get_object(pk)
        activity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete_all(self, request, format=None):
        Activity.objects.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Create your views here.
def index(request):
    return render(request, 'yoursleeping/index.html', {})

def data_list(request):
    datas = Activity.objects.filter().order_by('date') #.order_by('time')

    return render(request, 'yoursleeping/data_list.html', { 'datas' : datas })

@csrf_exempt
def data_add(request):
    try:
        if request.method == "POST":
            form = ActivityForm(request.POST)
            if form.is_valid():
                data = form.save(commit=True)
    except Exception as exception:
        return JsonResponse({
            'success' : False,
            'exception' : exception
        }, json_dumps_params = { 'ensure_ascii' : True})

    return JsonResponse({
        'success' : True,
    }, json_dumps_params = { 'ensure_ascii' : True})

def data_delete(request):
    try:
        Activity.objects.filter().delete()
    except Exception as exception:
        return JsonResponse({
            'success' : False,
            'exception' : exception
        }, json_dumps_params = { 'ensure_ascii' : True})

    return JsonResponse({
        'success' : True,
    }, json_dumps_params = { 'ensure_ascii' : True})
