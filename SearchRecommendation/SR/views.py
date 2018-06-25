# _*_ coding: utf-8 _*_

from django.http import  HttpResponse,HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django import  forms
from django .forms import fields
from SR.query import get_content_list

from SR.query import get_content_book_list
from SR.query import get_content_game_list

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
    list_type = request.POST.get('list_type',False)
    print(list_type)

    if list_type =="电影":
        search_all_result = get_content_list(search_txt)
        return render_to_response('film_Result.html', {'searchtxt': search_all_result})
    elif list_type =="图书":
        search_all_result = get_content_book_list(search_txt)
        return render_to_response('book_Result.html', {'searchtxt': search_all_result})
    else:
        search_all_result = get_content_game_list(search_txt)
        return render_to_response('game_Result.html', {'searchtxt': search_all_result})
    #search_all_result = get_content_list(search_txt)
    #return render_to_response('ResultList.html', {'searchtxt': search_all_result})










