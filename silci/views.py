from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from .models import Barang

# Create your views here.
def show_xml(request):
	data = Barang.objects.all()
	return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")