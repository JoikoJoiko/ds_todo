from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import AuthenticationForm

from .forms import RegisterForm, TaskForm
from .models import Task


def index(request):
    if request.user.is_authenticated:
        tasks_count = Task.objects.filter(user=request.user).count()
        done_count = Task.objects.filter(user=request.user, status='done').count()
        active_count = Task.objects.filter(user=request.user).exclude(status='done').count()
    else:
        tasks_count = 0
        done_count = 0
        active_count = 0

    context = {
        'tasks_count': tasks_count,
        'done_count': done_count,
        'active_count': active_count,
    }

    return render(request, 'todo/index.html', context)


def about(request):
    return render(request, 'todo/about.html')


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)

    status = request.GET.get('status')
    priority = request.GET.get('priority')
    category = request.GET.get('category')

    if status:
        tasks = tasks.filter(status=status)

    if priority:
        tasks = tasks.filter(priority=priority)

    if category:
        tasks = tasks.filter(category=category)

    context = {
        'tasks': tasks,
        'selected_status': status,
        'selected_priority': priority,
        'selected_category': category,
    }

    return render(request, 'todo/task_list.html', context)


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    return render(request, 'todo/task_detail.html', {
        'task': task
    })


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()

            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm()

    return render(request, 'todo/task_form.html', {
        'form': form,
        'title': 'Новая задача',
        'button_text': 'Создать задачу'
    })


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)

    return render(request, 'todo/task_form.html', {
        'form': form,
        'title': 'Редактирование задачи',
        'button_text': 'Сохранить изменения'
    })


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('task_list')

    return render(request, 'todo/task_confirm_delete.html', {
        'task': task
    })

@login_required
def task_toggle_done(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        if task.status == 'done':
            task.status = 'in_progress'
        else:
            task.status = 'done'

        task.save()

    return redirect('task_list')

def register(request):
    if request.user.is_authenticated:
        return redirect('task_list')

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = RegisterForm()

    return render(request, 'todo/register.html', {
        'form': form
    })

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите логин'
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })

class CustomLoginView(LoginView):
    template_name = 'todo/login.html'
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    next_page = 'index'
