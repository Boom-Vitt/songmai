<div align="center">

<img src="assets/banner.svg" alt="Songmai — ส่งต่อจากแชตเดิม ผ่าน HANDOFF.md ไปยัง agent ใหม่" width="100%">

# ส่งไม้ให้ AI พร้อมจับงานที่เปลี่ยนไประหว่างทาง

**บันทึกหลักฐานตอนส่ง → ตรวจไฟล์และ Git ตอนรับ → ทำต่อจากสถานะจริง**

แจกฟรี **Skill ภาษาไทย · ตัวตรวจ handoff ล้าสมัย · เทมเพลต · ตัวอย่างรันได้**

[![Check repository](https://github.com/Boom-Vitt/songmai/actions/workflows/check.yml/badge.svg)](https://github.com/Boom-Vitt/songmai/actions/workflows/check.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-BAFF65?style=flat-square)](LICENSE)
[![Language: Thai](https://img.shields.io/badge/Language-ไทย-5AC8D8?style=flat-square)](skills/songmai/SKILL.md)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9%2B-B8C4D7?style=flat-square)](skills/songmai/scripts/songmai.py)

**[เริ่มใช้](#quick-start) · [ลองตัวอย่าง](#demo) · [ติดตั้ง Skill](#install) · [ดูไฟล์ในชุด](#files) · [ผลทดสอบ](docs/TEST-REPORT.md)**

[ดาวน์โหลดชุดไฟล์ ZIP](https://github.com/Boom-Vitt/songmai/archive/refs/heads/main.zip)

</div>

---

> **เริ่มได้จากคำสั่งภาษาไทย** — ไม่ต้องสมัครบริการเพิ่มหรือใส่ API key เพื่อใช้ไฟล์และสคริปต์ในชุดนี้ ส่วน agent ที่เลือกใช้ขึ้นอยู่กับบัญชีของคุณ ตัวตรวจไฟล์ใช้ Python 3.9+ โดยไม่ต้องติดตั้งแพ็กเกจเพิ่ม

## ในชุดนี้มีอะไร

| 🧭 เก็บเป้าหมาย | 🔒 Seal หลักฐาน | 🔎 จับความเปลี่ยนแปลง | 🤝 รับไม้จากของจริง |
| --- | --- | --- | --- |
| บรีฟ · ขอบเขต · งานค้าง | SHA-256 ของเอกสารและไฟล์ · Git | ไฟล์แก้/หาย · เอกสารแก้ · branch/commit/local edits | รายงานจุดที่ต้องอ่านและตรวจใหม่ · ไม่แก้ไฟล์งาน |

เหมาะกับคนที่ทำงานกับ AI หลายแชตหรือหลาย agent แล้วอยากให้ผู้รับเห็นบริบทและงานค้างก่อนทำต่อ

## ต่างจาก handoff ธรรมดายังไง

| Handoff ธรรมดา | Songmai |
| --- | --- |
| สรุปว่า app.py อยู่ในสถานะไหนตอนส่ง | เก็บ fingerprint แล้วบอกได้ว่าเนื้อหา app.py เปลี่ยนไปหลังส่ง |
| ผลทดสอบเก่าเขียนว่า PASS แต่ไฟล์อาจถูกแก้อีกแล้ว | เตือน `STALE` และชี้ไฟล์ที่ต้องอ่าน/ตรวจใหม่ก่อนเชื่อผลเดิม |
| บอกชื่อ branch/commit ให้ผู้รับเทียบเอง | เทียบ branch, HEAD และ local edits ผ่าน Git ให้อัตโนมัติ |
| ต้องรักษารูปแบบและตรวจไฟล์ด้วยตนเอง | Skill สร้างเอกสารพร้อม seal และตรวจ resume ให้จากคำสั่งภาษาไทย |

**ตัวอย่าง:** ส่งงานตอน `app.py` ยังไม่ escape HTML แล้วมีคนแก้ไฟล์ก่อนผู้รับเปิดแชต แม้ชื่อไฟล์ยังเหมือนเดิม Songmai จะรายงาน `CHANGED: app.py` ผู้รับจึงรู้ว่าต้องอ่านและรันเกณฑ์ตรวจใหม่ก่อนทำตามเอกสารเก่า

Songmai ส่งต่อผ่านเอกสารและไฟล์ **ไม่ได้เชื่อมบัญชีหรือย้ายความจำของโมเดลอัตโนมัติ** ผู้รับต้องเข้าถึงไฟล์งานด้วย

Snapshot เป็น fingerprint สำหรับเทียบสถานะ ไม่ใช่ลายเซ็นผู้ส่ง และไม่ตัดสินว่าเนื้อหาหรือผลทดสอบถูกต้อง

---

<a id="quick-start"></a>

## เริ่มใช้ใน 3 ขั้นตอน

### 1 · ให้แชตเดิมสร้าง HANDOFF.md

ดาวน์โหลด ZIP แล้วแตกไฟล์ ให้ local agent อ่าน [SKILL.md](skills/songmai/SKILL.md) และ [เทมเพลต](skills/songmai/templates/HANDOFF.md) จากตำแหน่งที่คุณเก็บชุดแจก จากนั้นสั่ง:

```text
ใช้ Songmai สร้าง HANDOFF.md สำหรับส่งงานนี้ให้ agent ตัวถัดไป
เก็บเป้าหมาย สถานะจริง สิ่งที่ทำแล้ว หลักฐาน ไฟล์อ้างอิง และงานค้างตามลำดับ
รอบนี้สร้างเอกสารส่งต่อและ seal หลักฐานเท่านั้น ไม่เดาผลที่ยังไม่ได้ตรวจ
```

หากใช้แชตบนเว็บ ให้แนบ SKILL.md, เทมเพลต และข้อมูล/ไฟล์ที่ต้องสรุป ใช้ [คำสั่งสร้างแบบเต็ม](skills/songmai/references/CREATE.md) ถ้าต้องการความละเอียดเพิ่ม

### 2 · Seal หลักฐานตอนส่ง

ต้องมี **Python 3.9+** สคริปต์ใช้ standard library เท่านั้น ไม่ต้อง `pip install` จากโฟลเดอร์ songmai รัน:

```sh
python3 skills/songmai/scripts/songmai.py seal "/path/to/project/HANDOFF.md" --root "/path/to/project"
```

ได้ **HANDOFF.songmai.json** ข้างเอกสาร เก็บ hash ของไฟล์อ้างอิงและเอกสาร พร้อม Git ถ้ามี ไม่เก็บเนื้อหาไฟล์หรือ patch ส่ง snapshot ไปพร้อม HANDOFF.md และไฟล์งาน หากใช้ Skill กับ local agent จะเรียกขั้นตอนนี้ให้เอง

แทน path ตัวอย่างด้วยโฟลเดอร์งานของคุณ บน Windows ใช้ `python` แทน `python3` ให้ seal หลังอัปเดตเอกสารและ commit สุดท้ายถ้ามี ถ้ามี snapshot เดิม คำสั่งจะหยุด; ใช้ `seal --replace` หลังตรวจงานและอัปเดตเอกสารแล้วเท่านั้น

### 3 · ให้ agent ใหม่รับไม้

เปิด workspace งานเดียวกัน หรือส่ง HANDOFF.md, HANDOFF.songmai.json พร้อมไฟล์อ้างอิงให้ครบ แล้วสั่ง:

```text
ใช้ Songmai ทำงานต่อจาก HANDOFF.md นี้
ตรวจ resume กับ snapshot ตอนส่ง ถ้า STALE ให้อ่านไฟล์ที่เปลี่ยนและตรวจผลใหม่
ตรวจไฟล์กับ workspace จริง รักษาสิ่งที่อนุมัติและ local edits
ทำงานค้างที่ได้รับอนุญาตแล้วต่อจากจุดเดิม
ตรวจผลแล้วอัปเดต HANDOFF.md ถ้าขาดข้อมูลจำเป็นให้ถามเฉพาะจุดนั้น
```

Skill จะรันคำสั่งนี้ก่อนแก้ไฟล์ ผู้ที่ไม่ได้ติดตั้ง Skill รันเองได้:

```sh
python3 skills/songmai/scripts/songmai.py resume "/path/to/project/HANDOFF.md" --root "/path/to/project"
```

`UNCHANGED` = สถานะตรงกับตอนส่ง, `STALE` = มีสิ่งเปลี่ยน ต้องตรวจใหม่, `UNSEALED` = ไม่มี snapshot จากผู้ส่ง `resume` อ่านอย่างเดียว ไม่ย้อนไฟล์และไม่รันคำสั่งในเอกสาร หลังทำต่อให้อัปเดต HANDOFF.md แล้ว `seal --replace` สำหรับรอบถัดไป

[คำสั่งรับไม้แบบเต็ม](skills/songmai/references/RESUME.md) · [Workflow](WORKFLOW.md)

---

<a id="demo"></a>

## ลองตัวอย่างที่รันได้

### ลองจับ handoff ล้าสมัยด้วยตนเอง

จากโฟลเดอร์ songmai เตรียมสำเนาใหม่ใน `runs/stale-demo` แล้วส่งไม้:

```sh
python3 -c "import shutil; shutil.copytree('examples/landing-page', 'runs/stale-demo', ignore=shutil.ignore_patterns('__pycache__'))"
python3 skills/songmai/scripts/songmai.py seal runs/stale-demo/HANDOFF.md
python3 skills/songmai/scripts/songmai.py resume runs/stale-demo/HANDOFF.md
```

ได้ `SEALED` แล้ว `UNCHANGED` จากนั้นจำลองว่ามีคนแก้ app.py ระหว่างทาง:

```sh
python3 -c "import shutil; shutil.copyfile('runs/stale-demo/solution/app.py', 'runs/stale-demo/app.py')"
python3 skills/songmai/scripts/songmai.py resume runs/stale-demo/HANDOFF.md
```

ต้องได้ **`CHANGED: app.py` และ `STALE`, exit 1** ทั้งที่ไฟล์ยังอยู่ครบ นี่คือสิ่งที่การอ่าน handoff หรือเช็คไฟล์อยู่เฉย ๆ จับให้ไม่ได้ ผู้รับต้องตรวจผลใหม่:

```sh
python3 runs/stale-demo/check_page.py
```

ผลต้องเป็น `PASS: title and CTA are escaped; Thai language and signup URL preserved.` Snapshot เก่าไม่ได้ถูกทับ ใช้โฟลเดอร์ชื่อใหม่หาก `runs/stale-demo` มีอยู่แล้ว

### ตัวอย่างงานที่ส่งต่อ

**ตัวอย่างจำลอง Claude → Codex:** agent แรกทำ renderer ไว้แล้ว แต่ยังไม่ escape ข้อความ ผู้รับอ่านบรีฟกับ handoff แล้วแก้ต่อให้ผ่านเกณฑ์ ทั้งหมดรัน offline ไม่ใช้บัญชีหรือเครดิต

จากโฟลเดอร์ songmai:

```sh
python3 skills/songmai/scripts/check_handoff.py examples/landing-page/HANDOFF.md --root examples/landing-page
python3 examples/landing-page/check_page.py
```

คำสั่งแรกต้องได้ `PASS: 3…` คำสั่งที่สอง **ตั้งใจให้ FAIL, exit 1** ที่ `title must be escaped as HTML text` เพื่อให้เห็นงานค้างจริง อ่าน [HANDOFF.md](examples/landing-page/HANDOFF.md) แล้วให้ agent ทำต่อในสำเนาตัวอย่าง

| ไฟล์ตัวอย่าง | เปิดดู |
| --- | --- |
| เป้าหมายและเกณฑ์ตรวจเว็บ | [BRIEF.md →](examples/landing-page/BRIEF.md) |
| เอกสารส่งงานจาก agent แรก | [HANDOFF.md →](examples/landing-page/HANDOFF.md) |
| ตัวตรวจและเฉลยสำหรับเทียบผล | [ตัวตรวจ →](examples/landing-page/check_page.py) · [เฉลย →](examples/landing-page/solution/app.py) |

<details>
<summary><strong>ลองผลก่อน/หลังด้วยไฟล์เฉลย</strong></summary>

ถ้าอยากลองผลก่อน/หลังด้วยตนเอง ให้เตรียมสำเนาใน `runs/demo` ซึ่งไม่ทับต้นฉบับ:

```sh
python3 -c "import shutil; shutil.copytree('examples/landing-page', 'runs/demo', ignore=shutil.ignore_patterns('__pycache__'))"
python3 -c "import shutil; shutil.copyfile('runs/demo/solution/app.py', 'runs/demo/app.py')"
python3 runs/demo/check_page.py
```

ผลหลังใช้เฉลยต้องเป็น `PASS: title and CTA are escaped; Thai language and signup URL preserved.` นี่เป็นการใช้ไฟล์เฉลยที่ให้มา ไม่ใช่หลักฐานว่า Claude/Codex ทำงานจริง คำสั่ง `copytree` จะปฏิเสธหาก runs/demo มีอยู่แล้ว ให้ใช้ชื่อโฟลเดอร์ทดลองใหม่แทน

</details>

---

<a id="install"></a>

## ติดตั้งเป็น Skill ใน local agent

ไม่จำเป็นต้องติดตั้งเพื่อใช้คำสั่งด้านบน หากอยากเรียกด้วยชื่อ ให้รันจากโฟลเดอร์ songmai **เลือก agent ที่ใช้**:

<details>
<summary><strong>Codex — ติดตั้งแล้วเรียกด้วย $songmai</strong></summary>

**Codex** — ติดตั้งครบทั้งคำสั่ง เทมเพลต และสคริปต์:

```sh
python3 -c "from pathlib import Path; import shutil; shutil.copytree('skills/songmai', Path.home()/'.agents/skills/songmai')"
```

เปิด session ใหม่ แล้วเรียก `$songmai สร้าง HANDOFF.md` หรือ `$songmai ทำต่อจาก HANDOFF.md` ตำแหน่ง user skills อ้างอิง [เอกสาร Codex](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)

</details>

<details>
<summary><strong>Claude Code — ติดตั้งแล้วเรียกด้วย /songmai</strong></summary>

**Claude Code**:

```sh
python3 -c "from pathlib import Path; import shutil; shutil.copytree('skills/songmai', Path.home()/'.claude/skills/songmai')"
```

เปิด session ใหม่ แล้วเรียก `/songmai สร้าง HANDOFF.md` หรือ `/songmai ทำต่อจาก HANDOFF.md` ตาม [เอกสาร Claude Code](https://code.claude.com/docs/en/skills)

</details>

คำสั่งติดตั้งทั้งสองจะหยุดหากมีโฟลเดอร์ songmai อยู่แล้ว เพื่อไม่ทับ Skill เดิม บน Windows เปลี่ยน `python3` เป็น `python`

---

<a id="files"></a>

## ในชุดแจก

| ไฟล์ | ใช้ทำอะไร |
| --- | --- |
| [Skill](skills/songmai/SKILL.md) | เลือกวิธีสร้างหรือรับไม้ |
| [เทมเพลต HANDOFF](skills/songmai/templates/HANDOFF.md) | กรอกเป้าหมาย หลักฐาน และงานค้าง |
| [คำสั่งสร้าง](skills/songmai/references/CREATE.md) / [รับไม้](skills/songmai/references/RESUME.md) | คัดลอกใช้ในแชต |
| [ตัวตรวจ](skills/songmai/scripts/check_handoff.py) | ตรวจไฟล์อ้างอิงใน workspace แบบ read-only |
| [Songmai CLI](skills/songmai/scripts/songmai.py) | seal หลักฐาน แล้ว resume ตรวจว่าเอกสาร ไฟล์ หรือ Git เปลี่ยนไปหรือยัง |
| [ตัวอย่างเว็บ](examples/landing-page/BRIEF.md) | ทดลอง baseline → handoff → งานที่แก้แล้ว |
| [ผลตรวจและข้อจำกัด](docs/TEST-REPORT.md) | ดูว่าได้ทดสอบอะไรจริง |

## ตรวจชุดแจก

<details>
<summary><strong>รันชุดทดสอบในเครื่อง</strong></summary>

```sh
python3 -m unittest discover -s tests -v
```

</details>

CI ใช้ Ubuntu, macOS และ Windows ตรวจ CLI และตัวอย่าง baseline/solution ดูสถานะจริงได้ที่ [Actions](https://github.com/Boom-Vitt/songmai/actions)

---

**ฟรี · ใช้ได้ · แก้ได้ · Fork ได้ · แจกต่อได้** — โค้ดและเอกสารต้นฉบับใน repo นี้ใช้ [MIT License](LICENSE) โดยคงประกาศสิทธิ์ไว้

ชื่อ Claude, Codex และ ChatGPT เป็นชื่อผลิตภัณฑ์ของเจ้าของแต่ละราย Songmai เป็นโครงการอิสระของ BoomBigNose
