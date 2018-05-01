from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from pfmApp.forms import JmeterSvrModelForm

import os
import pdb


# Create your views here.
@login_required
def add_jmeter_server_action(request):
    # jsmf = JmeterSvrModelForm(request.POST)
    return render(request, "pfmApp/jmeterServer.html")


@login_required
def testTable(request):
    return render(request, "pfmApp/jmxUpload.html")

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

        # return HttpResponse('Successful')  # 此处简单返回一个成功的消息，在实际应用中可以返回到指定的页面中

    return JsonResponse({'A':'Failed'})


def handle_upload_file(file, filename):
    path = 'script/'  # 上传文件的保存路径，可以自己指定任意的路径
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
