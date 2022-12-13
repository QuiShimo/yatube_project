from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from posts.views import Group, Post

User = get_user_model()


class PostsURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testuser')
        cls.user_2 = User.objects.create_user(username='testuser_2')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='testgroup',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст',
        )
        cls.page_and_template_for_guest = {
            '/': 'posts/index.html',
            '/group/testgroup/': 'posts/group_list.html',
            '/profile/testuser/': 'posts/profile.html',
            '/posts/1/': 'posts/post_detail.html',
        }
        cls.page_and_template_for_auth_user = {
            '/': 'posts/index.html',
            '/group/testgroup/': 'posts/group_list.html',
            '/profile/testuser/': 'posts/profile.html',
            '/posts/1/': 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
        }

    def setUp(self):
        self.guest_client = Client()
        self.auth_client = Client()
        self.auth_client.force_login(PostsURLTest.user)

    def test_posts_url_correct_for_guest(self):
        '''
        Проверка доступности страниц приложения posts
        для неавторизованных пользователей
        '''
        urls_lists = PostsURLTest.page_and_template_for_guest

        for urls in urls_lists:
            with self.subTest(value=urls):
                response = self.guest_client.get(urls)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_posts_template_correct_for_guest(self):
        '''
        Проверка корректности шаблона для страниц приложения posts
        для неавторизованных пользователей
        '''
        urls_lists = PostsURLTest.page_and_template_for_guest
        for urls, template in urls_lists.items():
            with self.subTest(value=urls):
                response = self.guest_client.get(urls)
                self.assertTemplateUsed(response, template)

    def test_posts_redirect_for_guests(self):
        '''
        Проверка корректности переадресации для неавторизованных
        пользователей
        '''
        page_redirect_list = {
            '/posts/1/comment/': '/auth/login/?next=/posts/1/comment/',
            '/posts/1/edit/': '/auth/login/?next=/posts/1/edit/',
            '/create/': '/auth/login/?next=/create/',
        }
        for url, url_redirect in page_redirect_list.items():
            with self.subTest(value=url):
                response = self.guest_client.get(url)
                self.assertRedirects(response, url_redirect)

    def test_posts_404_for_guests(self):
        '''Проверка ошибки 404 для неавторизованных пользователей'''
        response = self.guest_client.get('/unexisting_page/')
        self.assertEquals(response.status_code, HTTPStatus.NOT_FOUND)

    def test_posts_url_correct_for_auth_user(self):
        '''
        Проверка доступности страниц приложения posts
        для авторизованных пользователей
        '''
        urls_list = PostsURLTest.page_and_template_for_auth_user
        for urls in urls_list:
            with self.subTest(value=urls):
                response = self.auth_client.get(urls)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_posts_template_correct_for_auth_user(self):
        '''
        Проверка корректности шаблона для страниц приложения posts
        для авторизованных пользователей
        '''
        urls_list = PostsURLTest.page_and_template_for_auth_user
        for urls, template in urls_list.items():
            with self.subTest(value=urls):
                response = self.auth_client.get(urls)
                self.assertTemplateUsed(response, template)

    def test_posts_redirect_for_auth(self):
        '''
        Проверка корректности переадресации для авторизованных
        пользователей: при переходе на страницу редактирования поста, где
        пользователь не автор - переадресация на страницу просмотра поста
        '''
        self.auth_client.force_login(PostsURLTest.user_2)
        response = self.auth_client.get('/posts/1/edit/')
        self.assertRedirects(response, '/posts/1/')

    def test_posts_404_for_auth(self):
        '''Проверка ошибки 404 для неавторизованных пользователей'''
        response = self.auth_client.get('/unexisting_page/')
        self.assertEquals(response.status_code, HTTPStatus.NOT_FOUND)
