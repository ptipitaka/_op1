import os
import subprocess
import pytz
import glob
import boto3
from botocore.exceptions import NoCredentialsError
from datetime import datetime

from django.db.models import Q
from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from .models import Sadda, Linga, Pada

from aksharamukha import transliterate
from braces.views import SuperuserRequiredMixin
from collections import OrderedDict

pdf_folder_path = os.path.join(settings.BASE_DIR, 'padanukkama', 'static', 'pdf')


# --------------------------
# delete_all_files_in_folder
# --------------------------
def delete_all_files_in_folder(folder_path):
    files = glob.glob(os.path.join(folder_path, '*'))
    for f in files:
        os.remove(f)


# ------------
# latex_escape
# ------------
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


# ------------------
# pali_char_convert
# ------------------
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


# ------------------
# sadda_type_display
# ------------------
def sadda_type_display(sadda_object):
    # ดึงข้อมูลทั้งหมดจากฐานข้อมูลและเรียงตาม 'sequence'
    linga_objects = Linga.objects.all().order_by('sequence')

    # สร้าง dictionary จาก QuerySet
    order_dict = {obj.code: obj.sequence for obj in linga_objects}

    display_value = sadda_object.sadda_type
    thai_translation = {
        'Nama': '',
        'Akhyata': 'ขยฺา',
        'Byaya': 'พฺยย'
    }

    result = thai_translation.get(display_value, display_value)

    if sadda_object.sadda_type == 'Nama':
        linga_list = list(Linga.objects.filter(id__in=sadda_object.namasaddamala.values_list('linga', flat=True)))
        unique_linga = set(str(l) for l in linga_list)  # ใช้ set ในการหาค่าที่ไม่ซ้ำกัน
        # แปลงเป็น list และเรียงลำดับตามที่ระบุใน order_dict
        sorted_linga = sorted(unique_linga, key=lambda x: order_dict.get(x, 9999))

        if len(sorted_linga) >= 3:
            return 'วาจฺ'

        result = ", ".join(sorted_linga)

    return result


# -------------
# upload_to_aws
# -------------
def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                      endpoint_url=settings.AWS_S3_ENDPOINT_URL)

    try:
        s3.upload_file(local_file, bucket, s3_file, ExtraArgs={'ACL': 'public-read', 'CacheControl': 'max-age=86400'})
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


# ---------------------
# padanukkama_titlepage
# ---------------------
def padanukkama_titlepage():
    latex_frontmatter = r"""
    \frontmatter
    \pagestyle{empty}

    % Title page
    \begin{titlepage}
        \centering
        
        ~
        
        \vspace{24pt}
        {\scshape\Huge \booktitle\par}
        \vspace{6pt}
        {\scshape\large \subtitle\par}
        \vspace{\stretch{1.25}}
    \end{titlepage}
    \cleardoublepage
    """
    return latex_frontmatter


