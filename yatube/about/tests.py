from django.test import TestCase, Client


class StaticURLTest(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_author_url_correct(self):
        '''Проверка доступности адреса страниц /about/*'''
        page_and_template_list = {
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html',
        }
        for urls in page_and_template_list.keys():
            with self.subTest(value=urls):
                response = self.guest_client.get(urls)
                self.assertEqual(response.status_code, 200)

    def test_author_template_correct(self):
        '''Проверка шаблона для адреса страниц /about/*'''
        page_and_template_list = {
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html',
        }
        for urls, template in page_and_template_list.items():
            with self.subTest(value=urls):
                response = self.guest_client.get(urls)
                self.assertTemplateUsed(response, template)
