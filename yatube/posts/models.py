from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название группы',
        help_text=(
            'Может состоять из символов латиницы и кириллицы, '
            'а также содержать цифры'
        ),
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Уникальная строка идентификатор группы',
        help_text=(
            'Может состоять только из символов латиницы в нижнем '
            'регистре, а также цифр'
        ),
    )
    description = models.TextField(
        verbose_name='Описание группы',
        help_text=(
            'Краткое описание группы, чтобы можно было понять '
            'какие записи размещают в этой группе'
        ),
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст записи',
        help_text='Напиши о чем угодно, но не обижай других пользователей',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания записи',
        help_text=(
            'Указывает на время создания записи. Автоматически '
            'проставляется текущее время, если не указана другая дата'
        ),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор записи',
        help_text=(
            'Пользователь, создавший запись. Только он имеет права'
            'на её редактирование'
        ),
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа',
        help_text=(
            'Группа, в которой будет размещена запись.'
            'Необязательное поле.'
        ),
    )
    image = models.ImageField(
        verbose_name='Картинка',
        help_text='Картинка будет размещена вверху поста.',
        upload_to='posts/',
        blank=True,
    )

    def __str__(self):
        return self.text[:15]

    class Meta:
        ordering = ('-pub_date',)


class Comments(models.Model):
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Напиши о чем угодно, но не обижай других пользователей',
        blank=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания комментария',
        help_text=(
            'Указывает на время создания комментария. Автоматически '
            'проставляется текущее время, если не указана другая дата'
        ),
    )
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.CASCADE,
    )