# ---------------------
# GenerateBook 2 Column
# ---------------------
def GenerateBook(request, padanukkama_id):
    # ลบไฟล์ทั้งหมดใน folder
    delete_all_files_in_folder(pdf_folder_path)

    # สร้าง LaTeX ไฟล์จาก template
    saddas = Sadda.objects.filter(padanukkama = padanukkama_id).order_by('sadda_seq')

    # สร้าง LaTeX content
    mainmatter_list = []
    previous_first_char = None

    for sadda in saddas:
        first_char = sadda.sadda_seq[0]

        if first_char != previous_first_char:
            if previous_first_char is not None:
                mainmatter_list.append(r"\end{multicols}")

            # แปลงตัวอักษรใน Pali และ escape สำหรับ LaTeX ที่นี่
            section_title = pali_char_convert(first_char)
            section_title = latex_escape(section_title)

            mainmatter_list.append(r"\needspace{5cm} \section*{%s}" % section_title)
            mainmatter_list.append(r"\begin{multicols}{2}")

        construction = sadda.construction if sadda.construction else "ไม่มีการประกอบคำ"
        sadda_type = sadda_type_display(sadda)
        padas = ''
        if sadda.sadda_type == 'Nama':
            related_padas = Pada.objects.filter(sadda=sadda).order_by('pada_seq')
            unique_padas = list(OrderedDict.fromkeys([p.pada for p in related_padas]))
            padas = ', '.join([latex_escape(p) for p in unique_padas])
        meaning = sadda.meaning if sadda.meaning else "ไม่มีคำแปล"

        entry_line = r"\entry{%s} {%s} {%s} {%s} {%s}" % (
            latex_escape(sadda.sadda),
            latex_escape(sadda_type),
            latex_escape(construction),
            latex_escape(meaning),
            padas,
        )
        mainmatter_list.append(entry_line)


        previous_first_char = first_char

    mainmatter_list.append(r"\end{multicols}")
    mainmatter = "\n".join(mainmatter_list)

    context = {
        "frontmatter": padanukkama_titlepage(),
        "mainmatter": mainmatter,
    }
    latex_main_content = render(request, 'padanukkama/latex/padanukkama/padanukkama.tex', context).content.decode('utf-8')

    # สร้างชื่อไฟล์ที่ไม่ซ้ำกัน
    unique_filename = get_random_string(5)
    tex_file_path = os.path.join(pdf_folder_path, f"{unique_filename}.tex")
    pdf_file_path = os.path.join(pdf_folder_path, f"{unique_filename}.pdf")
    err_file_path = os.path.join(pdf_folder_path, f"{unique_filename}.err")

    # บันทึก LaTeX ไฟล์ลงใน disk
    with open(tex_file_path, 'w', encoding='utf-8') as f:
        f.write(latex_main_content)

    # คอมไพล์ LaTeX ไฟล์เป็น PDF
    try:
        result = subprocess.run(
            ['xelatex', '-output-directory=' + pdf_folder_path, tex_file_path])
        if result.returncode == 0:
            uploaded_pdf = upload_to_aws(pdf_file_path, settings.AWS_STORAGE_BUCKET_NAME, 'pdf/' + os.path.basename(pdf_file_path))
            uploaded_tex = upload_to_aws(tex_file_path, settings.AWS_STORAGE_BUCKET_NAME, 'pdf/' + os.path.basename(tex_file_path))

            if uploaded_pdf and uploaded_tex:
                print("Both files uploaded successfully")
            else:
                print("File upload failed")
                with open(err_file_path, 'a', encoding='utf-8') as f:
                    f.write("File upload failed")
                
        elif result.returncode != 0:
            # print("xelatex failed with return code", result.returncode)
            with open(err_file_path, 'a', encoding='utf-8') as f:
                f.write("xelatex failed with return code" + str(result.returncode))
    except BrokenPipeError as e:
        with open(err_file_path, 'a', encoding='utf-8') as f:
            f.write("BrokenPipeError" + {e})

    # อ่าน PDF ไฟล์ลงใน memory
    with open(pdf_file_path, 'rb') as f:
        pdf_data = f.read()

    # ส่ง PDF ไฟล์กลับเป็น response โดยสร้างชื่อไฟล์จากวันที่และเวลาปัจจุบัน
    # กำหนด Timezone ของกรุงเทพฯ
    bangkok_tz = pytz.timezone('Asia/Bangkok')
    local_time = datetime.now(bangkok_tz)
    # สร้างชื่อไฟล์จากวันที่และเวลาท้องถิ่น
    formatted_time = local_time.strftime("%Y%m%d-BKK-%H%M")
    # ส่ง PDF ไฟล์กลับเป็น response
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="padanukkama-{unique_filename}-{formatted_time}.pdf"'
    return response



