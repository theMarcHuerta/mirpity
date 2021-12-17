from django.shortcuts import render
import requests
import sys
from subprocess import run,PIPE

def button(request):
    return render(request, 'home.html')

def output(request):
    data=requests.get("https://reqres.in/api/users")
    print(data.text)
    data=data.text
    return render(request, 'home.html', {'data':data})

def external(request):
    inp = request.POST.get('param')
#     out = run([sys.executable,'//Users//ironmacbookair//Desktop//twtproj//twtproj//twt_code.py', inp], shell=False, stdout=PIPE)
    out = run([sys.executable,'//twt_code.py', inp], shell=False, stdout=PIPE)
    rout = str(out.stdout) + "HELLO"
    return render(request, 'home.html', {'data1':rout})

