from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.conf import settings

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtailtrans.models import TranslatablePage
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from django.conf import settings 
from ictcg.streams import blocks

class HomePage(TranslatablePage):
    """
    Homepage class
    """

    parent_page_types = ["wagtailtrans.TranslatableSiteRootPage"]
    subpage_types = [
        "guidelines.GuidelinesListingPage", 
        "base.GenericPageWithSubNav", 
        "case_studies.CaseStudiesListingPage", 
        "base.CookiePage", 
        "base.GenericPage",
        "sponsors.SponsorsPage"
    ]

    masthead_title = models.CharField(
        max_length=240,
        null=True,
        help_text=_("Title for masthead component")
    )

    masthead_description = RichTextField(blank=True, default="")

    masthead_link = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL
    )

    masthead_link_title = models.CharField(
        max_length=240,
        null=True,
        blank=True,
        help_text=_("Title for link")
    )

    masthead_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )

    masthead_image_description = models.CharField(
        max_length=240,
        null=True,
        blank=True,
        help_text=_("Alt tag description for image")
    )

    body = StreamField([
        ("rich_text_section", blocks.HomePageRichTextBlock()),
        ("highlight_list_section", blocks.HighlightListBlock()),
        ("case_study_section", blocks.CaseStudyBlock()),
        ("sponsors_section", blocks.HomePageRichTextBlock(template = "streams/homepage_sponsors_block.html")),
    ], null=True, blank=True)

    content_panels = TranslatablePage.content_panels + [
        StreamFieldPanel("body"),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("masthead_title"),
                FieldPanel("masthead_description"),
                PageChooserPanel("masthead_link"),
                FieldPanel("masthead_link_title"),
                ImageChooserPanel("masthead_image"),
                FieldPanel("masthead_image_description"),
            ],
            heading=_('Masthead'),
        ),
        StreamFieldPanel("body"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('masthead_title'),
        index.SearchField('masthead_description'),
        index.SearchField('body'),
    ]

    def clean(self):
        super().clean()
        if self.masthead_image and not self.masthead_image_description:
            raise ValidationError({
            'masthead_image_description': _("Please enter description for the masthead image"), 
        })

class GenericPageWithSubNav(TranslatablePage):
    """
    Generic page class which allows rich text and quote components to be added.  Can only be added under the homepage but can be nested itself.
    Page includes a sub navigation on the left of the layout for quick links to content on the page. This is auto genereated based on the body components.
    """

    parent_page_types = ["base.HomePage", "base.GenericPageWithSubNav", "base.GenericPage"]
    subpage_types = ["base.GenericPageWithSubNav", "base.GenericPage", "sponsors.SponsorsPage"]

    navigation_title = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        help_text=_("Title for Navigation")
    )

    body = StreamField([
        ("rich_text_section", blocks.RichTextWithTitleBlock()),
        ("quote_section", blocks.QuoteBlock()),
    ], null=True, blank=True)

    content_panels = TranslatablePage.content_panels + [
        FieldPanel("navigation_title"),
        StreamFieldPanel("body"),
    ]

class GenericPage(TranslatablePage):
    """
    Generic page class which allows rich text and quote components to be added.
    Similar page to GenericPageWithSubNav but does not include the sub-navigation component.
    """

    parent_page_types = ["base.HomePage", "base.GenericPageWithSubNav", "base.GenericPage"]
    subpage_types = ["base.GenericPageWithSubNav", "base.GenericPage", "sponsors.SponsorsPage"]

    introduction = RichTextField(blank=True, default="")

    body = StreamField([
        ("rich_text_section", blocks.RichTextWithTitleBlock()),
        ("quote_section", blocks.QuoteBlock()),
    ], null=True, blank=True)

    content_panels = TranslatablePage.content_panels + [
        FieldPanel("introduction"),
        StreamFieldPanel("body"),
    ]

class CookiePage(TranslatablePage):
    """
    Simple page class which allows doe rich text content.  Also allow analytics consent form to be added to the page.  Can only be added under the homepage with no children.
    Overrides the default serve method to allow for setting cookie permissions
    """

    subpage_types = []
    ajax_template = "base/cookie_page_ajax.html"

    introduction = RichTextField(blank=True, default="")

    body = StreamField([
        ("cookie_section", blocks.CookieTableBlock()),
        ("Analtyics_cookie_section", blocks.CookieTableBlock(template="streams/analytics_cookie_block.html")),
    ], null=True, blank=True)

    content_panels = TranslatablePage.content_panels + [
        FieldPanel("introduction"),
        StreamFieldPanel("body"),
    ]

    def serve(self, request, *args, **kwargs):
        response = super().serve(request, *args, **kwargs)
        if request.method == 'POST':
            analytics = request.POST.get("analytics", "false")
            response.set_cookie('cookie_notice', "true", max_age=settings.COOKIE_MAX_AGE)
            response.set_cookie('analytics', analytics, max_age=settings.COOKIE_MAX_AGE)
            if analytics == 'false':
                # Delete any analytics cookies if the user opts out
                domain = request.META['HTTP_HOST'].replace("www", "")
                response.delete_cookie(('_gat_gtag_%s' % settings.ANALYTICS_ID).replace("-", "_"), domain=domain)
                response.delete_cookie('_ga', domain=domain)
                response.delete_cookie('_gid', domain=domain)
                
            request.COOKIES['analytics'] = analytics

        return response
