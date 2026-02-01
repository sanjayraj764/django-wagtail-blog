from django.db import models
from wagtail.models import Page
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from datetime import date

class BlogPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    template = "a_blog/blog_page.html"
    
    def get_context(self, request):
        """Provide paginated child articles to the template."""
        context = super().get_context(request)

        # Query live, specific child pages (articles) ordered by publication date
        articles_qs = self.get_children().live().specific().order_by('-first_published_at')

        # Paginate - adjust per_page as needed
        per_page = 12
        paginator = Paginator(articles_qs, per_page)
        page_num = request.GET.get('page')
        try:
            page_obj = paginator.get_page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)

        context['articles'] = page_obj.object_list
        context['page_obj'] = page_obj
        context['paginator'] = paginator
        context['is_paginated'] = page_obj.has_other_pages()

        return context


class ArticlePage(Page):
    intro = models.CharField(max_length=225)
    body = RichTextField(blank=True)
    description = models.CharField(max_length=255, blank=True)
    date = models.DateField("Post date", default=date.today)
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, null=True,related_name='+'
    )
    caption = models.CharField(blank=True, max_length=80)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('image'),
        FieldPanel('caption'),
        FieldPanel('body'),
        FieldPanel('description'),
        FieldPanel('date'),
    ]   