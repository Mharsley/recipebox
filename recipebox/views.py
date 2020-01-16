from django.shortcuts import render, HttpResponseRedirect, reverse
from django.utils import timezone
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from recipebox.models import RecipeItem, Author
from recipebox.forms import AuthorAdd, NewsItemAdd, LoginForm, RecipeForm


def index(request):
    html = 'index.html'
    recipes = RecipeItem.objects.all()
    return render(request, html, {'data': recipes})


@login_required
def recipe_item_view(request, key_id):
    html = 'item_page.html'
    recipe = RecipeItem.objects.get(pk=key_id)
    return render(request, html, {'data': recipe})

@login_required()
def add_recipe(request, *args, **kwargs):
    html = 'addauthor.html'

    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data['title'],
                description=data['description'],
                time_required=data['time_required'],
                instructions=data['instructions'],
                author=data['author']
            )
            return HttpResponseRedirect(reverse('homepage'))
    form = RecipeForm()

    return render(request,html,{'form': form})


def author_view(request, key_id):
    html = 'author_page.html'
    author = Author.objects.get(pk=key_id)
    items = RecipeItem.objects.all().filter(author=author)
    return render(request, html, {
        'author': author,
        'recipes': items
        })

@login_required
def add_author_view(request):
    html = "author_add.html"
    if request.method == 'POST':
        form = AuthorAdd(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Author.objects.create(name=data['name'])
        return HttpResponseRedirect(reverse('homepage'))
    form = AuthorAdd()
    return render(request, html, {'form': form})


def add_item_view(request):
    html = "item_add.html"
    if request.method == 'POST':
        form = NewsItemAdd(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            RecipeItem.objects.create(
                title=data['title'],
                author=data['author'],
                description=data['description'],
                prep_time=data['prep_time'],
                instructions=data['instructions'],
                post_date=timezone.now()
            )
            return HttpResponseRedirect(reverse('homepage'))
    form = NewsItemAdd()
    return render(request, html, {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'],
                password=data['password']
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('homepage'))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))
