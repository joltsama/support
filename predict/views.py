from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import AgentResponseTime
from .predict import ex1 as AG
import time
import random


def index(request):
    return render(request, 'predict/home.html')


def gen_random_data(request):
    ag = AG.AgentPredictTime()
    issues = ag.generate_issue_data(28800)
    pred_data = ag.make_pred_data()
    AgentResponseTime.objects.all().delete()
    for issue in issues:
        ag.predict_time(issue, pred_data)
    for i in pred_data:
        print(i)
    for i in range(len(pred_data)):
        a = AgentResponseTime(time_of_day=i, answer_time=pred_data[i])
        a.save()

    return HttpResponse('Data generated successfully. go to /')


def CurrentTimings(request):
    labels = []
    data = []

    queryset = AgentResponseTime.objects.all().order_by('time_of_day')
    for t in queryset:
        a = time.strftime("%H:%M", time.localtime(t.time_of_day*3600))
        # labels.append(time.time_of_day)
        labels.append(a)
        data.append(t.answer_time)

    return JsonResponse(data={
        'labels': labels,
        'data': data
    })


def simulate(request):
    return render(request, 'predict/simulate.html')


def simulatedata(request):
    ag = AG.AgentPredictTime()
    pred_data = []
    labels = []
    queryset = AgentResponseTime.objects.all().order_by('time_of_day')
    for t in queryset:
        a = time.strftime("%H:%M", time.localtime(t.time_of_day*3600))
        labels.append(a)
        pred_data.append(t.answer_time)

    data_new, newissues = ag.simulate(pred_data)

    issueset = data_new[:]
    for i in newissues:
        start_time, answer_time = ag.simplify_issue_time(i)
        issueset[start_time] = answer_time

    for i in range(len(pred_data)):
        a = AgentResponseTime(time_of_day=i, answer_time=pred_data[i])
        a.save()

    return JsonResponse(data={
        'labels': labels,
        'data_old': pred_data,
        'data_new': data_new,
        'issueset': issueset
    })


def change(request):
    start_time = request.POST['start_time']
    end_time = request.POST['end_time']
    change_value = request.POST['change_value']

    ag = AG.AgentPredictTime()
    start_time = ag.simplify_issue_time_from_time(start_time)
    end_time = ag.simplify_issue_time_from_time(end_time)
    answer_time = int(change_value)

    queryset = AgentResponseTime.objects.all().order_by('time_of_day')

    pred_data = []
    for t in queryset:
        pred_data.append(t.answer_time)

    print(start_time, end_time, len(pred_data))

    for i in range(start_time, end_time+1):
        ag.predict_time2((i, answer_time), pred_data)

    for i in range(start_time, end_time+1):
        a = AgentResponseTime.objects.get(pk=i)
        a.answer_time = pred_data[i]
        a.save()

    return HttpResponseRedirect('/')
