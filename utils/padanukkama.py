from django.db.models import Q
from django.db import transaction

from tipitaka.models import CommonReference, WordList
from padanukkama.models import Padanukkama, Pada, NamaSaddamala, Sadda, AkhyataSaddamala, LiteralTranslation, TranslatedWord
from .pali_char import *

from padanukkama.workflows import SaddaTranslationWorkflow

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
        conditions |= Q(code__range=(from_position, to_position))

    # Filter the WordList objects based on the conditions and wordlist_version
    wordlists = WordList.objects.filter(wordlist_version__in=wordlist_versions).filter(conditions).distinct('word')
    print(wordlists.count(), 'records')

    # Create Pada objects in bulk to minimize database queries
    pada_objects_to_create = []
    for wordlist in wordlists:
        is_pada_exists = Pada.objects.filter(padanukkama=padanukkama, pada=wordlist.word).exists()

        if not is_pada_exists:
            pada_objects_to_create.append(
                Pada(
                    padanukkama=padanukkama,
                    pada=wordlist.word,
                    pada_seq=wordlist.word_seq,
                    pada_roman_script=wordlist.word_roman_script,
                    lft=0,
                    rght=0,
                    tree_id=0,
                    level=0,
                )
            )

    # Bulk create the Pada objects
    Pada.objects.bulk_create(pada_objects_to_create)
    print('rebuilding...')
    Pada.objects.rebuild()



