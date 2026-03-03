from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.http import HttpResponseRedirect
from .models import Task, Category, Comment
from .forms import TaskForm, CategoryForm, CommentForm, RegisterForm

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

# Task Views
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        qs = Task.objects.filter(user=self.request.user)
        status = self.request.GET.get('status', 'all')
        if status == 'completed':
            qs = qs.filter(is_completed=True)
        elif status in ('todo', 'in_progress'):
            qs = qs.filter(is_completed=False)
        category_id = self.request.GET.get('category')
        if category_id and str(category_id).isdigit():
            qs = qs.filter(categories__id=int(category_id)).distinct()
        return qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base = Task.objects.filter(user=self.request.user)
        now = timezone.now()
        today = now.date()
        tomorrow = today + timedelta(days=1)
        context['tasks_remaining_today'] = base.filter(
            is_completed=False, deadline__date=today
        ).count()
        context['active_status'] = self.request.GET.get('status', 'all')
        context['today'] = today
        context['tomorrow'] = tomorrow
        context['today_str'] = today.isoformat()
        context['tomorrow_str'] = tomorrow.isoformat()
        context['now'] = now
        return context

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task-list')
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

@login_required
def toggle_task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.is_completed = not task.is_completed
    task.save()
    url = reverse('task-list')
    if request.GET:
        url += '?' + request.GET.urlencode()
    return HttpResponseRedirect(url)

# Category Views
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'tasks/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'tasks/category_form.html'
    success_url = reverse_lazy('category-list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# Comment View
@login_required
def add_comment(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.user = request.user
            comment.save()
    return redirect('task-detail', pk=pk)

# Home View
def home(request):
    if request.user.is_authenticated:
        return redirect('task-list')
    return render(request, 'base.html')