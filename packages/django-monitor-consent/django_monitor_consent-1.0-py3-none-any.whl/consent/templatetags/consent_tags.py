from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag("consent/banner.html")
def consent_banner():
    return {"CONSENT_PARAGRAPHS": settings.CONSENT_TEXT.split("\n\n")}
