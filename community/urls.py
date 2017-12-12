from django.conf.urls import url

from . import views

app_name = 'community'  # 必须设置这个app_name,告诉Django这个urls模块属于community,这样才能在model中写方法时,调用name=xxx的函数
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(\w+)/(?P<pk>\d+)/$', views.topic, name='topic'),  # 一次只传入一个参数，在这个url中板块的名字直接用/w+匹配
    url(r'^(?P<board_name>\w+)/$', views.board, name='board'),
]