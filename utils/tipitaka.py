import traceback
from django.db import transaction

from mptt.utils import tree_item_iterator

from tipitaka.models import Edition, Page, Structure, TableOfContent, WordList, WordlistVersion

from .pali_char import *

# ----------------------------------------------------------------
# ค้นหาข้อความหรืออักษรจาก content ในตาราง Page
# ----------------------------------------------------------------
def find_text_in_tipitaka_page_content(text):
    all_p = Page.objects.all()
    found = 0
    for page in all_p:
        try:
            if text in page.content:
                found += 1
                print(found, page.edition, page.volume, page.page_number)
        except Exception as e:
            print("ERROR: Found error from find_text_in_tipitaka_page_content")
            print(f"Error message: {str(e)}")
            traceback.print_exc()

# ----------------------------------------------------------------
# ค้นหาและเปลี่ยนข้อความหรืออักษรจาก content ในตาราง Page
# ----------------------------------------------------------------
def find_and_replace_text_in_tipitaka_page_content(text, newtext):
    all_p = Page.objects.all()
    found = 0
    for page in all_p:
        try:
            if text in page.content:
                found += 1
                page.content = page.content.replace(text, newtext)
                page.save()
                print('#: ', found, 'e:', page.edition, 'v:', page.volume, 'p:', page.page_number)
        except Exception as e:
            print("ERROR: Found error from find_and_replace_text_in_tipitaka_page_content")
            print(f"Error message: {str(e)}")
            traceback.print_exc()

# ----------------------------------------------------------------
# ค้นหาคำจากข้อความ content ในตาราง Page เพื่อหาคำที่ลงท้ายด้วย พินทุ
# เนื่องจากศัพท์จะลงท้ายด้วยพินทุไม่ได้ ข้อมูลที่พบเหล่านี้อาจเป็นเพราะคำที่เว้นผิด
# ----------------------------------------------------------------
def pintu_found_at_last_char_of_word(edition_id):
    found = 0
    try:
        all_pages = Page.objects.filter(edition=edition_id).order_by("volume", "page_number")
        vol_no = 0
        for each_page in all_pages:
            if vol_no != each_page.volume.volume_number:
                vol_no = each_page.volume.volume_number
                print('========vol:', vol_no)
            position = 1
            line_number = 1
            if each_page.content:
                all_lines = each_page.content.replace("\r", "").split("\n")
                for each_line in all_lines:
                    all_words = each_line.split(" ")
                    for each_word in all_words:
                        try:
                            if each_word[-1] == "ฺ":
                                found += 1
                                print('#: ', found, 'vol:', vol_no, 'page:', each_page.page_number, 'line:', line_number, 'origin:', each_word,)
                                position += 1
                        except:
                            pass
                    line_number += 1
    except Exception as e:
        print("ERROR: Found error_found_atom pintu_i_of_wordn_last_char")
        print(f"Error message: {str(e)}")
        traceback.print_exc()

# ----------------------------------------------------------------
# ตรวจสอบ error ทั่วไปที่เกิดจากการปริวรรตอักษร เพื่อให้ทราบว่ามีการใช้อักษร
# ที่ไม่ใช้ตัวแทนเสียงในภาษาบาลี
# ----------------------------------------------------------------
def check_word_before_generation_wordlist(edition_id):
    found = 0
    try:
        all_pages = Page.objects.filter(edition=edition_id).order_by("volume", "page_number")
        vol_no = 0
        for each_page in all_pages:
            if vol_no != each_page.volume.volume_number:
                vol_no = each_page.volume.volume_number
                print('========vol:', vol_no)
            position = 1
            line_number = 1
            if each_page.content:               
                all_lines = each_page.content.replace("\r", "").split("\n")
                for each_line in all_lines:
                    all_words = each_line.split(" ")
                    for each_word in all_words:
                        cleaned_word = clean(each_word)
                        if len(cleaned_word.replace(" ", "")):
                            # print(vol_no, each_page.page_number, line_number, each_word, cleaned_word)
                            try:
                                # print(cv_pali_to_roman(extract(cleaned_word)))
                                cv_pali_to_roman(extract(cleaned_word))
                            except:
                                found += 1
                                print('#', found, 'page:', each_page.page_number, 'line:', line_number, 'origin:', each_word, 'clean:', cleaned_word)
                            position += 1
                    line_number += 1
    except Exception as e:
        print("ERROR: Found error from create_wordlist")
        print(f"Error message: {str(e)}")
        traceback.print_exc()


# ----------------------------------------------------------------
# ปรับปรุง Word_seq และ ปริวรรตอักษรโรมัน เมื่อพบ errors จะแสดงรายงาน
# ----------------------------------------------------------------
def Update_word_seq_in_WordList():
    words = WordList.objects.all()
    error_list = {}
    for each_word in words:
        try:
            each_word.word_seq = encode(extract(clean(each_word.word)))
            each_word.word_roman_script = cv_pali_to_roman(extract(clean(each_word.word)))
            each_word.save()
        except:
            error_list[each_word.id] = each_word.word
    print(error_list)

