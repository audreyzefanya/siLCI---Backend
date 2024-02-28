from django.urls import path
from silci.views import show_xml 

app_name = 'silci'

urlpatterns = [
    path('xml/', show_xml, name='show_xml'),
]