from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post

User = get_user_model()


class PostsFromTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='testauthor')

    def setUp(self):
        self.auth_client = Client()
        self.auth_client.force_login(PostsFromTest.user)

    def test_create_post(self):
        """Проверка формы создания поста"""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый пост',
        }
        self.auth_client.post(
            reverse('posts:create_post'),
            data=form_data,
            follow=True,
        )
        posts = Post.objects.filter(
            author=PostsFromTest.user,
            text='Тестовый пост',
            group=None,
        )
        self.assertEqual(posts.count(), 1)
        self.assertNotEqual(posts_count, Post.objects.count())

    def test_edit_post(self):
        post = Post.objects.create(
            author=PostsFromTest.user,
            text='Тестовый текст',
        )
        post_count = Post.objects.count()
        post_id = post.id
        form_data = {'text': 'Новый тестовый текст'}
        self.auth_client.post(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': post_id},
            ),
            data=form_data,
            follow=True,
        )

        edit_post = Post.objects.get(id=post_id)
        self.assertEqual(edit_post.author, post.author)
        self.assertEqual(edit_post.text, 'Новый тестовый текст')
        self.assertEqual(edit_post.group, post.group)
        self.assertEqual(post_count, Post.objects.count())