# ----------------------------------------------------------------
# สร้างฐานข้อมูล WordList โดยจะเก็บ Version เก่าไว้ และสร้าง Version ใหม่ขึ้น
# เป็นฟังก์ชั่นหลักในการประมวลผลสร้าง WordList
# ----------------------------------------------------------------
def create_wordlist(edition_id, created_by):
    try:
        # Step 1: Add WordlistVersion
        edition_instance = Edition.objects.get(pk=edition_id)
        new_version_number = int(edition_instance.version) + 1
        
        # WordlistVersion
        new_WordlistVersion_instance = WordlistVersion(
            version=new_version_number,
            edition=edition_instance,
            created_by=created_by
        )
        new_WordlistVersion_instance.save()  # Save the instance
        
        # Step 2: Create WordList and add to the database related to the latest version
        all_pages = Page.objects.filter(edition=edition_id).order_by("volume", "page_number")
        vol_no = 0
        for each_page in all_pages:
            if vol_no != each_page.volume.volume_number:
                vol_no = each_page.volume.volume_number
                print(vol_no)
            position = 1
            line_number = 1
            if each_page.content:
                all_lines = each_page.content.replace("\r", "").split("\n")
                for each_line in all_lines:
                    all_words = each_line.split(" ")
                    for each_word in all_words:
                        cleaned_word = clean(each_word)
                        if len(cleaned_word.replace(" ", "")):
                            new_wordlist_instance = WordList(
                                code="%s-%s-%s-%s" % (edition_instance.code,
                                                      str(each_page.volume.volume_number).zfill(3),
                                                      str(each_page.page_number).zfill(4),
                                                      str(position).zfill(3)),
                                word=cleaned_word,
                                # word_seq=encode(extract(cleaned_word)),
                                position=position,
                                line_number=line_number,
                                wordlist_version=new_WordlistVersion_instance,
                                edition=edition_instance,
                                volume=each_page.volume,
                                page=each_page,
                            )
                            new_wordlist_instance.save()
                            position += 1
                    line_number += 1
        
    except Exception as e:
        print("ERROR: Found error from create_wordlist")
        print(f"Error message: {str(e)}")
        traceback.print_exc()

# ----------------------------------------------------------------
# Table of contents
# สร้างรหัสย่อเพื่อใช้สำหรับอ้างอิง (TCR) จากโครงสร้าง สารบัญ
# ----------------------------------------------------------------
@transaction.atomic
def update_structure_code(node):
    def create_code(title):
        print(title)
        payangka = get_first_payangka_roman(cv_payangka(extract(clean(title))), 9)
        return payangka

    siblings = node.get_siblings(include_self=True)
    code_array = [n.code for n in siblings]

    payangka = create_code(node.title)
    got_new_code = False
    if len(payangka) > 1:
        for i in range(0, len(payangka)):
            try:
                new_code = payangka[0] + payangka[i + 1]
                if new_code not in code_array:
                    print('adding code>1', new_code)
                    node.code = new_code
                    got_new_code = True
                    break
            except:
                if not got_new_code:
                    for i in range(1, 50):
                        new_code = payangka[0] + payangka[1] + str(i)
                        if new_code not in code_array:
                            print('adding code>1s', new_code)
                            node.code = new_code
                            break
    else:
        print(payangka)
        new_code = payangka[0]
        if new_code not in code_array:
            for i in range(1, 50):
                new_code = payangka[0] + str(i)
                if new_code not in code_array:
                    print('adding code=1', new_code)
                    node.code = new_code
                    break
    
    node.save()
    print(code_array)

    for child in node.get_children():
        update_structure_code(child)

# ----------------------------------------------------------------
# นำเข้าข้อมูลสารบัญที่เตรียมใน Sheet
# ----------------------------------------------------------------

def import_structure(structure_datas):
    # Create a dictionary to map parent IDs to Sturcture instances
    parents = {}
    toc = TableOfContent.objects.get(pk=1)

    # Iterate over the structure data and create Sturcture instances
    for structure_data in structure_datas:
        structure = Structure(
            code=structure_data['code'],
            title=structure_data['title'],
            ro=structure_data['ro'],
            si=structure_data['si'],
            hi=structure_data['hi'],
            lo=structure_data['lo'],
            my=structure_data['my'],
            km=structure_data['km'],
            table_of_content=toc)
        structure.parent = parents.get(structure_datas['parent_id'])
        structure.save()

        # Add the new structure instance to the parent dictionary
        parents[structure_data['id']] = structure

    # Rebuild the tree structure
    tree_items = list(tree_item_iterator(Structure.objects.all()))
    Structure.objects.partial_rebuild(tree_items)

    return True