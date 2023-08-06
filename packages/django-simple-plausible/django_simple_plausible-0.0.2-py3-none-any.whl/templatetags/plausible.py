from django import template
from django.conf import settings
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag()
def plausible(site_domains=None, script_url=None):
    if site_domains is None:
        site_domains = getattr(settings, "PLAUSIBLE_SITES", "plausible.io")
    if script_url is None:
        script_url = getattr(settings, "PLAUSIBLE_SCRIPT_URL", "https://plausible.io/js/plausible.js")

    attrs = {
        "data-domain": site_domains,
        "src": script_url,
    }

    return mark_safe("<script defer{}></script>".format(flatatt(attrs)))
