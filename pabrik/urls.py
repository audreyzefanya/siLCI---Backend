from django.urls import path

from .views import *

app_name = 'pabrik'

urlpatterns = [
    path('allpabrik', PabrikViewSet.as_view({
        'get': 'getAllPabrik',
    })),
    path('allbarangpabrik', PabrikViewSet.as_view({
        'get': 'getAllBarangPabrik',
    })),
    path('create', PabrikViewSet.as_view({
        'post': 'createPabrik'
    })),
    #     path('detail/<str:pabrik_id>', PabrikViewSet.as_view({
    #     'get': 'detailPabrik'
    # })),
    #     path('update/<str:pabrik_id>', PabrikViewSet.as_view({
    #     'put': 'updatePabrik'
    # })),
    # path('perusahaan/all', PerusahaanViewSet.as_view({
    #     'get': 'getAllPerusahaan'
    # })),
    # path('perusahaan/create', PerusahaanViewSet.as_view({
    #     'post': 'createPerusahaan'
    # })),
    # path('perusahaan/<str:perusahaan_id>', PerusahaanViewSet.as_view({
    #     'get': 'getPabrikPerusahaan',
    #     'put': 'addPabrikToPerusahaan'
    # })),
]