def mix_namavipatties(sadda, template_id):
    if not is_validate_pali(sadda):
        return {'error':True}

    pada = NamaSaddamala.objects.get(pk=template_id)
    result = {'error':False}
    sadda_expand = extract(sadda)
    
    vipatti_fields = [
        'nom_sg', 'nom_pl','voc_sg','voc_pl','acc_sg','acc_pl',
        'instr_sg','instr_pl','dat_sg','dat_pl','abl_sg','abl_pl',
        'gen_sg','gen_pl','loc_sg','loc_pl',
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



def mix_akhyatavipatties(akhyata, template_id):
    if not is_validate_pali(akhyata):
        return {'error':True}

    pada = AkhyataSaddamala.objects.get(pk=template_id)    
    result = {'error':False}
    sadda_expand = extract(akhyata)

    vipatti_fields = ['vat_pu3_para_sg','vat_pu3_para_pl','vat_pu3_atta_sg','vat_pu3_atta_pl',
                      'vat_pu2_para_sg','vat_pu2_para_pl','vat_pu2_atta_sg','vat_pu2_atta_pl',
                      'vat_pu1_para_sg','vat_pu1_para_pl','vat_pu1_atta_sg','vat_pu1_atta_pl',
                      'pan_pu3_para_sg','pan_pu3_para_pl','pan_pu3_atta_sg','pan_pu3_atta_pl',
                      'pan_pu2_para_sg','pan_pu2_para_pl','pan_pu2_atta_sg','pan_pu2_atta_pl',
                      'pan_pu1_para_sg','pan_pu1_para_pl','pan_pu1_atta_sg','pan_pu1_atta_pl',
                      'sat_pu3_para_sg','sat_pu3_para_pl','sat_pu3_atta_sg','sat_pu3_atta_pl',
                      'sat_pu2_para_sg','sat_pu2_para_pl','sat_pu2_atta_sg','sat_pu2_atta_pl',
                      'sat_pu1_para_sg','sat_pu1_para_pl','sat_pu1_atta_sg','sat_pu1_atta_pl',
                      'par_pu3_para_sg','par_pu3_para_pl','par_pu3_atta_sg','par_pu3_atta_pl',
                      'par_pu2_para_sg','par_pu2_para_pl','par_pu2_atta_sg','par_pu2_atta_pl',
                      'par_pu1_para_sg','par_pu1_para_pl','par_pu1_atta_sg','par_pu1_atta_pl',
                      'hit_pu3_para_sg','hit_pu3_para_pl','hit_pu3_atta_sg','hit_pu3_atta_pl',
                      'hit_pu2_para_sg','hit_pu2_para_pl','hit_pu2_atta_sg','hit_pu2_atta_pl',
                      'hit_pu1_para_sg','hit_pu1_para_pl','hit_pu1_atta_sg','hit_pu1_atta_pl',
                      'ajj_pu3_para_sg','ajj_pu3_para_pl','ajj_pu3_atta_sg','ajj_pu3_atta_pl',
                      'ajj_pu2_para_sg','ajj_pu2_para_pl','ajj_pu2_atta_sg','ajj_pu2_atta_pl',
                      'ajj_pu1_para_sg','ajj_pu1_para_pl','ajj_pu1_atta_sg','ajj_pu1_atta_pl',
                      'bha_pu3_para_sg','bha_pu3_para_pl','bha_pu3_atta_sg','bha_pu3_atta_pl',
                      'bha_pu2_para_sg','bha_pu2_para_pl','bha_pu2_atta_sg','bha_pu2_atta_pl',
                      'bha_pu1_para_sg','bha_pu1_para_pl','bha_pu1_atta_sg','bha_pu1_atta_pl',
                      'kal_pu3_para_sg','kal_pu3_para_pl','kal_pu3_atta_sg','kal_pu3_atta_pl',
                      'kal_pu2_para_sg','kal_pu2_para_pl','kal_pu2_atta_sg','kal_pu2_atta_pl',
                      'kal_pu1_para_sg','kal_pu1_para_pl','kal_pu1_atta_sg','kal_pu1_atta_pl',
    ]


    for vipatti_key in vipatti_fields:
        vipatti_keys = getattr(pada, vipatti_key)
        if akhyata == pada.title_code:
            result[vipatti_key] = vipatti_keys or ''
        else:
            template_expand = extract(pada.title_code)
            vipatti_key_weared = wear_namavipatti(sadda_expand, template_expand, vipatti_keys)
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




def copy_child_padas(from_padanukkama_id, to_padanukkama_id):
    first_padanukkama = Padanukkama.objects.get(pk=from_padanukkama_id)
    second_padanukkama = Padanukkama.objects.get(pk=to_padanukkama_id)
    
    # สร้าง dictionary ที่มี key เป็น pada และ value เป็น list ของ children
    first_pada_children_map = {pada.pada: list(pada.get_children()) for pada in first_padanukkama.pada.all() if pada.get_children().exists()}
    
    for second_pada in second_padanukkama.pada.all():
        # หา children ที่ตรงกันจาก first_pada_children_map
        matching_children = first_pada_children_map.get(second_pada.pada)
        if matching_children:
            # print('found match and has children', second_pada.pada)
            for child_of_1st_pada in matching_children:
                # ตรวจสอบว่า child pada นี้มีอยู่แล้วหรือไม่
                existing_pada = Pada.objects.filter(
                    padanukkama=second_padanukkama,
                    pada=child_of_1st_pada.pada,
                    parent=second_pada,
                ).first()

                if not existing_pada:
                    created = Pada.objects.create(
                        padanukkama=second_padanukkama,
                        pada=child_of_1st_pada.pada,
                        pada_seq=encode(extract(clean(child_of_1st_pada.pada))),
                        parent=second_pada,
                    )
                    print(f'Created new child pada: {created.pada}')




def copy_sadda(from_padanukkama_id, to_padanukkama_id):
    first_padanukkama = Padanukkama.objects.get(pk=from_padanukkama_id)
    second_padanukkama = Padanukkama.objects.get(pk=to_padanukkama_id)

    # สร้าง dictionary ที่มี key เป็น pada และ value เป็น sadda
    first_pada_sadda_map = {pada.pada: pada.sadda for pada in first_padanukkama.pada.all() if pada.has_sadda()}

    for second_pada in second_padanukkama.pada.all():
        # หา sadda ที่ตรงกันจาก first_pada_sadda_map
        matching_sadda = first_pada_sadda_map.get(second_pada.pada)
        if matching_sadda:
            existing_sadda = Sadda.objects.filter(padanukkama=second_padanukkama, sadda=matching_sadda.sadda).first()
            if existing_sadda:
                sadda = existing_sadda
            else:
                # สร้างข้อมูล sadda สำหรับ pada รายการที่สองโดยคัดลอกจาก pada รายการแรก
                sadda = Sadda.objects.create(
                    padanukkama=second_padanukkama,
                    sadda=matching_sadda.sadda,
                    sadda_seq=matching_sadda.sadda_seq,
                    sadda_type=matching_sadda.sadda_type,
                    construction=matching_sadda.construction,
                    meaning=matching_sadda.meaning,
                    description=matching_sadda.description,
                    state=SaddaTranslationWorkflow.initial_state
                )
                print(sadda.sadda)
                # คัดลอกข้อมูล namasaddamala และ verb_conjugation
                sadda.namasaddamala.set(matching_sadda.namasaddamala.all())
                sadda.verb_conjugation.set(matching_sadda.verb_conjugation.all())

            # ให้ pada รายการที่สองเชื่อมโยงกับ sadda
            second_pada.sadda = sadda
            second_pada.save()



def delete_recently_created_sadda(to_padanukkama_id):
    # รับ padanukkama รายการที่สอง
    second_padanukkama = Padanukkama.objects.get(pk=to_padanukkama_id)
    
    # ลบข้อมูล Sadda ที่เชื่อมโยงกับ padanukkama รายการที่สอง
    second_padanukkama.saddas.all().delete()



# ดำเนินการแก้ไข
def fix_pada_in_translation(literal_translation_id):
    all_words = TranslatedWord.objects.filter(
        Q(literal_translation=literal_translation_id) & 
        Q(pada__isnull=False) &
        Q(structure_id=6889) &
        Q(pada__parent__isnull=False)
    )
    


