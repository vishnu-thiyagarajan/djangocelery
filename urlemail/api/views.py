# Create your views here.
from rest_framework import generics
from urlemail.models import Actions
from .serializers import ActionSerializer
# from django.core.mail.message import EmailMessage
from .tasks import downloadandemail


class CreateDownloadAndEmail(generics.CreateAPIView):
    lookup_feild = 'pk'
    serializer_class = ActionSerializer

    def perform_create(self, serializer):
        downloadandemail.delay(data=serializer.validated_data)
        serializer.save()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DownloadAndEmail(generics.RetrieveUpdateDestroyAPIView):
    lookup_feild = 'pk'
    serializer_class = ActionSerializer

    def get_object(self):
        pk = self.kwargs.get("pk")
        val = Actions.objects.get(pk=pk)
        val.urls = val.urls[1:-1].split(',')
        return val
