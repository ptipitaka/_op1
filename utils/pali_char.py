# ปกติ อักขระบาลี ใช้ symbol หนึ่ง ถีง สอง symbol แทนอักขระ 1 ตัว และปกติเขียนอยู่ในรูปที่หดแล้ว pali_shrink
# แต่ว่า coder จะเห็นเป็น symbol เพียง 1 ตัว
# สร้าง function

'''
  แต่ function ทั้งหมดนี้ ถ้าคำบาลีไม่ถูกไวยากรณ์ ตั้งแต่ ข้อที่ 2 ก็ error ได้
  แต่ถึงไม่ error ก็ไม่แน่ว่า คำนั้นจะถูกหรือไม่
  ดังนั้น ในกรณีนี้ ต้องถือว่าคำนั้นถูกต้องอยู่ก่อน จนกว่า มนุษย์จะตรวจพบ
  1. clean(pali_shrink) คัดอักขระอื่นออกไป
      - ตรวจสอบว่า ถูกไวยากรณ์ของอักขระหรือไม่  ***** ยากมาก ยังไม่ได้ทำ
  2. extract(pali_shrink) ทำให้เป็น list ของอักขระ เพราะบางทีมี 2 symbol
      - วางพยัญชนะ หน้า สระ
      - ประโยชน์ ใช้ในการทำ ตัวรูป
      - ผลลัพธ์ pali_expand เป็น list ของ string
  3. encode(pali_expand) แทน list ของ string ด้วยรหัส
      - พยัญชนะเพียงแค่เอาพินทุออก
      - สระแปลงเป็นตัวเลข 0-7
      - อํ แปลงเป็นเลข 8 เรียงตามความนิยม
      - ประโยชน์เพื่อการเรียงลำดับ และเพื่อประหยัดพื้นที่หน่วยความจำ
      - ผลลัพธ์ pali_code ข้อมูล type sting
  4. decode(pali_code) แปลง pali_code กลับเป็น pali_expand
  5. compress(pali_expand) แปลง pali_expand กลับเป็น pali_shrink
      - วางสระ หน้า หลัง บน ล่าง
'''

space = '\u0020'      # ช่องว่าง
vw_a = '\u0E30'       # สระ -ะ
hanargasa ='\u0E31'   # ไม้หันอากาศ
_r = '\u0E32'         # สระ -า
_i = '\u0E34'         # สระ -ิ
_e = '\u0E35'         # สระ -ี
_u = '\u0E38'         # สระ -ุ
_uu = '\u0E39'        # สระ -ู
pintu ='\u0E3A'       # จุด พินทุ
_ea = '\u0E40'        # สระ -เ
_o = '\u0E42'         # สระ -โ
niccahit ='\u0E4D'    # นิคคหิต
yamaga ='\u0E4E'      # ตัว ยะมะกะ เขียนแทนจุด ของภาษาบาลี

sarani = ['อ','อา','อิ','อี','อุ','อู','เอ','โอ']
payanchanani = [
  'กฺ','ขฺ','คฺ','ฆฺ','งฺ',
  'จฺ','ฉฺ','ชฺ','ฌฺ','ญฺ',
  'ฏฺ','ฐฺ','ฑฺ','ฒฺ','ณฺ',
  'ตฺ','ถฺ','ทฺ','ธฺ','นฺ',
  'ปฺ','ผฺ','พฺ','ภฺ','มฺ',
  'ยฺ','รฺ','ลฺ','วฺ','สฺ','หฺ','ฬฺ']
aukkrani = sarani + payanchanani + ['อํ']
two_voice = ['ยฺ','รฺ','ลฺ','วฺ','หฺ']

pali_symbol = 'อ' + _r + _i + _e + _u + _uu + _ea + _o + 'กขคฆงจฉชฌญฏฐฑฒณตถทธนปผพภมยรลวสหฬ' + pintu + niccahit
vowel = ["อ", "อา","อิ","อี","อุ","อู","เอ","โอ","อํ"]

def clean(pali_shrink):
    res = ''
    for x in pali_shrink:
        if x in pali_symbol:
            res += x
    return res

