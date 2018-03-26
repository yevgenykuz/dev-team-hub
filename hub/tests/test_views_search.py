from django.test import TestCase
from django.urls import reverse
from forum.models import Post, Topic, Category
from news.models import Article
from wiki.models import Entry, Section


class SearchViewTests(TestCase):
    def setUp(self):
        self.search_text = 'search this'
        self.search_form_data = {'search_q': self.search_text}
        self.false_search_text = 'not found'
        self.false_search_form_data = {'search_q': self.false_search_text}

    def test_search_for_news_article(self):
        news_article = Article.objects.create(title=self.search_text, body='Some text', publish=True)
        response = self.client.get(reverse('search'), self.search_form_data)
        self.assertIn(news_article, response.context['news_articles'])

    def test_search_for_wiki_entry(self):
        wiki_section = Section.objects.create(name='Generic', description='Generic stuff')
        wiki_entry = Entry.objects.create(name=self.search_text, value="Some text", publish=True, section=wiki_section)
        response = self.client.get(reverse('search'), self.search_form_data)
        self.assertIn(wiki_entry, response.context['wiki_entries'])

    def test_search_for_forum_post(self):
        forum_category = Category.objects.create(name='Generic', description='Generic stuff')
        forum_topic = Topic.objects.create(subject='Test topic', category=forum_category)
        forum_post = Post.objects.create(body=self.search_text, topic=forum_topic)
        response = self.client.get(reverse('search'), self.search_form_data)
        self.assertIn(forum_post, response.context['forum_posts'])

    def test_false_search_for_news_article(self):
        response = self.client.get(reverse('search'), self.false_search_form_data)
        self.assertEquals(response.context['news_articles'].count(), 0)

    def test_false_search_for_wiki_entry(self):
        response = self.client.get(reverse('search'), self.false_search_form_data)
        self.assertEquals(response.context['wiki_entries'].count(), 0)

    def test_false_search_for_forum_post(self):
        response = self.client.get(reverse('search'), self.false_search_form_data)
        self.assertEquals(response.context['forum_posts'].count(), 0)