# -------------------------
# GenerateBook1Col 1 Column
# -------------------------
def GenerateBook1Col(request, padanukkama_id):
    # ลบไฟล์ทั้งหมดใน folder
    delete_all_files_in_folder(pdf_folder_path)

    # สร้าง LaTeX ไฟล์จาก template
    saddas = Sadda.objects.filter(padanukkama = padanukkama_id).order_by('sadda_seq')

    # สร้าง LaTeX content
    mainmatter_list = []
    previous_first_char = None

    for sadda in saddas:
        first_char = sadda.sadda_seq[0]

        if first_char != previous_first_char:
            # แปลงตัวอักษรใน Pali และ escape สำหรับ LaTeX ที่นี่
            section_title = pali_char_convert(first_char)
            section_title = latex_escape(section_title)

            mainmatter_list.append(r"\needspace{5cm} \section*{%s}" % section_title)

        construction = sadda.construction if sadda.construction else "ไม่มีการประกอบคำ"
        sadda_type = sadda_type_display(sadda)
        meaning = sadda.meaning if sadda.meaning else "ไม่มีคำแปล"

        entry_line = r"\entry{%s} {%s} {%s} {%s}" % (
            latex_escape(sadda.sadda), latex_escape(construction), latex_escape(sadda_type), latex_escape(meaning))
        mainmatter_list.append(entry_line)

        previous_first_char = first_char

    mainmatter = "\n".join(mainmatter_list)

    context = {
        "frontmatter": padanukkama_titlepage(),
        "mainmatter": mainmatter,
    }
    latex_main_content = render(request, 'padanukkama/latex/padanukkama/padanukkama.tex', context).content.decode('utf-8')

    # สร้างชื่อไฟล์ที่ไม่ซ้ำกัน
    unique_filename = get_random_string(5)
    tex_file_path = os.path.join(pdf_folder_path, f"{unique_filename}.tex")
    pdf_file_path = os.path.join(pdf_folder_path, f"{unique_filename}.pdf")
    err_file_path = os.path.join(pdf_folder_path, f"{unique_filename}.err")

    # บันทึก LaTeX ไฟล์ลงใน disk
    with open(tex_file_path, 'w', encoding='utf-8') as f:
        f.write(latex_main_content)

    # คอมไพล์ LaTeX ไฟล์เป็น PDF
    try:
        result = subprocess.run(
            ['xelatex', '-output-directory=' + pdf_folder_path, tex_file_path])
        if result.returncode == 0:
            uploaded_pdf = upload_to_aws(pdf_file_path, settings.AWS_STORAGE_BUCKET_NAME, 'pdf/' + os.path.basename(pdf_file_path))
            uploaded_tex = upload_to_aws(tex_file_path, settings.AWS_STORAGE_BUCKET_NAME, 'pdf/' + os.path.basename(tex_file_path))

            if uploaded_pdf and uploaded_tex:
                print("Both files uploaded successfully")
            else:
                print("File upload failed")
                with open(err_file_path, 'a', encoding='utf-8') as f:
                    f.write("File upload failed")
                
        elif result.returncode != 0:
            # print("xelatex failed with return code", result.returncode)
            with open(err_file_path, 'a', encoding='utf-8') as f:
                f.write("xelatex failed with return code" + str(result.returncode))
    except BrokenPipeError as e:
        with open(err_file_path, 'a', encoding='utf-8') as f:
            f.write("BrokenPipeError" + {e})

    # อ่าน PDF ไฟล์ลงใน memory
    with open(pdf_file_path, 'rb') as f:
        pdf_data = f.read()

    # ส่ง PDF ไฟล์กลับเป็น response โดยสร้างชื่อไฟล์จากวันที่และเวลาปัจจุบัน
    # กำหนด Timezone ของกรุงเทพฯ
    bangkok_tz = pytz.timezone('Asia/Bangkok')
    local_time = datetime.now(bangkok_tz)
    # สร้างชื่อไฟล์จากวันที่และเวลาท้องถิ่น
    formatted_time = local_time.strftime("%Y%m%d-BKK-%H%M")
    # ส่ง PDF ไฟล์กลับเป็น response
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="padanukkama-{unique_filename}-{formatted_time}.pdf"'
    return response


