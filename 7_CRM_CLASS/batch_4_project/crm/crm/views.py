
from django.http import HttpResponse
from django.shortcuts import render
def demo(req):
    print("hellow world")
    return HttpResponse(f"this is a demo function, {req.method}")
def demo2(req):
    print("hellow world")
    return HttpResponse(f"this is a demo2 function, {req.method}")

def register(req):
    return render(req,'signup.html')
