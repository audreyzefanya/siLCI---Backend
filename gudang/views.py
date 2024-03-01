from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Gudang
from .serializers import GudangSerializer

class GudangViewSet(viewsets.ViewSet):
    def listGudang(self, request):
        gudang = Gudang.objects.all()
        serializer = GudangSerializer(gudang, many=True)
        return Response(serializer.data)

    def createGudang(self, request):
        serializer = GudangSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)