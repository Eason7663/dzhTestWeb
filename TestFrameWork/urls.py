"""TestFrameWork URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
# from rest_framework.authtoken.views import  obtain_auth_token
from polls.urls import router
from polls import views
from pfmApp.view import pfmCaseView as pfmAppViews

# from pfmApp.urls import router

urlpatterns = [
    ###pfmApp
    url(r'^pfmApp/', include('pfmApp.urls'),name='pfmApp'),
    ###polls
    url(r'^polls/', include('polls.urls'),name='polls'),
    url(r'^admin/', admin.site.urls,),
    url(r'^', include('polls.urls')),
    url(r'^accounts/login/', include('polls.urls')),
    url(r'^login_action/$', views.login_action),
    url(r'^logout/$', views.logout_action),
    url(r'^testproject_manage/$', views.testproject_manage),
    url(r'^testsuit_manage/$', views.testsuit_manage),
    # url(r'^testcase_manage/$', views.testcase_manage),
    url(r'^testcase_manage/$', views.testcase_manage),
    url(r'^search_project_name/$', views.search_project_name),
    url(r'^help_document/$', views.help_document),
    # url(r'^execute_case/(?P<case_id>[0-9]+)/$', include('polls.urls')),
    url(r'^testcase/add', views.add_case_action),
    url(r'^testcase/post/add', views.add_post_case_action),
    url(r'^execute_case/(?P<case_id>[0-9]+)/$', views.execute_case_action),
    url(r'^execute_case/detail/(?P<case_id>[0-9]+)/$', views.execute_case_detail_action),
    ############################API
    url(r'^api/',include(router.urls)),
    ############################pfmApp
    url(r'^performance/case/add$',pfmAppViews.add_jmeter_server_action),
    url(r'^pfmApp/script/upload$',pfmAppViews.script_upload_action),
    url(r'^jmx/analyze/page$',pfmAppViews.testTable),


]
# ] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)