from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Task, Category, Comment

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class TaskForm(forms.ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['categories'].queryset = Category.objects.filter(user=user)

    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'priority', 'categories', 'status']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'categories': forms.CheckboxSelectMultiple(),
            'status': forms.Select(),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a comment...'})
        }