from django.db.models import Q

from tipitaka.models import CommonReference, WordList
from padanukkama.models import Padanukkama, Pada, NamaSaddamala, AkhyataSaddamala
from .pali_char import extract, compress, is_validate_pali

def create_pada(padanukkama_id):
    padanukkama = Padanukkama.objects.get(pk=padanukkama_id)
    # Retrieve the structures related to the padanukkama
    structures = padanukkama.structure.all()
    # Retrieve all the related CommonReference instances for the structures
    common_references = CommonReference.objects.filter(structure__in=structures)
    # Collect the from_position, to_position, and wordlist_version values from the common_references
    positions = common_references.values_list('from_position', 'to_position')
    wordlist_versions = common_references.values_list('wordlist_version', flat=True)
    # Combine the conditions using OR (Q objects) for each common reference
    conditions = Q()
    for from_position, to_position in positions:
        conditions |= Q(code__gte=from_position, code__lte=to_position)

    # Filter the WordList objects based on the conditions and wordlist_version
    wordlists = WordList.objects.filter(wordlist_version__in=wordlist_versions).filter(conditions).distinct('word')
    for wordlist in wordlists:
        # Pada.objects.create(
        #     padanukkama=padanukkama,
        #     pada=wordlist.word,
        #     pada_seq=wordlist.word_seq,
        #     pada_roman_script=wordlist.word_roman_script,
        # )
        is_pada_exists = Pada.objects.filter(
            padanukkama=padanukkama,
            pada=wordlist.word
        ).exists()

        if not is_pada_exists:
            Pada.objects.create(
                padanukkama=padanukkama,
                pada=wordlist.word,
                pada_seq=wordlist.word_seq,
                pada_roman_script=wordlist.word_roman_script,
            )


def mix_namavipatties(sadda, template_id):
    if not is_validate_pali(sadda):
        return {'error':True}

    pada = NamaSaddamala.objects.get(pk=template_id)
    result = {'error':False}
    sadda_expand = extract(sadda)
    
    vipatti_fields = [
        'nom_sg', 'nom_pl','voc_sg','voc_pl','acc_sg','acc_pl','instr_sg','instr_pl','dat_sg','dat_pl','abl_sg','abl_pl','gen_sg','gen_pl','loc_sg','loc_pl',
    ]
    for vipatti_key in vipatti_fields:
        vipatti_keys = getattr(pada, vipatti_key)
        if sadda == pada.title_code:
            result[vipatti_key] = vipatti_keys or ''
        else:
            template_expand = extract(pada.title_code)
            vipatti_key_weared = wear_namavipatti(sadda_expand, template_expand, vipatti_keys)
            result[vipatti_key]=vipatti_key_weared
        
    return result

def mix_akhyatavipatties(arkayata, template_id):
    if not is_validate_pali(arkayata):
        return {'error':True}

    pada = AkhyataSaddamala.objects.get(pk=template_id)

    if len(arkayata) <= 2:
        return {'error':True}
    else:
        arkayata = arkayata[:-2]
        pada.title = pada.title[:-2]
        print( arkayata,' => ',pada)

    fields = pada._meta.get_fields()
    start = 5  # start = 5 
    stop = len(pada._meta.fields) # stop = 101

    result = {'error':False}
    
    sadda_expand = extract(arkayata)
    template_expand = extract(pada.title)

    for num in range(start, stop):
        vipatti_key = fields[num].name
        vipatti_keys = getattr(pada, vipatti_key)
        try:
            vipatti_key_weared = wear_namavipatti(sadda_expand, template_expand, vipatti_keys)
        except:
            return {'error':True}
        result[vipatti_key]=vipatti_key_weared
        
    return result

def  wear_namavipatti(sadda_expand, template_expand, vipatti_keys):
    if not vipatti_keys:
        return ''
    result = []
    vipatti_keys = vipatti_keys.split()


    for i in range(len(vipatti_keys)):
        result.append(cv_to_pattern(sadda_expand, template_expand, extract(vipatti_keys[i])))
 
    return " ".join(result)


def cv_to_pattern(sadda_expand, template_expand, vipatti_key_expand):
    pattern = get_pattern(template_expand, vipatti_key_expand)
    #  ได้ pattern มาแล้ว แต่เวลาเปรียบเทียบต้องจากหลังไปหน้า
    first_time = True
    y = []
    for i in range(len(pattern)):
        if isinstance(pattern[i], int):
            # ถ้าเป็นตัวเลขต้องเอาจากต้นทาง satta
            if first_time:
                last_id = pattern[i] + 1
                if last_id != 0:
                    y +=  sadda_expand[:last_id]
                else:
                    y +=  sadda_expand[:]
                first_time = False
            else:
                idn = pattern[i]
                y.append(sadda_expand[idn])
        else:
            y.append(pattern[i])
    
    return compress(y)
    


def get_pattern(template_expand, vipatti_key_expand):
    
    pattern = list(vipatti_key_expand)
    origin = list(template_expand)
    
    l_ori = len(origin)
    for i in range(len(pattern)):
        x = pattern[i]
        try:
            idn = origin.index(x)
            pattern[i] = idn-l_ori
            origin[idn]='-'
        except:
            pass

    l = len(pattern)
    if isinstance(pattern[0], int):
        max = pattern[0] - 1 # ตั้งค่าเพื่อเปรียบเทียบการลดลงทีละ 1 index
        for i in range(l):
            if isinstance(pattern[i], int):
                max += 1  # ลดทีละ 1
                if max < pattern[i]: # ลดมากกว่า 1
                    pattern = pattern[i-1:] # เอาแค่ก่อนหน้า
                    break
                elif i+1 == l: # แสดงว่าเท่ากันจนถึงตัวสุดท้าย
                    pattern = [pattern[i]]
            else: # เป็้น string
                pattern = pattern[i-1:]
                break
    return pattern
