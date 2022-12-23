from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Comment, Follow, Group, Post

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


class CommentModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='TestUser_213')
        cls.post = Post.objects.create(
            author=CommentModelTest.user,
            text='Тестовый пост',
        )
        cls.comment = Comment(
            author=CommentModelTest.user,
            post=CommentModelTest.post,
        )

    def test_comment_verbone_name(self):
        """verbose_name в полях Comment совпадает с ожидаемым."""
        comment = CommentModelTest.comment
        field_verboses = {
            'text': 'Текст комментария',
            'created': 'Дата создания комментария',
            'post': 'Пост',
            'author': 'Автор',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    comment._meta.get_field(value).verbose_name, expected)

    def test_comment_help_text(self):
        """help_text в полях Comment совпадает с ожидаемым."""
        comment = CommentModelTest.comment
        field_help_texts = {
            'text': 'Напиши о чем угодно, но не обижай других пользователей',
            'created': (
                'Указывает на время создания комментария. Автоматически '
                'проставляется текущее время, если не указана другая дата'
            ),
            'post': 'Указывает на пост, к которому создан комментарий.',
            'author': 'Указывает на автора, который создал комментарий.',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    comment._meta.get_field(value).help_text, expected)

    def test_comment_str_method(self):
        """Проверка, что метод __str__ возвращает первый 15 символов text"""
        self.assertEqual(
            str(CommentModelTest.comment),
            CommentModelTest.comment.text[:15],
        )


class FollowModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='TestUser_123')
        cls.author = User.objects.create(username='TestUser_321')
        cls.follow = Follow.objects.create(
            user=FollowModelTest.user,
            author=FollowModelTest.author,
        )

    def test_follow_verbone_name(self):
        """verbose_name в полях Follow совпадает с ожидаемым."""
        follow = FollowModelTest.follow
        field_verboses = {
            'user': 'Тот, кто подписывается',
            'author': 'Автор',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    follow._meta.get_field(value).verbose_name, expected)

    def test_follow_help_text(self):
        """help_text в полях Follow совпадает с ожидаемым."""
        follow = FollowModelTest.follow
        field_help_texts = {
            'user': 'Указывает на пользователя, который подписывается',
            'author': ('Указывает на автора, на которого '
                       'подписался пользователь.'),
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    follow._meta.get_field(value).help_text, expected)

    def test_follow_str_method(self):
        """Проверка, что метод __str__ возвращает первый 15 символов text"""
        self.assertEqual(
            str(FollowModelTest.follow),
            (f'{FollowModelTest.user.username} подписался '
             f'на {FollowModelTest.author.username}'),
        )
