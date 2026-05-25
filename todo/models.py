from django.conf import settings
from django.db import models
from django.urls import reverse


class Task(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В процессе'),
        ('done', 'Выполнена'),
        ('archived', 'В архиве'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
        ('critical', 'Критический'),
    ]

    CATEGORY_CHOICES = [
        ('study', 'Учёба'),
        ('work', 'Работа'),
        ('home', 'Дом'),
        ('personal', 'Личное'),
        ('other', 'Другое'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='Пользователь'
    )

    title = models.CharField('Название задачи', max_length=200)
    description = models.TextField('Описание', blank=True)

    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )

    priority = models.CharField(
        'Приоритет',
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium'
    )

    category = models.CharField(
        'Категория',
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other'
    )

    deadline = models.DateField('Срок выполнения', null=True, blank=True)
    is_favorite = models.BooleanField('Избранное', default=False)

    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['status', '-is_favorite', 'deadline', '-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task_detail', kwargs={'pk': self.pk})
