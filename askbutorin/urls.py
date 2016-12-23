from django.conf.urls import url
from django.contrib import admin
from ask_app import views
from . import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^$', views.index, name='index'),
    url(r'^hot/$', views.hot, name='hot'),
    url(r'^tag/(?P<tag>.+)/$', views.tag, name='tag'),
    url(r'^ask/$', views.ask, name='ask'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^question/(?P<id>\d+)/?$', views.question, name='question'),
    url(r'^settings/', views.settings, name='settings'),
    url(r'^change_password/', views.change_password, name='change_password'),
    url(r'^like/$', views.like, name='like'),
    url(r'^correct/$', views.correct_answer, name='correct'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
