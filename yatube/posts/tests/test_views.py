from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.conf import settings
from django import forms


from posts.models import Post, Group

User = get_user_model()


class PostsPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='testauthor')
        cls.user_2 = User.objects.create(username='testauthor_2')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='testgroup',
            description='Тестовое описание',
        )

        cls.group_2 = Group.objects.create(
            title='Тестовая группа 2',
            slug='testgroup2',
            description='Тестовое описание 2',
        )

        cls.post_2 = Post.objects.create(
                author=cls.user_2,
                text='Текст поста',
                group=cls.group_2,
            )

        for i in range(settings.POSTS_ON_PAGE + 5):
            cls.post = Post.objects.create(
                author=cls.user,
                text=f'Текст поста {i}',
                group=cls.group,
            )

    def setUp(self):
        self.auth_client = Client()
        self.auth_client.force_login(PostsPagesTests.user)

    def test_posts_pages_correct_template(self):
        correct_template_list = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group_list',
                kwargs={'slug': PostsPagesTests.group.slug}
                ): 'posts/group_list.html',
            reverse(
                'posts:profile',
                kwargs={'username': PostsPagesTests.user.username}
                ): 'posts/profile.html',
            reverse(
                'posts:post_detail',
                kwargs={'post_id': PostsPagesTests.post.id}
                ): 'posts/post_detail.html',
            reverse(
                'posts:post_edit',
                kwargs={'post_id': PostsPagesTests.post.id}
                ): 'posts/create_post.html',
            reverse('posts:create_post'): 'posts/create_post.html',
        }
        for reverse_name, template in correct_template_list.items():
            with self.subTest(value=reverse_name):
                response = self.auth_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        posts_list = Post.objects.all()[:settings.POSTS_ON_PAGE]
        response = self.auth_client.get(reverse('posts:index'))
        post_on_page = response.context.get('page_obj').object_list
        for i in range(len(posts_list)):
            with self.subTest(value=posts_list[i]):
                self.assertEqual(posts_list[i], post_on_page[i])

    def test_index_page_paginator(self):
        """
        В шаблон index передается правильный паджинатор
        """
        response = self.auth_client.get(reverse('posts:index'))
        self.assertEqual(
            len(response.context['page_obj']),
            settings.POSTS_ON_PAGE,
        )

    def test_index_page_paginator_five_records(self):
        """Проверка: на второй странице должно быть 5 постов"""
        response = self.auth_client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 6)

    def test_group_page_context(self):
        """Шаблон group сформирован с правильным контекстом."""
        posts_list = PostsPagesTests.group.posts.all()[:settings.POSTS_ON_PAGE]
        response = self.auth_client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': PostsPagesTests.group.slug},
            )
        )
        post_on_page = response.context.get('page_obj').object_list
        for i in range(len(posts_list)):
            with self.subTest(value=posts_list[i]):
                self.assertEqual(posts_list[i], post_on_page[i])

    def test_group_page_paginator(self):
        """Проверка страницы групп: передается правильный паджинатор"""
        response = self.auth_client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': PostsPagesTests.group.slug},
            )
        )
        self.assertEqual(
            len(response.context['page_obj']),
            settings.POSTS_ON_PAGE,
        )

    def test_group_page_paginator_five_posts(self):
        """Проверка страницы групп: на второй странице должно быть 5 постов"""
        response = self.auth_client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': PostsPagesTests.group.slug},
            ) + '?page=2'
        )
        self.assertEqual(len(response.context['page_obj']), 5)

    def test_profile_page(self):
        """Проверка страницы профиля: приходит правильный список постов"""
        posts_list = PostsPagesTests.user.posts.all()[:settings.POSTS_ON_PAGE]
        response = self.auth_client.get(
            reverse(
                'posts:profile',
                kwargs={'username': PostsPagesTests.user.username},
            )
        )
        post_on_page = response.context.get('page_obj').object_list
        for i in range(len(posts_list)):
            with self.subTest(value=posts_list[i]):
                self.assertEqual(posts_list[i], post_on_page[i])

    def test_profile_page_paginator_list_on_page(self):
        """Проверка страницы профиля: проверка количества постов на странице"""
        response = self.auth_client.get(
            reverse(
                'posts:profile',
                kwargs={'username': PostsPagesTests.user.username},
            )
        )
        self.assertEqual(
            len(response.context['page_obj']),
            settings.POSTS_ON_PAGE,
        )

    def test_profile_page_paginator_next_page(self):
        """Проверка страницы профиля: вторая страница содержит 5 постов"""
        response = self.auth_client.get(
            reverse(
                'posts:profile',
                kwargs={'username': PostsPagesTests.user.username},
            ) + '?page=2'
        )
        self.assertEqual(len(response.context['page_obj']), 5)

    def test_post_detail_page(self):
        """Проверка страницы поста: контекст"""
        post = PostsPagesTests.post
        response = self.auth_client.get(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': PostsPagesTests.post.id}
            )
        )
        self.assertEqual(response.context['post'], post)

    def test_create_post_form(self):
        """Проверка страницы создания поста: контекст"""
        response = self.auth_client.get(reverse('posts:create_post'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_edit_post_form(self):
        """Проверка страницы изменения поста: контекст"""
        response = self.auth_client.get(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': PostsPagesTests.post.id}
            )
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_group(self):
        """"Проверка, что созданный пост не попадает в другую группу"""
        response = self.auth_client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': PostsPagesTests.group_2.slug},
            )
        )
        f_post = response.context['page_obj'][0]
        post_text = f_post.text,
        post_group = f_post.group,
        post_author = f_post.author,

        self.assertNotEqual(post_text, PostsPagesTests.post.text)
        self.assertNotEqual(post_group, PostsPagesTests.post.group)
        self.assertNotEqual(post_author, PostsPagesTests.post.author)
