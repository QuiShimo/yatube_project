import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Comment, Group, Post

User = get_user_model()
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsFromTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='testauthor')
        cls.group = Group.objects.create(
            title='test',
            slug='test',
            description='test'
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.auth_client = Client()
        self.auth_client.force_login(PostsFromTest.user)

    def test_create_post(self):
        """Проверка формы создания поста"""
        posts_count = Post.objects.count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': 'Тестовый пост',
            'group': PostsFromTest.group.id,
            'image': uploaded,
        }
        self.auth_client.post(
            reverse('posts:create_post'),
            data=form_data,
            follow=True,
        )
        posts = Post.objects.filter(
            author=PostsFromTest.user,
            text='Тестовый пост',
            group=PostsFromTest.group,
            image='posts/small.gif',
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
        form_data = {
            'text': 'Новый тестовый текст',
            'group': PostsFromTest.group.id,
        }
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
        self.assertEqual(edit_post.group, PostsFromTest.group)
        self.assertEqual(post_count, Post.objects.count())


class CommentFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='TestUser_3333')
        cls.post = Post.objects.create(
            author=CommentFormTests.user,
            text='Тестовый пост'
        )

    def setUp(self):
        self.auth_client = Client()
        self.auth_client.force_login(CommentFormTests.user)

    def test_create_comment(self):
        """Проверка, что комментарий создается"""
        comment_count = Comment.objects.count()
        form_data = {
            'text': 'Тестовый комментарий'
        }
        self.auth_client.post(
            reverse(
                'posts:add_comment',
                kwargs={'post_id': CommentFormTests.post.id}
            ),
            data=form_data,
            follow=True,
        )

        comment = Comment.objects.filter(
            author=CommentFormTests.user,
            post=CommentFormTests.post,
            text='Тестовый комментарий',
        )

        self.assertEqual(comment.count(), 1)
        self.assertNotEqual(comment_count, comment.count())
