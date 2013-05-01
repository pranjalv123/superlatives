from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from models import *
import json

uname = 'pranjal'
def getSuperlatives(request):
    #uname =request.META.get('HTTP_SSL_CLIENT_S_DN_EMAIL', '')
    superlatives = [i.toDict(uname) for i in Superlative.objects.all() if len(i.name) > 0 or i.owner.name == uname]
    return HttpResponse(json.dumps(superlatives))

def getSelections(request):
    #uname =request.META.get('HTTP_SSL_CLIENT_S_DN_EMAIL', '')
    user = User.objects.get_or_create(name=uname)[0]
    selections = [i.toDict()
                  for i in Selection.objects.filter(user=user)]
    return HttpResponse(json.dumps(selections))

def newSuperlative(request):
    #uname =request.META.get('HTTP_SSL_CLIENT_S_DN_EMAIL', '')
    user = User.objects.get_or_create(name=uname)[0]
    superlative = Superlative.objects.create(owner=user,
                                             name='',
                                             numfields=1)
    return HttpResponse(json.dumps(superlative.toDict(user)))

def updateSuperlative(request):
    #uname =request.META.get('HTTP_SSL_CLIENT_S_DN_EMAIL', '')
    user = User.objects.get_or_create(name=uname)[0]
    name = request.POST['name']
    num = request.POST['num']
    pk = request.POST['id']
    superlative = Superlative.objects.get(pk=pk)
    superlative.name = name
    superlative.numfields = num
    superlative.save()
    return HttpResponse("got")

def deleteSuperlative(request):
    #uname =request.META.get('HTTP_SSL_CLIENT_S_DN_EMAIL', '')
    user = User.objects.get_or_create(name=uname)[0]
    pk = request.POST['id']
    superlative = Superlative.objects.get(pk=pk)
    otherpeople =Selection.objects.filter(superlative=superlative).exclude(user=user)
    if otherpeople.count() > 0:
        return HttpResponse("false")
    superlative.delete()
    return HttpResponse("deleted")

def updateSelection(request):
    #uname =request.META.get('HTTP_SSL_CLIENT_S_DN_EMAIL', '')
    user = User.objects.get_or_create(name=uname)[0]
    answer = request.POST['answer']
    index = request.POST['index']
    pk = request.POST['id']
    superlative = Superlative.objects.get(pk=pk)
    selection = Selection.objects.get_or_create(superlative=superlative,
                                                user=user,
                                                index=index)[0]
    selection.selection = answer
    print selection.index, selection.selection
    selection.save()
    return HttpResponse("got")

def index(request):
    #uname =request.META.get('HTTP_SSL_CLIENT_S_DN_EMAIL', '')
    return render(request, 'index.html', {'username': uname})
