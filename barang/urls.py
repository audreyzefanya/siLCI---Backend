from django.urls import path

from .views import *

app_name = 'barang'

urlpatterns = [
    path('all', BarangViewSet.as_view({
        'get': 'getAllBarang',
    })),
    path('create', BarangViewSet.as_view({
        'post': 'createBarang'
    })),
    path('detail/<str:barang_id>', BarangViewSet.as_view({
        'get': 'detailBarang'
    })),
    path('update/<str:barang_id>', BarangViewSet.as_view({
        'put': 'updateBarang'
    })),
    path('perusahaan/all', PerusahaanViewSet.as_view({
        'get': 'getAllPerusahaan'
    })),
    path('perusahaan/create', PerusahaanViewSet.as_view({
        'post': 'createPerusahaan'
    })),
    path('perusahaan/<str:perusahaan_id>', PerusahaanViewSet.as_view({
        'get': 'getBarangPerusahaan',
        'put': 'addBarangToPerusahaan'
    })),
    path('perusahaan/detail/<str:perusahaan_id>', PerusahaanViewSet.as_view({
        'get': 'getPerusahaan',
    })),
    path('perusahaan/barang/request', PengadaanViewSet.as_view({
        'post': 'addPengadaaanImpor'
    })),
    path('perusahaan/request/<str:pengadaan_id>/status', PengadaanViewSet.as_view({
        'put': 'increaseStatusPengadaan'
    })),
    path('perusahaan/request/<str:pengadaan_id>/reject', PengadaanViewSet.as_view({
        'put': 'rejectPengadaan'
    })),
    path('perusahaan/request/detail/<str:pengadaan_id>/', PengadaanViewSet.as_view({
        'get': 'detailPengadaan'
    })),

    path('perusahaan/request/all/', PengadaanViewSet.as_view({
        'get': 'getAllPengadaan'
    }), name='all-pengadaan'),

    path('pengadaan/request/upload-invoice/<str:pengadaan_id>', PengadaanViewSet.as_view({
        'post': 'uploadInvoiceFile'
    }), name='upload-invoice-file'),

    path('pengadaan/request/upload-payment/<str:pengadaan_id>/', PengadaanViewSet.as_view({
        'post': 'uploadPaymentFile'
    }), name='upload-payment-file'),

    path('dashboard/stafpengadaan', DashboardViewSet.as_view({
        'get': 'getDataDashboardStafPengadaan'
    })),
    path('dashboard/adminimpor', DashboardViewSet.as_view({
        'get': 'getDataDashboardAdminImpor'
    })),
]
