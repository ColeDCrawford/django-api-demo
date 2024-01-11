from django.shortcuts import render
from api.serializers import AmendmentSerializer
from rest_framework import viewsets
from api.models import Amendment

# Create your views here.

def home(request):
    amendments = Amendment.objects.all() # we can sort and filter here too
    context = {'amendments': amendments}
    return render(request, 'home.html', context=context)

class AmendmentViewSet(viewsets.ModelViewSet):
    queryset = Amendment.objects.all() # we can sort and filter here too
    serializer_class = AmendmentSerializer