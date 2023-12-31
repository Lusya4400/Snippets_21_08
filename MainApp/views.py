from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from MainApp.models import Snippet, Comment
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import auth

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


@login_required
def my_snippets(request):
    snippets = Snippet.objects.filter(user=request.user)
    context = {
        'pagename': 'Мои сниппеты',
        'snippets': snippets,
        'count':snippets.count()
        }
    return render(request, 'pages/view_snippets.html', context)


@login_required
def add_snippet_page(request):
    # Получаем пустую форму
    if request.method == "GET":      
        form = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form
        }
        return render(request, 'pages/add_snippet.html', context)
 
    # Записываем новый снипет из данных формы
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            if request.user.is_authenticated:
                snippet.user = request.user
                snippet.save()
            return redirect("snippets-list")
        return render(request, 'pages/add_snippet.html', {'form': form})

def snippets_page(request):
    snippets = Snippet.objects.filter(public=True)

    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets,
        'count': snippets.count()
        }
    return render(request, 'pages/view_snippets.html', context)

def snippet_detail(request, snippet_id):
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except ObjectDoesNotExist:
        raise Http404
    comments = Comment.objects.filter(snippet_id=snippet_id)
    context ={'pagename': 'Просмотр сниппета',
            'snippet': snippet,
            'type': 'view',
            'comments': comments
    }
    return render(request, 'pages/snippet_detail.html', context)

def snippet_delete(request, snippet_id):
    snippet = Snippet.objects.get(id=snippet_id)
    snippet.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

def snippet_edit(request, snippet_id):
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except ObjectDoesNotExist:
        raise Http404
    # получаем данные сниппета
    if request.method == "GET":      
        context = {
            'pagename': 'Редактирование сниппета',
            'snippet': snippet,
            'type': "edit"
        }
        return render(request, 'pages/snippet_detail.html', context)
    
    #Новый сниппет
    if request.method == "POST":
        data_form = request.POST
        snippet.name = data_form["name"]
        snippet.lang = data_form["lang"]
        snippet.code = data_form["code"]
        snippet.creation_date = data_form["creation_date"]
        snippet.public = data_form.get("public", False)
        snippet.save()
        return redirect("snippets-list")

def create_user(request):
    context = {"pagename": "Регистрация пользователя"}
    if request.method == "GET":
        form = UserRegistrationForm()
        context["form"] = form
        return render(request, "pages/registration.html", context)
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        context['form'] = form
        return render(request, "pages/registration.html", context)



def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            context = {
                'pagename': 'PythonBin',
                'errors': ['wrong username or password']
            }
            return render(request, 'pages/index.html', context)
    return redirect('home')


def logout(request):
    auth.logout(request)
    return redirect(request.META.get("HTTP_REFERER", '/'))

@login_required
def comment_add(request, snippet_id):
    snippet = Snippet.objects.get(id=snippet_id)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.snippet = snippet
            comment.save()

        return redirect(f'/snippet/{snippet_id}')

    raise Http404

def comment_edit(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except ObjectDoesNotExist:
        raise Http404
    # получаем данные комментария
    snippet = Comment.snippet
    if request.method == "GET":      
        context = {
            'pagename': 'Редактирование Комментария',
            'snippet': snippet,
            'comment': comment
        }
        return render(request, 'pages/snippet_detail.html', context)
    
    # записываем новый комментарий
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.snippet = snippet
            comment.save()

        return redirect(f'/snippet/{snippet.id}')

def sort_up_lang(request):
    pass



# def create_snippet(request):
#     if request.method == "POST":
#        form = SnippetForm(request.POST)
#        if form.is_valid():
#           form.save()
#           return redirect("snippets-list")
#        return render(request,'add_snippet.html', {'form': form})

