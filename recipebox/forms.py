from django import forms
from recipebox.models import Author, Recipe
from django.forms import ModelForm

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'time_required', 'instructions', 'author']

class AuthorAdd(forms.Form):
    name = forms.CharField(max_length=50)


class NewsItemAdd(forms.Form):
    title = forms.CharField(max_length=50)
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    description = forms.CharField(widget=forms.Textarea)
    instructions = forms.CharField(widget=forms.Textarea)
    prep_time = forms.CharField(max_length=50)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)