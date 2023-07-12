from padanukkama.models import *
from tipitaka.models import *

from aksharamukha import transliterate

def remove_ending_vowels(word):
    ending_vowels = ['a','ā','i','ī','u','ū','e','o','ṃ']
    removed_chars = ''
    
    while word and word[-1] in ending_vowels:
        removed_chars = word[-1] + removed_chars
        word = word[:-1]
    
    return word, removed_chars


def get_differing_characters(word1, word2):
    differing_chars = []
    start_index = 0
    
    for part in word1.split(word2):
        differing_chars.append(word1[start_index:start_index+len(part)])
        start_index += len(part) + len(word2)
    
    return ''.join(differing_chars)


def noun_declension(str, namasaddamala_id):
    # variables
    vipatti_fields = [
        'nom_sg', 'nom_pl','voc_sg','voc_pl','acc_sg','acc_pl',
        'instr_sg','instr_pl','dat_sg','dat_pl','abl_sg','abl_pl',
        'gen_sg','gen_pl','loc_sg','loc_pl',
    ]
    result = {'error':False}

    try:
        # convert to Roman
        str_roman = transliterate.process('Thai', 'IASTPali', str)
        # remove endding vowels
        sadda_roman_without_karanta, removed_chars_roman = remove_ending_vowels(str_roman)
        # convert remove endding vowels to Thai
        sadda_thai_without_karanta = transliterate.process('IASTPali', 'Thai', sadda_roman_without_karanta)
        # get namasaddamala
        pada = NamaSaddamala.objects.get(pk=namasaddamala_id)

        # get title code (base sadda) and cnvert to Roman
        code_roman = transliterate.process('Thai', 'IASTPali', pada.title_code)
        # remove endding vowels of code title
        code_roman_without_karanta, code_roman_karanta = remove_ending_vowels(code_roman)
        
        for vipatti_field in vipatti_fields:
            vipatti_str_thai = getattr(pada, vipatti_field)
            vipatti_str_roman = transliterate.process('Thai', 'IASTPali', vipatti_str_thai or '')
            
            if sadda_roman_without_karanta == code_roman_without_karanta:
                result[vipatti_field] = vipatti_str_thai or ''
            else:
                result[vipatti_field] = []
                for v in vipatti_str_roman.split(' '):
                    endding_chars = get_differing_characters(v, code_roman_without_karanta)
                    str_roman_with_declension = sadda_roman_without_karanta + endding_chars
                    str_thai_with_declension = transliterate.process('IASTPali', 'Thai', str_roman_with_declension)
                    result[vipatti_field].append(str_thai_with_declension)
                result[vipatti_field] = " ".join(result[vipatti_field])
    except:
        result = {'error':True}
        
    return result

