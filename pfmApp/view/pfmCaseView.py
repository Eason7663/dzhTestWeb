from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from pfmApp.forms import JmeterSvrModelForm
from pfmApp.models import PfmCaseModel

import os
import pdb


# Create your views here.
@login_required
def add_jmeter_server_action(request):
    # jsmf = JmeterSvrModelForm(request.POST)
    return render(request, "pfmApp/jmeterServer.html")


@login_required
def pfmCase_home_view(request):
    pfmCase = PfmCaseModel.objects.all()
    username = request.session.get('username', '')
    return render(request, "pfmApp/pfmCaseHome.html",{"user": username,"pfmCases":pfmCase})


from appaction.singletonClass import JmeterServer
from appaction.jmeterThread import JmxRunThread
from appaction.fetchReportThread import FetchReportThread

@login_required
def execute_pfmCase(request,case_id):

    host = "10.15.107.189"
    username = "root"
    password = "znzyjwqqlsjrghwy189"
    path = "/opt/apache-jmeter-3.2/bin/"
    jmeterServer = JmeterServer(host,username,password,path)

    pfmCase = PfmCaseModel.objects.get(id=case_id)
    t = JmxRunThread(jmeterServer,pfmCase,"JsvrThread")

    t.initTaskList()
    t.start()
    # reportName = "concept_100.jtl"
    # fetchReport = FetchReportThread(jmeterServer, reportName, "FetchReport")
    # fetchReport.start()

    while True:
        msg = t.msgQueue.get()
        if "Task has been done:" in msg:
            reportName =msg.split("->")[-1].replace(".jmx",".jtl")
            print(reportName)
            # reportName= "concept_100.jtl"
            fetchReport = FetchReportThread(jmeterServer,reportName,t.msgQueue,"FetchReport")
            fetchReport.start()
        print(msg)
        if msg == "All Task Done" or msg == "Task has been interrupted":
            break
    # print(pfmCase.scriptName)
    return HttpResponse(str(case_id))

@login_required
def script_upload_action(request):
    # pdb.set_trace()
    if request.method == "POST":
        # file = str(request.FILES['file'])
        # is_private = request.POST['is_private']
        # print(request.FILES['file'])
        # print(is_private)
        handle_upload_file(request.FILES['file'], str(request.FILES['file']))
        # jsmf = JmeterSvrModelForm(request.POST)
        # return render(request, "pfmApp/jmeterServer3.html", {'form': jsmf})

    return HttpResponse('Successful')  # 此处简单返回一个成功的消息，在实际应用中可以返回到指定的页面中

    # return JsonResponse({'A':'Failed'})


def handle_upload_file(file, filename):
    path = 'script/'  # 上传文件的保存路径，可以自己指定任意的路径
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
