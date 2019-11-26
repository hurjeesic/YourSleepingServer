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
    datas = Activity.objects.filter().order_by('date', 'time')

    return render(request, 'yoursleeping/data_list.html', { 'datas' : datas, 'size' : len(datas) })

@csrf_exempt
def data_add(request):
    bComplete = False
    try:
        if request.method == "POST":
            form = ActivityForm(request.POST)
            if form.is_valid():
                data = form.save(commit=True)

            if int(request.POST.get('heart_rate')) == -1: bComplete = True
    except Exception as exception:
        return JsonResponse({
            'success' : False,
            'exception' : exception
        }, json_dumps_params = { 'ensure_ascii' : False })

    return JsonResponse({
        'success' : True,
        'completed' : bComplete,
    }, json_dumps_params = { 'ensure_ascii' : True })

@csrf_exempt
def data_add_all(request):
    try:
        if request.method == "POST":
            length = int(request.POST.get('size'))
            for i in range(length):
                data = Activity()
                data.date = int(request.POST.get('date' + str(i)))
                data.time = int(request.POST.get('time' + str(i)))
                data.heartrate = int(request.POST.get('heartrate' + str(i)))
                data.type = int(request.POST.get('type' + str(i)))
                data.sleep_time = int(request.POST.get('sleep_time' + str(i)))
                data.save()
        else:
            length = int(request.GET.get('size'))
            for i in range(length):
                data = Activity()
                data.date = int(request.GET.get('date' + str(i)))
                data.time = int(request.GET.get('time' + str(i)))
                data.heartrate = int(request.GET.get('heartrate' + str(i)))
                data.type = int(request.GET.get('type' + str(i)))
                data.sleep_time = int(request.GET.get('sleep_time' + str(i)))
                data.save()
    except Exception as exception:
        return JsonResponse({
            'success' : False,
            'exception' : exception
        }, json_dumps_params = { 'ensure_ascii' : False })

    return JsonResponse({
        'success' : True,
    }, json_dumps_params = { 'ensure_ascii' : True })

def data_delete(request):
    try:
        Activity.objects.filter().delete()
    except Exception as exception:
        return JsonResponse({
            'success' : False,
            'exception' : exception
        }, json_dumps_params = { 'ensure_ascii' : False })

    return JsonResponse({
        'success' : True,
    }, json_dumps_params = { 'ensure_ascii' : True })

def sleep_analyze(request):
    try:
        # 데이터 저장
        datas = Activity.objects.filter().order_by('date')
        csv_data = []
        csv_data.append(["date", "time", "sleep", "sleep_time"])
        for data in datas:
            csv_data.append([data.date, data.time, data.type, data.sleep_time])

        import os
        import pandas as pd

        path = os.path.dirname(__file__) + "\\static\\data\\sleepdata.csv"
        df = pd.DataFrame(csv_data)
        df.to_csv(path, header=False, index=False)

        # 머신러닝
        import sklearn
        from sklearn.model_selection import train_test_split
        from sklearn import svm  #for Support Vector Machine (SVM) Algorithm
        from sklearn import metrics #for checking the model accuracy

        def read_data(filename): #학습할 데이터 읽기
            return pd.read_csv(filename)

        def make_matching_data(time, sleep, sleep_time): #비교할 시간, 수면상태, 수면시간 을 넣어주면 dataframe형태로 반환
            from datetime import datetime, timedelta

            target_date = datetime.now()
            if time < target_date.hour * 60 + target_date.minute:
                target_date += timedelta(days = 1)

            target_date_str = target_date.strftime('%Y%m%d')

            matching_data = []

            i = 0
            now = datetime.now()
            while True:
                date_str = now.strftime('%Y%m%d')
                time_str = str(now.hour * 60 + now.minute)
                matching_data.append([int(date_str), int(time_str), sleep, sleep_time])

                # print(target_date_str + " == " + date_str + ", " + str(time) + " == " + time_str)
                if int(target_date_str) == int(date_str) and time == int(time_str): break

                now += timedelta(minutes = 1)

            return pd.DataFrame(matching_data, columns = ['date', 'time', 'sleep', 'sleep_time'])

        def run_svm(df, list, target, data):
            train_X = df[list]  # 키와 발크기만 선택
            train_y = df[target]  # 정답 선택
            test_X = data[list]  # taking test data features
            test_y = data[target]  # output value of test data

            baby1 = svm.SVC()  # 애기
            baby1 = svm.SVC(gamma='auto')
            baby1.fit(train_X, train_y)  # 가르친 후
            prediction = baby1.predict(test_X)  # 테스트
            score = metrics.accuracy_score(prediction, test_y) * 100
            print('인식률:', score)

            return prediction.tolist()

        predictedTime = 140
        target_state = 1
        sleep_data = read_data(path) #학습 데이터 읽기
        data = make_matching_data(predictedTime, target_state, 1    ) #비교할 데이터 만들기
        result = run_svm(sleep_data, ['time', 'sleep_time'], 'sleep', data) #인공저능아부분

        for i in range(len(result) - 1, 0, -1):
            if result[i] == target_state:
                predictedTime -= len(result) - i - 1
                if (predictedTime < 0): predictedTime += 60 * 24
                break

        #위는 쓰는 예시 ㅎㅇㅌ
    except Exception as exception:
        return JsonResponse({
            'success' : False,
            'exception' : exception
        }, json_dumps_params = { 'ensure_ascii' : False })

    return JsonResponse({
        'success' : True,
        'time' : predictedTime,
    }, json_dumps_params = { 'ensure_ascii' : True })
