from django.shortcuts import render
from django.http import HttpResponseBadRequest
from rest_framework.decorators import api_view
# Create your views here.


ACCEPTED_TOKEN = ('omni_pretest_token')


@api_view(['POST'])
def import_order(request):
    # Add your code here
    return HttpResponseBadRequest()