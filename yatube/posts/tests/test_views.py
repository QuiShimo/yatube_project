from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.conf import settings

from posts.models import Post, Group

User = get_user_model()


class TeamplateTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='testauthor')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='testgroup',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=TeamplateTests.user,
            text='Тестовый пост',
            group=TeamplateTests.group,
        )

    def setUp(self):
        self.auth_client = Client()
        self.auth_client.force_login(TeamplateTests.user)

    def test_posts_pages_correct_template(self):
        correct_template_list = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group_list',
                kwargs={'slug': TeamplateTests.group.slug}
            ): 'posts/group_list.html',
            reverse(
                'posts:profile',
                kwargs={'username': TeamplateTests.user.username}
            ): 'posts/profile.html',
            reverse(
                'posts:post_detail',
                kwargs={'post_id': TeamplateTests.post.id}
            ): 'posts/post_detail.html',
            reverse(
                'posts:post_edit',
                kwargs={'post_id': TeamplateTests.post.id}
            ): 'posts/create_post.html',
            reverse('posts:create_post'): 'posts/create_post.html',
        }
        for reverse_name, template in correct_template_list.items():
            with self.subTest(value=reverse_name):
                response = self.auth_client.get(reverse_name)
                self.assertTemplateUsed(response, template)


class PaginatorTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='testauthor')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='testgroup',
            description='Тестовое описание',
        )

        for i in range(settings.POSTS_ON_PAGE + 5):
            Post.objects.create(
                author=cls.user,
                text=f'Текст поста {i}',
                group=cls.group,
            )

    def setUp(self):
        self.auth_client = Client()
        self.auth_client.force_login(PaginatorTests.user)

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
        """
        Проверка: В шаблон index передается правильный паджинатор на 2 странице
        """
        posts = Post.objects.count() - settings.POSTS_ON_PAGE
        response = self.auth_client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), posts)

    def test_group_page_paginator(self):
        """Проверка страницы групп: передается правильный паджинатор"""
        response = self.auth_client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': PaginatorTests.group.slug},
            )
        )
        self.assertEqual(
            len(response.context['page_obj']),
            settings.POSTS_ON_PAGE,
        )

    def test_group_page_paginator_five_posts(self):
        """Проверка страницы групп: на второй странице должно быть 5 постов"""
        posts = PaginatorTests.group.posts.count() - settings.POSTS_ON_PAGE
        response = self.auth_client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': PaginatorTests.group.slug},
            ) + '?page=2'
        )
        self.assertEqual(len(response.context['page_obj']), posts)

    def test_profile_page_paginator_list_on_page(self):
        """Проверка страницы профиля: проверка количества постов на странице"""
        response = self.auth_client.get(
            reverse(
                'posts:profile',
                kwargs={'username': PaginatorTests.user.username},
            )
        )
        self.assertEqual(
            len(response.context['page_obj']),
            settings.POSTS_ON_PAGE,
        )

    def test_profile_page_paginator_next_page(self):
        """Проверка страницы профиля: вторая страница содержит 5 постов"""
        posts = PaginatorTests.user.posts.count() - settings.POSTS_ON_PAGE
        response = self.auth_client.get(
            reverse(
                'posts:profile',
                kwargs={'username': PaginatorTests.user.username},
            ) + '?page=2'
        )
        self.assertEqual(len(response.context['page_obj']), posts)


class ContextTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='testuser')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='testgroup',
            description='Тестовое описание',
        )
        cls.group_2 = Group.objects.create(
            title='Тестовая группа 2',
            slug='testgroup_2',
            description='Тестовое описание 2',
        )
        cls.post = Post.objects.create(
            author=ContextTests.user,
            text='Тестовый пост',
            group=ContextTests.group,
        )

    def setUp(self):
        self.auth_client = Client()
        self.auth_client.force_login(ContextTests.user)

    def posts_equals(self, post1, post2):
        """Сравнение двух постов по значениям text, group, author"""
        self.assertEqual(post1.text, post2.text)
        self.assertEqual(post1.group, post2.group)
        self.assertEqual(post1.author, post2.author)

    def test_index_page_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.auth_client.get(reverse('posts:index'))
        post_on_page = response.context['page_obj'][0]
        self.posts_equals(ContextTests.post, post_on_page)

    def test_group_page_context(self):
        """Шаблон group сформирован с правильным контекстом."""
        response = self.auth_client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': ContextTests.group.slug},
            )
        )
        post_on_page = response.context['page_obj'][0]
        self.posts_equals(ContextTests.post, post_on_page)

    def test_profile_page_context(self):
        """Проверка страницы профиля: приходит правильный список постов"""
        response = self.auth_client.get(
            reverse(
                'posts:profile',
                kwargs={'username': ContextTests.user.username},
            )
        )
        post_on_page = response.context['page_obj'][0]
        self.posts_equals(ContextTests.post, post_on_page)

    def test_post_detail_page(self):
        """Проверка страницы поста: контекст"""
        response = self.auth_client.get(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': ContextTests.post.id}
            )
        )
        self.posts_equals(response.context['post'], ContextTests.post)

    def test_post_group(self):
        """"Проверка, что созданный пост не попадает в другую группу"""
        response = self.auth_client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': ContextTests.group_2.slug},
            )
        )
        posts_group_2 = response.context['page_obj']
        self.assertEqual(len(posts_group_2), 0)
