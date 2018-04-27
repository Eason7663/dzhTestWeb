from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from pfmApp.forms import JmeterSvrModelForm

import os

# Create your views here.
@login_required
def add_jmeter_server_action(request):
    jsmf = JmeterSvrModelForm(request.POST)
    return render(request,"pfmApp/jmeterServer.html",{'form':jsmf})

@login_required
def script_upload_action(request):
    if request.method == "POST":

        handle_upload_file(request.FILES['file'], str(request.FILES['file']))
        # jsmf = JmeterSvrModelForm(request.POST)
        # return render(request, "pfmApp/jmeterServer.html", {'form': jsmf})

        # return HttpResponse('Successful')  # 此处简单返回一个成功的消息，在实际应用中可以返回到指定的页面中

    return HttpResponse('Failed')


def handle_upload_file(file, filename):
    path = 'script/'  # 上传文件的保存路径，可以自己指定任意的路径
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
