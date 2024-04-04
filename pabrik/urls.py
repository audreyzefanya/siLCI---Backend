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
    path('<str:pabrik_name>', PabrikViewSet.as_view({
        'get': 'getPabrik',
    })),
    path('batch/<str:pabrik_name>', BatchProduksiViewSet.as_view({
        'get': 'getAllBatchProduksiInPabrik',
        'post': 'addBatchProduksiToPabrik'
    })),
    path('batch/<str:pabrik_name>/<str:batch_code>', BatchProduksiViewSet.as_view({
        'get': 'getAllBatchProduksiInPabrik',
        'post': 'addBatchProduksiToPabrik'
    })),
    path('barang/<str:pabrik_name>', BarangPabrikViewSet.as_view({
        'get': 'getBarangInPabrik',
        'post': 'addBarangToPabrik'
    })),
    path('permintaanpengiriman/<str:pabrik_name>', PermintaanPengirimanViewSet.as_view({
        'get': 'getDaftarPengiriman',
    })),
    path('statuspengiriman/<str:kode_permintaan>', PermintaanPengirimanViewSet.as_view({
        'put': 'statusPengiriman',
    })),
    #     path('detail/<str:pabrik_id>', PabrikViewSet.as_view({
    #     'get': 'detailPabrik'
    # })),
    #     path('update/<str:pabrik_id>', PabrikViewSet.as_view({
    #     'put': 'updatePabrik'
    # })),
]