# -------------------------
# GenerateBookPada 2 Column 
# -------------------------
def GeneratePadaBook2Column(request, padanukkama_id):
    # ลบไฟล์ทั้งหมดใน folder
    delete_all_files_in_folder(pdf_folder_path)

    # ดึงข้อมูลทั้งหมดที่ตรงกับเงื่อนไข
    all_padas = Pada.objects.filter(
        Q(padanukkama=padanukkama_id) & Q(parent=None)
    ).order_by('pada_seq')

    # กรองเฉพาะที่มี descendants
    padas_with_descendants = [pada for pada in all_padas if pada.has_descendants()]

    # ดึงข้อมูลจาก database อีกครั้ง ถ้าจำเป็น
    padas = Pada.objects.filter(
        id__in=[pada.id for pada in padas_with_descendants]
    ).order_by('pada_seq')


    # สร้าง LaTeX content
    mainmatter_list = []
    previous_first_char = None

    for each_pada in padas:
        # กระบวนการสร้าง section ตามอักษรแรกของคำ
        first_char = each_pada.pada_seq[0]

        if first_char != previous_first_char:
            if previous_first_char is not None:
                mainmatter_list.append(r"\end{multicols}")

            # แปลงตัวอักษรใน Pali และ escape สำหรับ LaTeX ที่นี่
            section_title = pali_char_convert(first_char)
            section_title = latex_escape(section_title)

            mainmatter_list.append(r"\needspace{5cm} \section*{%s}" % section_title)
            mainmatter_list.append(r"\begin{multicols}{2}")

        # ตัวแปรที่ 1 บท
        _1 = each_pada.pada
        # ตรวจสอบว่าเป็นสนธิศัพท์หรือไม่
        if each_pada.has_descendants():
            # ตัวแปรที่ 2 สทธิ
            _2 = r"(%s)" %(each_pada.get_sandhi())

            _3_list = []
            for each_sondhi in each_pada.get_only_descendants().order_by('pk'):
                if each_sondhi.has_sadda():
                    sadda = each_sondhi.sadda
                    sadda_type = sadda_type_display(sadda)
                    construction = sadda.construction if sadda.construction else "ไม่พบข้อมูล"
                    meaning = sadda.meaning if sadda.meaning else "ไม่พบข้อมูล"
                    _3_list.append(r"\textbf{%s} \hfill {\small\textit{%s}} \par{\small\textsc{%s}} {%s}" %(
                        sadda.sadda,
                        latex_escape(sadda_type),
                        latex_escape(construction),
                        latex_escape(meaning)
                    ))
                else:
                    _3_list.append(r"ไม่พบข้อมูล")
            _3_list_latex = [r"\par " + item for item in _3_list]
            # ตัวแปรที่ 3 รายละเอียด
            _3 = r"".join(_3_list_latex)
        # ไม่มีสนธิ แต่ แปลศัพท์ไว้
        elif each_pada.has_sadda():
            sadda = each_pada.sadda
            sadda_type = sadda_type_display(sadda)
            construction = sadda.construction if sadda.construction else "ไม่พบข้อมูล"
            meaning = sadda.meaning if sadda.meaning else "ไม่พบข้อมูล"
            # ตัวแปรที่ 2 ศัพท์
            _2 = r"(%s)" %(sadda.sadda)
            # ตัวแปรที่ 3 รายละเอียด
            _3 = r"\textit{%s} %s $\bullet$\ %s" %(
                latex_escape(sadda_type),
                latex_escape(construction),
                latex_escape(meaning)
            )
        # ยังไม่ได้แปลศัพท์
        else:
            # ตัวแปรที่ 2 ศัพท์
            _2 = "ไม่พบข้อมูล"
            # ตัวแปรที่ 3 รายละเอียด
            _3 = "ไม่พบข้อมูล"

        entry_line = r"\entry{%s} {%s} {%s}" %(
            latex_escape(_1),
            latex_escape(_2),
            _3
        )
        mainmatter_list.append(entry_line)

        # เก็บค่าอักษรแรก
        previous_first_char = first_char

    mainmatter_list.append(r"\end{multicols}")
    mainmatter = "\n".join(mainmatter_list)

    context = {
        "frontmatter": padanukkama_titlepage(),
        "mainmatter": mainmatter,
    }
    latex_main_content = render(request,
        'padanukkama/latex/padanukkama/padanukkama_by_pada.tex',
        context).content.decode('utf-8')

    # สร้างชื่อไฟล์ที่ไม่ซ้ำกัน
    unique_filename = get_random_string(5)
    tex_file_path = os.path.join(pdf_folder_path, f"{unique_filename}.tex")
    pdf_file_path = os.path.join(pdf_folder_path, f"{unique_filename}.pdf")
    err_file_path = os.path.join(pdf_folder_path, f"{unique_filename}.err")

    # บันทึก LaTeX ไฟล์ลงใน disk
    with open(tex_file_path, 'w', encoding='utf-8') as f:
        f.write(latex_main_content)

    # คอมไพล์ LaTeX ไฟล์เป็น PDF
    try:
        result = subprocess.run(
            ['xelatex', '-output-directory=' + pdf_folder_path, tex_file_path])
        if result.returncode == 0:
            uploaded_pdf = upload_to_aws(pdf_file_path, settings.AWS_STORAGE_BUCKET_NAME, 'pdf/' + os.path.basename(pdf_file_path))
            uploaded_tex = upload_to_aws(tex_file_path, settings.AWS_STORAGE_BUCKET_NAME, 'pdf/' + os.path.basename(tex_file_path))

            if uploaded_pdf and uploaded_tex:
                print("Both files uploaded successfully")
            else:
                print("File upload failed")
                with open(err_file_path, 'a', encoding='utf-8') as f:
                    f.write("File upload failed")
                
        elif result.returncode != 0:
            # print("xelatex failed with return code", result.returncode)
            with open(err_file_path, 'a', encoding='utf-8') as f:
                f.write("xelatex failed with return code" + str(result.returncode))
    except BrokenPipeError as e:
        with open(err_file_path, 'a', encoding='utf-8') as f:
            f.write("BrokenPipeError" + {e})

    # อ่าน PDF ไฟล์ลงใน memory
    with open(pdf_file_path, 'rb') as f:
        pdf_data = f.read()

    # ส่ง PDF ไฟล์กลับเป็น response โดยสร้างชื่อไฟล์จากวันที่และเวลาปัจจุบัน
    # กำหนด Timezone ของกรุงเทพฯ
    bangkok_tz = pytz.timezone('Asia/Bangkok')
    local_time = datetime.now(bangkok_tz)
    # สร้างชื่อไฟล์จากวันที่และเวลาท้องถิ่น
    formatted_time = local_time.strftime("%Y%m%d-BKK-%H%M")
    # ส่ง PDF ไฟล์กลับเป็น response
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="padanukkama-{unique_filename}-{formatted_time}.pdf"'
    return response

