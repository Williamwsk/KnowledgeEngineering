# _*_ coding: utf-8 _*_

from django.http import  HttpResponse,HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django import  forms
from SR.query import get_content_list

# Create your views here.
#def hello(request):
#    context = {}
#    context['hello'] =  'Hello World!'
#    return render(request,'Search.html',context)
#    return  render(request,'Search.html')
class SearchForm(forms.Form):
    search_txt = forms.CharField()

def search(request):
    search_txt = 'NULL'
    return render_to_response('Search.html',{'search_txt':search_txt})

def click_search(request):
    search_txt = request.POST['search_txt']
    search_all_result = get_content_list(search_txt)
    return render_to_response('Result.html',{'searchtxt':search_all_result})






