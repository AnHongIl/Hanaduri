from django.shortcuts import render
from django.http import HttpResponse
from apps.models import Writings
import pickle
import json
import socket

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return HttpResponse("Hello, World.")

def writings(request):
    dict_writings = []
    for w in Writings.objects.all():
        dict_writing = {}
        dict_writing['title'] = w.title
        dict_writing['body'] = w.body
        dict_writing['administration'] = w.administration
        dict_writing['legislature'] = w.legislature
        dict_writings.append(dict_writing)
    return HttpResponse(json.dumps(dict_writings, ensure_ascii=False))

@csrf_exempt
def keywords(request):
    if request.method == "POST":
        try:
            print(request.body)
            title = request.POST.get("title")
            print("In django, received from client: {}".format(title))

            if title == '' or title == None:
                return HttpResponse("title is null")
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('', 8001))
            sock.send(title.encode("UTF-8"))
            keywords = pickle.loads(sock.recv(2000))
            print("In django received from keywords {}".format(keywords))
            string = ""
            for keyword in keywords:
                string += keyword + ","
            print("In django send to client {}".format(string))
        except:
            return HttpResponse("Error ;;;;;;;;")
        return HttpResponse(string)
    """
    server_socket = socket.socket(socket.AF_INET, socekt.SOCK_STREAM)
    server_socket.bind('', 8000)
    server_socket.listen(1)
    client_socket, addr = server_socket.accept()

    client_socket.send(
    """
    return HttpResponse("Hello keywords")

@csrf_exempt
def recommendations(request):
    if request.method == "POST":
        try:
            title = request.POST.get("title")
            body = request.POST.get("body")

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('', 8002))
            dic = {}
            dic['title'] = title
            dic['body'] = body
            print("In django, send to recommendations dic: {}".format(dic))
            sock.send(pickle.dumps(dic))
            print("In django, Send title & body to recommendations")
            data = sock.recv(2000)
            results = pickle.loads(data)
            print("In django, Received from recommendations result: {}".format(results))

            administration = None
            legislature = None
            if results == "안전/환경":
                administration = "행정안전부"
                legislature = "박주민"
            else:
                administration="과학기술정통부"
                legislature= "노웅래"
            results += ',' + administration + ',' + legislature
            return HttpResponse(results)
        except:
            return HttpResponse("recommendations error")
    return HttpResponse("Send a POST request")

@csrf_exempt
def write(request):
    if request.method == 'POST':
        try:
            title = request.POST.get("title")
            body = request.POST.get("body")
            category = request.POST.get("category")
            administration = request.POST.get("administration")
            legislature = request.POST.get("legislature")
            keywords = request.POST.get("keywords")
            print(title)
            print(body)
            print(category)
            print(administration)
            print(legislature)
            print(keywords)
            wt = Writings(title=title, body=body, category=category, administration=administration, legislature=legislature, keywords=keywords)
            wt.save()
        except:
            return HttpResponse("write error")
    return HttpResponse(title + " is saved")

def delete(request):
    pk = Writings.objects.latest('id').id
    wt = Writings.objects.get(pk=pk)
    title = wt.title
    wt.delete()
    return HttpResponse(title + " is deleted")
