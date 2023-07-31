from django import template
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

import json

from padanukkama.models import *

register = template.Library()


# ---------------------
# parse_editorjs
# ---------------------
@register.filter
def parse_editorjs(value):
    try:
        parsed_data = json.loads(value)
        text_list = []
        if "blocks" in parsed_data:
            for block in parsed_data["blocks"]:
                if "type" in block and block["type"] == "paragraph" and "data" in block and "text" in block["data"]:
                    text_list.append(block["data"]["text"])
        return text_list
    except (ValueError, KeyError):
        pass
    return []

# ---------------------
# nama_translation
# ---------------------
@register.inclusion_tag('padanukkama/templatetags/nama_translation.html')
def nama_translation(pada_id):
    pada = get_object_or_404(Pada, pk=pada_id)
    meaning = parse_editorjs(pada.sadda.description)

    sadda_type = pada.sadda.sadda_type
    # if sadda_type == 'Nama':
        

    return {
        'pada': pada,
        'meaning': meaning,
        'sadda_type': sadda_type
    }