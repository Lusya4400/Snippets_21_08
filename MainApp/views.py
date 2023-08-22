from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from django.core.exceptions import ObjectDoesNotExist


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    context = {'pagename': 'Добавление нового сниппета'}
    return render(request, 'pages/add_snippet.html', context)


def snippets_page(request):
    snippets = Snippet.objects.all()
    len_s = len(snippets)
    if snippets:
        context = {'pagename': 'Просмотр сниппетов',
                'snippets': snippets,
                'num' : len_s
        }
    else:
        context = {'pagename': 'Просмотр сниппетов',
        }
    return render(request, 'pages/view_snippets.html', context)
