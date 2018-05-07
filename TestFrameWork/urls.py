"""
TestFrameWork URL Configuration

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
from regApp.urls import router
from regApp.views import TestProjectViews,TestSuitViews,TestCaseViews,UserViews
from pfmApp.view import pfmCaseView as pfmAppViews

# from rest_framework.authtoken import views

urlpatterns = [
    ###首页
    url(r'^$', UserViews.index, name='index'),
    ###pfmApp
    url(r'^pfmApp/', include('pfmApp.urls'),name='pfmApp'),
    ###regApp
    url(r'^regApp/', include('regApp.urls'), name='regApp'),
    url(r'^admin/', admin.site.urls,),

    url(r'^accounts/login/', include('regApp.urls')),
    url(r'^login/action$', UserViews.login_action),
    url(r'^logout$', UserViews.logout_action),
    # url(r'^testproject_manage/$', TestProjectViews.testproject_manage),
    # url(r'^testsuit_manage/$', TestSuitViews.testsuit_manage),
    # # url(r'^testcase_manage/$', views.testcase_manage),
    # url(r'^testcase_manage/$', TestCaseViews.testcase_manage),
    url(r'^help_document$', UserViews.help_document),
    # url(r'^execute_case/(?P<case_id>[0-9]+)/$', include('regApp.urls')),
    # url(r'^testcase/add', TestCaseViews.add_case_action),
    # url(r'^testcase/post/add', TestCaseViews.add_post_case_action),

    ############################API
    url(r'^api/',include(router.urls)),
    ############################token
]
# ] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)