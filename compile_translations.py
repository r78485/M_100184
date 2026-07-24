import os
import struct

BASE_DIR = r"f:\M_100184"
LOCALE_DIR = os.path.join(BASE_DIR, 'locale', 'bn', 'LC_MESSAGES')
os.makedirs(LOCALE_DIR, exist_ok=True)

PO_FILE = os.path.join(LOCALE_DIR, 'django.po')

translations = {
    "General Settings — EduManage ERP": "সাধারণ সেটিংস — এডুম্যানেজ ইআরপি",
    "Interface Language": "ইন্টারফেস ভাষা",
    "Save Preferences": "সেটিংস সেভ করুন",
    "Core Administration": "কোর এডমিনিস্ট্রেশন",
    "Dashboard": "ড্যাশবোর্ড",
    "General Settings": "সাধারণ সেটিংস",
    "Academic & Students": "একাডেমিক এবং শিক্ষার্থী",
    "Admissions": "ভর্তি",
    "Classes & Sections": "ক্লাস ও সেকশন",
    "Subjects": "বিষয়সমূহ",
    "Students": "শিক্ষার্থীবৃন্দ",
    "Employees": "কর্মচারীবৃন্দ",
    "Financials & ERP": "অর্থনীতি ও ইআরপি",
    "Accounts": "অ্যাকাউন্টস",
    "Fees": "ফি",
    "Salary": "বেতন",
    "Online Store & POS": "অনলাইন স্টোর ও পস",
}

po_content = """msgid ""
msgstr ""
"Project-Id-Version: EduManage ERP\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: 2026-07-20 00:00+0000\\n"
"PO-Revision-Date: 2026-07-20 00:00+0000\\n"
"Language: bn\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"

"""

for eng, bn in translations.items():
    po_content += f'msgid "{eng}"\nmsgstr "{bn}"\n\n'

with open(PO_FILE, 'w', encoding='utf-8') as f:
    f.write(po_content)

print("Created django.po successfully.")

def generate_mo(po_dict, output_path):
    keys = sorted(po_dict.keys())
    offsets = []
    ids = b''
    strs = b''

    for k in keys:
        v = po_dict[k]
        k_enc = k.encode('utf-8')
        v_enc = v.encode('utf-8')
        offsets.append((len(k_enc), len(ids), len(v_enc), len(strs)))
        ids += k_enc + b'\0'
        strs += v_enc + b'\0'

    output = bytearray()
    output.extend(struct.pack('<I', 0x950412de))
    output.extend(struct.pack('<I', 0))
    output.extend(struct.pack('<I', len(keys)))
    
    orig_table_offset = 28
    trans_table_offset = 28 + 8 * len(keys)
    hash_table_size = 0
    hash_table_offset = 28 + 16 * len(keys)
    
    output.extend(struct.pack('<I', orig_table_offset))
    output.extend(struct.pack('<I', trans_table_offset))
    output.extend(struct.pack('<I', hash_table_size))
    output.extend(struct.pack('<I', hash_table_offset))

    for length, offset, _, _ in offsets:
        output.extend(struct.pack('<I', length))
        output.extend(struct.pack('<I', orig_table_offset + 8 * len(keys) * 2 + offset))

    for _, _, length, offset in offsets:
        output.extend(struct.pack('<I', length))
        output.extend(struct.pack('<I', orig_table_offset + 8 * len(keys) * 2 + len(ids) + offset))

    output.extend(ids)
    output.extend(strs)

    with open(output_path, 'wb') as f:
        f.write(output)

mo_dict = {"": "Project-Id-Version: EduManage ERP\\nReport-Msgid-Bugs-To: \\nPOT-Creation-Date: 2026-07-20 00:00+0000\\nPO-Revision-Date: 2026-07-20 00:00+0000\\nLanguage: bn\\nMIME-Version: 1.0\\nContent-Type: text/plain; charset=UTF-8\\nContent-Transfer-Encoding: 8bit\\n"}
for eng, bn in translations.items():
    mo_dict[eng] = bn

MO_FILE = os.path.join(LOCALE_DIR, 'django.mo')
generate_mo(mo_dict, MO_FILE)

print("Created django.mo successfully.")
