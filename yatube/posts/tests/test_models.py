from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст',
        )

    def test_post_str_method(self):
        """Метод __str__ для Post возвращает ожидаемое значение"""
        self.assertEqual(
            str(PostModelTest.post),
            PostModelTest.post.text[:15],
            'Метод __str__ для Post возвращает некорректное значение',
        )

    def test_post_verbone_name(self):
        """verbose_name в полях Post совпадает с ожидаемым."""
        post = PostModelTest.post
        field_verboses = {
            'text': 'Текст записи',
            'pub_date': 'Дата создания записи',
            'author': 'Автор записи',
            'group': 'Группа',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name, expected)

    def test_post_help_text(self):
        """help_text в полях Post совпадает с ожидаемым."""
        post = PostModelTest.post
        field_help_texts = {
            'text': 'Напиши о чем угодно, но не обижай других пользователей',
            'pub_date': ('Указывает на время создания записи. Автоматически '
                         'проставляется текущее время, если не указана '
                         'другая дата'),
            'author': ('Пользователь, создавший запись. Только он имеет права'
                       'на её редактирование'),
            'group': ('Группа, в которой будет размещена запись.'
                      'Необязательное поле.'),
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text, expected)


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )

    def test_group_str_method(self):
        """Метод __str__ для Group возвращает ожидаемое значение"""
        self.assertEqual(
            str(GroupModelTest.group),
            GroupModelTest.group.title,
            'Метод __str__ для Group возвращает некорректное значение',
        )

    def test_group_verbone_name(self):
        """verbose_name в полях Group совпадает с ожидаемым."""
        group = GroupModelTest.group
        field_verboses = {
            'title': 'Название группы',
            'slug': 'Уникальная строка идентификатор группы',
            'description': 'Описание группы',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).verbose_name, expected)

    def test_group_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        group = GroupModelTest.group
        field_help_texts = {
            'title': ('Может состоять из символов латиницы и кириллицы, '
                      'а также содержать цифры'),
            'slug': ('Может состоять только из символов латиницы в нижнем '
                     'регистре, а также цифр'),
            'description': ('Краткое описание группы, чтобы можно было понять '
                            'какие записи размещают в этой группе'),
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).help_text, expected)
