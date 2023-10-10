import json

from django import template
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from padanukkama.models import *

from utils.pali_char import *

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
# get_at_index
# ---------------------

@register.filter
def get_at_index(list, index):
    return list[index]


# ---------------------
# get_from_dict
# ---------------------
@register.filter(name='get_from_dict')
def get_from_dict(value, arg):
    return value.get(arg, '')


# ---------------------
# get_from_array
# ---------------------
@register.filter(name='lookup')
def lookup(d, key):
    return d.get(key, '')

# ---------------------
# splits
# ---------------------
@register.filter
def split(value, arg):
    return value.split(arg)


# ---------------------
# pages_preview
# ---------------------
@register.inclusion_tag('padanukkama/templatetags/pages_preview.html', takes_context=True)
def pages_preview(context):
    return context


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


# ---------------------
# once
# ---------------------
@register.filter(name='once')
def once(value, arg):
    if not hasattr(once, "cache"):
        once.cache = {}
    
    if arg not in once.cache:
        once.cache[arg] = value
        return str(value) + ')'
    return ""


# ---------------------
# clear once
# ---------------------
@register.simple_tag(name='clear_once_cache')
def clear_once_cache():
    if hasattr(once, "cache"):
        del once.cache
    return ""



# ---------------------
# unique_parents
# ---------------------
@register.simple_tag
def initialize_parents_list():
    return set()

@register.simple_tag
def add_to_parents_list(parents_list, parent):
    parents_list.add(parent)
    return ""

@register.simple_tag
def check_in_parents_list(parents_list, parent):
    return parent in parents_list

@register.filter(name='has_pada')
def has_pada(value):
    return [item for item in value if item.pada]


@register.filter
def latex_escape(text):
    mapping = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        ',': r'\,',
        '*': r'\*',
        "'": r"\`",
        '"': r'\`',
        ':': r'\:',
    }
    return ''.join(mapping.get(c, c) for c in text)


@register.filter
def pali_char_convert(text):
    pintu ='\u0E3A'
    vowel = ['อ', 'อา','อิ','อี','อุ','อู','เอ','โอ','อํ']
    y = []
    for x in text:
        if x >= '0' and x <= '8':
            y.append(vowel[int(x)])
        else:
            y.append(x+pintu)
    return y


@register.filter
def sadda_type_display(sadda_object):
    display_value = sadda_object.get_sadda_type_display()
    thai_translation = {
        'Nāma': 'นาม',
        'Akhyāta': 'อาขฺยาต',
        'Byaya': 'พยฺย'
    }

    result = thai_translation.get(display_value, display_value)

    if sadda_object.sadda_type == 'Nama':
        linga = ", ".join(str(l) for l in Linga.objects.filter(id__in=sadda_object.namasaddamala.values_list('linga', flat=True)))
        result = result + ' ' + linga

    return result