# ขยายบาลีรูปหด เป็น บาลีรูปขยาย pali_shrink => pali_expand โดยข้อมูลเป็น list
# แล้วต้องจัดเรียง พยัญชนะวางอยู่หน้าสระ
# ช่วงทำ จะแทน อ ด้วย อะ แล้วค่อยเหลือ อ ตอนสุดท้าย
def extract(pali_shrink):
    y = pali_shrink + '????'  # เพื่อจะสังเกตุตัวถัดไปอีก 4  ตัว
    res = ''
    i = 0
    while i < len(y)-4:
        w = y[i:i+4]
        # เ หรือ โ ที่ไม่มี อ ตามหลัง
        if w[0] in [_ea, _o] and w[1] != 'อ':
            if w[2] != pintu: # ตุมฺเห, ทฺเว
                res += w[1]+pintu+w[0]+'อ'  # หฺ-เอ, วฺ-เอ
                i+=2
            else: # ตุเมฺห เทฺว คเณฺหยฺย
                res += w[1]+pintu+w[3]+pintu+w[0]+'อ' # มฺ-หฺ-เอ, ทฺ-วฺ-เอ, ณฺ-หฺ-เอ
                i+=4
        # พยัญชนะ (ที่มี อ อิ อุ ตามหลังแต่ไม่ปรากฏ อ)
        elif (w[0] >='ก' and w[0]<='ฬ') and w[1] != pintu:
            res += w[0]+pintu+'อะ'  # ใส่ อ รอไว้ก่อน
            i+=1
        elif(w[0:2]) == 'อํ':
            res += 'อะอํ'
            i+=2
        # ถ้าเป็น 'อิ', 'อุ', 'อู' อยู่หน้า หรือ อยู่กลางแต่ไม่ถูกลบ 'อ'
        elif w[0:2] in ['อา','อิ','อี', 'อุ', 'อู', 'เอ', 'โอ']:
            res += w[0:2]
            i+=2
        # นิคคหิต ต้องแปลงเป็น อํ
        elif w[0] == niccahit:
            res += 'อํ'
            i+=1
        # ถ้าเป็น สระ หลัง  บน ล่าง ให้ลบ สระ ะ ข้างหน้า
        elif w[0] in [_r, _i, _e, _u, _uu]:
            res = res[:-1] + w[0]
            i+=1

        # ถ้าเป็น อ อยู่หน้า และ ข้างหลังเป็นพยัญชนะ หรือเป็น เ, โ
        elif w[0] == 'อ' and (w[1]<="อ" or w[1]=="เ" or w[1]=="โ") :
            res += 'อะ'
            i+=1
        # เ หรือ โ ที่มี อ ตามหลัง, พยัญชนะสังโยค, pintu
        # นำต่อทีละตัวได้เลย
        else:
            res += w[0]
            i+=1

    # ---- ทำให้เป็น list ของอักขระบาลี ---------------
    pali_expand = []
    for i in range(0, len(res), 2):
        x = res[i:i+2]
        if x == 'อะ':
            pali_expand.append('อ')
        else:
            pali_expand.append(x)
    # ---------------------------------------------

    return pali_expand

# แปลง บาลีรูปขยาย เป็น รหัส pali_expand => pali_code
def encode(pali_expand):
    y = ''
    for x in pali_expand:
        if x in vowel:
            n = vowel.index(x)
            # เปลี่ยน สระ เป็นตัวเลข
            y += str(n)
        else:
            # เอาเฉพาะพยัญชนะ ไม่เอาจุด
            y += x[0]
    return y

# แปลงบาลีรหัส เป็น บาลีรูปขยาย pali_code => pali_expand
def decode(pali_code):
    y = []
    for x in pali_code:
        if x >= '0' and x <= '8':
            y.append(vowel[int(x)])
        else:
            y.append(x+pintu)
    return y

# แปลง บาลีรูปขยาย เป็น บาลีรูปหด  pali_expand => pali_shrink
# ผลลัพธ์จะออกคืนมารูปเดียวเท่านั้น
# ตุมฺเห และ ตุเมฺห กลับเป็น ตุมฺเห
# คณฺเหยฺย และ คเณฺหยฺย กลับเป็น คณฺเหยฺย
def compress(pali_expand):
    last_vowel = ['อ',_r, _i, _e, _u, _uu, niccahit ]
    if len(pali_expand) == 0:
        return []

    y = 'อ' # เดี๋ยวลบออกทีหลัง
    for x in pali_expand:

        #  ตัวสุดท้าย เป็น ตัวสุดท้ายของสระ
        if y[-1] in last_vowel:
            if x == "อํ": # ตามด้วย อํ
                y += str(x[1])
            else: # ตามด้วย พยัญชนะ หรือ สระได้ทั้งนั้น
                y += str(x)

        #  ตัวสุดท้าย เป็น พินทุ แล้ว x เป็น อ
        elif y[-1] == pintu and x == 'อ':
            y = y[:-1]  # ลบ พินทุ  เท่ากับ ลดความยาวไป 1

        #  ตัวสุดท้าย เป็น พินทุ แล้ว x เป็น สระ 2 symbols
        elif y[-1] == pintu and x in vowel:
            if x in [ 'เอ', 'โอ' ]:  # เป็น เอ หรือ โอ
                y = y[:-2] + x[0] + y[-2] # เป็นสระที่ต้องวางหน้า
            else:
                y = y[:-1] + x[1] # เป็น พินทุ ไม่มีทางเจอ อํ
        elif x == "อํ":
            y += niccahit
        else:
            y += x

    return y[1:]  #นำ อ ออกไป


