import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Comment, Follow, Group, Post

User = get_user_model()
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


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
        cache.clear()

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
        cache.clear()

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


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ContextTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='testuser')
        cls.user_2 = User.objects.create(username='testuser_2')
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
        cls.test_image = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.test_uploaded = SimpleUploadedFile(
            name='test_image.jpg',
            content=ContextTests.test_image,
            content_type='image/gif'
        )
        cls.post = Post.objects.create(
            author=ContextTests.user,
            text='Тестовый пост',
            group=ContextTests.group,
            image=ContextTests.test_uploaded
        )
        cls.comment = Comment.objects.create(
            author=ContextTests.user,
            text='Тестовый комментарий',
            post=ContextTests.post,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.auth_client = Client()
        self.auth_client.force_login(ContextTests.user)
        cache.clear()

    def posts_equals(self, post):
        """Сравнение двух постов по значениям text, group, author, image"""
        self.assertEqual(self.post.text, post.text)
        self.assertEqual(self.post.group, post.group)
        self.assertEqual(self.post.author, post.author)
        self.assertEqual(self.post.image, post.image)

    def test_index_page_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.auth_client.get(reverse('posts:index'))
        post_on_page = response.context['page_obj'][0]
        self.posts_equals(post_on_page)

    def test_group_page_context(self):
        """Шаблон group сформирован с правильным контекстом."""
        response = self.auth_client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': ContextTests.group.slug},
            )
        )
        post_on_page = response.context['page_obj'][0]
        self.posts_equals(post_on_page)

    def test_profile_page_context(self):
        """Проверка страницы профиля: приходит правильный список постов"""
        response = self.auth_client.get(
            reverse(
                'posts:profile',
                kwargs={'username': ContextTests.user.username},
            )
        )
        post_on_page = response.context['page_obj'][0]
        self.posts_equals(post_on_page)

    def test_post_detail_page(self):
        """Проверка страницы поста: правильный пост и комментарий"""
        response = self.auth_client.get(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': ContextTests.post.id}
            )
        )
        self.posts_equals(response.context['post'])
        comment = response.context['comments'][0]
        self.assertEqual(comment.author, ContextTests.comment.author)
        self.assertEqual(comment.text, ContextTests.comment.text)
        self.assertEqual(comment.post, ContextTests.comment.post)
        self.assertEqual(comment.created, ContextTests.comment.created)

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

    def test_follow(self):
        """Проверка того, что пользователь может подписываться на авторов"""
        self.auth_client.get(
            reverse(
                'posts:profile_follow',
                kwargs={'username': self.user_2.username},
            )
        )
        following = self.user.follower.filter(
            author=self.user_2,
            user=self.user,
        ).exists()
        self.assertTrue(following)

    def test_unfollow(self):
        """Проверка того, что пользователь может отписываться от авторов"""
        Follow.objects.create(
            user=ContextTests.user,
            author=ContextTests.user_2
        )
        self.auth_client.get(
            reverse(
                'posts:profile_unfollow',
                kwargs={'username': self.user_2.username},
            )
        )
        following = self.user.follower.filter(
            author=self.user_2,
            user=self.user,
        ).exists()
        self.assertFalse(following)

    def test_follow_page(self):
        """Проверяем, что при подписке посты появляются на странице"""
        self.auth_client.force_login(user=self.user_2)
        response = self.auth_client.get(
            reverse('posts:follow_index')
        )
        post_on_page = response.context['page_obj']
        self.assertEqual(len(post_on_page), 0)
        self.auth_client.get(
            reverse(
                'posts:profile_follow',
                kwargs={'username': self.user.username},
            )
        )

        response = self.auth_client.get(
            reverse('posts:follow_index')
        )
        post_on_page = response.context['page_obj']
        self.assertEqual(len(post_on_page), 1)


class CacheTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='test_user')

    def setUp(self):
        self.guest_client = Client()
        self.post = Post.objects.create(
            author=CacheTests.user,
            text='Тестовый пост',
        )

    def test_index_page_cache(self):
        """Тестирование работы кэширования на главной странице"""
        first_response = self.guest_client.get(reverse('posts:index'))
        self.post.delete()
        response = self.guest_client.get(reverse('posts:index'))
        self.assertEqual(first_response.content, response.content)
        cache.clear()
        response = self.guest_client.get(reverse('posts:index'))
        self.assertNotEqual(first_response.content, response.content)
