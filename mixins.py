from django.shortcuts import get_object_or_404
from rest_framework.response import Response

class DeepRetrListMixin:
    '''
    Foreign Key가 걸려있는 Model을 deep inspection할 수 있게 한다.
    Viewset에 상속하여 사용.
    API call시, get request에 /xyz/?deep=2 과 같은 식으로 사용.

    ex) class XYZViewSet(DeepRetrListMixin, viewsets.ModelViewSet)
    '''
    def retrieve(self, request, pk=None):
        qs = self.get_queryset()
        obj = get_object_or_404(qs, pk=pk)
        serializer = self.get_serializer(obj)

        deep = int(self.request.GET.get('deep', 0))
        self.serializer_class.Meta.depth = deep
        rs = serializer.data
        self.serializer_class.Meta.depth = 0

        return Response(rs)

    def list(self, request):
        qs = self.get_queryset()
        deep = int(self.request.GET.get('deep', 0))
        self.serializer_class.Meta.depth = deep
        serializer = self.get_serializer(qs, many=True)
        rs = serializer.data
        self.serializer_class.Meta.depth = 0
        return Response(rs)