#  รับ (pali_expand, จำนวนอักขระนำ )
#  แปลงเป็นพยางค์

def cv_payangka(pali_expand):
    # อํ กํ อา อพฺย กฺยกฺเย พฺยคฺเฆ ขฺยา ยาตฺรา ยา
    exts = pali_expand
    exts.extend(["?","?","?","?"])
    payanks = []

    i = 0
    while i < len(exts)-4:
        # แต่ละรอบ จบที่ 1 พยางค์
        payank = []
        payank.append(exts[i])
        # สระ นิคคหิต
        if exts[i+1] == "อํ":
            payank.append("อํ")
            i+=2
        # พยัญชนะ สระ นิคคหิต
        elif exts[i+2] == "อํ":
            payank.extend(exts[i+1:i+3])
            i+=3
        # สระ
        elif exts[i] in sarani and exts[i+1] in payanchanani and not exts[i+2] in payanchanani :
            i+=1
        # สระ
        elif exts[i] in sarani and exts[i+1] in sarani:
            i+=1
        else:
            # สระ สังโยค
            if exts[i+1] in payanchanani and exts[i+2] in payanchanani:
                payank.append(exts[i+1])
                i+=2
            # สังโยค พยัญชนะ สระ สังโยค
            elif exts[i+1] in payanchanani and exts[i+2] in sarani and exts[i+3] in payanchanani and exts[i+4] in payanchanani:
                payank.extend(exts[i+1:i+4])
                # กล้ำ เลื่อน 3
                if exts[i+4] in two_voice:
                    i+=3
                # ไม่กล้ำ เลื่อนเพื่มอีก 1
                else:
                    i+=4

            # สังโยค พยัญชนะ สระ
            elif exts[i+1] in payanchanani and exts[i+2] in sarani:
                payank.extend(exts[i+1:i+3])
                i+=3
            # พยัญชนะ สระ สังโยค
            elif exts[i+2] in payanchanani and exts[i+3] in payanchanani:
                payank.extend(exts[i+1:i+3])
                i+=3
            # พยัญชนะ สระ
            else:
                payank.append(exts[i+1])
                i += 2

        payanks.append(payank)

    return payanks


#  รับ บาลีเป็นพยางค์  จำนวน คืน คำแรก ตามจำนวน
def get_first_payangka_roman(pali_payangka, num):
    # อํ กํ อา อพฺย กฺยกฺเย พฺยคฺเฆ ขฺยา ยาตฺรา ยา
    roman = [
        'a','ā','i','ī','u','ū','e','o',
        'k','kh','g','gh','ṅ',
        'c','ch','j','jh','ñ',
        'ṭ','ṭh','ḍ','ḍh','ṇ',
        't','th','d','dh','n',
        'p','ph','b','bh','m',
        'y','r','l','v','s','h','ḷ', 'ṃ']

    result = []
    for payangka in pali_payangka:
        i = aukkrani.index(payangka[0])
        result.append(roman[i])

    l = len(result)
    if num > l:
        num = l

    return result[0:num]


def cv_pali_to_roman(pali_expand):

    roman = [
        'a','ā','i','ī','u','ū','e','o',
        'k','kh','g','gh','ṅ',
        'c','ch','j','jh','ñ',
        'ṭ','ṭh','ḍ','ḍh','ṇ',
        't','th','d','dh','n',
        'p','ph','b','bh','m',
        'y','r','l','v','s','h','ḷ','ṃ']

    y = ''
    for x in pali_expand:
        n = aukkrani.index(x)
        y += roman[n]

    return y


def is_validate_pali(pali_shrink):
    try:
        payankas = cv_payangka(extract(pali_shrink))
        pali_expand = [item for sublist in payankas for item in (sublist if isinstance(sublist, list) else [sublist])]
        cv_pali_to_roman(pali_expand)
        return True
    except:
        return False