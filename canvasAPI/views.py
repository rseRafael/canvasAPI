from django.http import HttpResponse, JsonResponse
import json

def test(request):
    myJson = {"content": "Hello, World"}
    res = JsonResponse(myJson)
    res['Access-Control-Allow-Origin'] = "*"
    return res