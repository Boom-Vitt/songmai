<div align="center">

<img src="assets/banner.svg" alt="Songmai — ส่งต่อจากแชตเดิม ผ่าน HANDOFF.md ไปยัง agent ใหม่" width="100%">

# ส่งไม้ให้ AI แล้วทำงานต่อจากจุดเดิม

**เปลี่ยนจาก Claude ไป Codex หรือเปิดแชตใหม่ โดยส่งเป้าหมาย สถานะจริง และงานค้างไปด้วย**

แจกฟรี **Skill · เทมเพลต · คำสั่งภาษาไทย · ตัวอย่างรันได้**

[![Check repository](https://github.com/Boom-Vitt/songmai/actions/workflows/check.yml/badge.svg)](https://github.com/Boom-Vitt/songmai/actions/workflows/check.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-BAFF65?style=flat-square)](LICENSE)
[![Language: Thai](https://img.shields.io/badge/Language-ไทย-5AC8D8?style=flat-square)](skills/songmai/SKILL.md)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9%2B-B8C4D7?style=flat-square)](skills/songmai/scripts/check_handoff.py)

**[เริ่มใช้](#quick-start) · [ลองตัวอย่าง](#demo) · [ติดตั้ง Skill](#install) · [ดูไฟล์ในชุด](#files) · [ผลทดสอบ](docs/TEST-REPORT.md)**

[ดาวน์โหลดชุดไฟล์ ZIP](https://github.com/Boom-Vitt/songmai/archive/refs/heads/main.zip)

</div>

---

> **เริ่มได้จากคำสั่งภาษาไทย** — ไม่ต้องสมัครบริการเพิ่มหรือใส่ API key เพื่อใช้ไฟล์และสคริปต์ในชุดนี้ ส่วน agent ที่เลือกใช้ขึ้นอยู่กับบัญชีของคุณ ตัวตรวจไฟล์ใช้ Python 3.9+ โดยไม่ต้องติดตั้งแพ็กเกจเพิ่ม

## ในชุดนี้มีอะไร

| 🧭 เก็บเป้าหมาย | 📂 บันทึกสถานะ | 🤝 ส่งต่อและรับไม้ | ✅ ตรวจไฟล์ |
| --- | --- | --- | --- |
| บรีฟ · ขอบเขต · สิ่งที่อนุมัติ | งานที่ทำแล้ว · หลักฐาน · งานค้าง | Skill · เทมเพลต · คำสั่งภาษาไทย | รายการไฟล์ relative · ตัวตรวจ read-only |

เหมาะกับคนที่ทำงานกับ AI หลายแชตหรือหลาย agent แล้วอยากให้ผู้รับเห็นบริบทและงานค้างก่อนทำต่อ

## ก่อน → หลัง

| ก่อนส่งไม้ | หลังส่งไม้ |
| --- | --- |
| “ทำต่อให้หน่อย” แต่ agent ใหม่ไม่เห็นงานเดิม | HANDOFF.md บอกเป้าหมาย สถานะ และจุดที่จะทำต่อ |
| จำไม่ได้ว่าเคยทดสอบอะไรแล้ว | มีคำสั่ง ผลที่รันจริง และส่วนที่ยัง NOT_RUN |
| อ้างชื่อไฟล์เก่าหรือ path ที่อีกเครื่องอ่านไม่ได้ | มีรายการไฟล์ relative และสคริปต์ตรวจว่าไฟล์ยังอยู่ |

Songmai ส่งต่อผ่านเอกสารและไฟล์ **ไม่ได้เชื่อมบัญชีหรือย้ายความจำของโมเดลอัตโนมัติ** ผู้รับต้องเข้าถึงไฟล์งานด้วย

---

<a id="quick-start"></a>

## เริ่มใช้ใน 3 ขั้นตอน

### 1 · ให้แชตเดิมสร้าง HANDOFF.md

ดาวน์โหลด ZIP แล้วแตกไฟล์ ให้ local agent อ่าน [SKILL.md](skills/songmai/SKILL.md) และ [เทมเพลต](skills/songmai/templates/HANDOFF.md) จากตำแหน่งที่คุณเก็บชุดแจก จากนั้นสั่ง:

```text
ใช้ Songmai สร้าง HANDOFF.md สำหรับส่งงานนี้ให้ agent ตัวถัดไป
เก็บเป้าหมาย สถานะจริง สิ่งที่ทำแล้ว หลักฐาน ไฟล์อ้างอิง และงานค้างตามลำดับ
รอบนี้สร้างเอกสารส่งต่อเท่านั้น ไม่เดาผลที่ยังไม่ได้ตรวจ
```

หากใช้แชตบนเว็บ ให้แนบ SKILL.md, เทมเพลต และข้อมูล/ไฟล์ที่ต้องสรุป ใช้ [คำสั่งสร้างแบบเต็ม](skills/songmai/references/CREATE.md) ถ้าต้องการความละเอียดเพิ่ม

### 2 · ตรวจไฟล์อ้างอิง

ต้องมี **Python 3.9+** สคริปต์ใช้ standard library เท่านั้น ไม่ต้อง `pip install` จากโฟลเดอร์ songmai รัน:

```sh
python3 skills/songmai/scripts/check_handoff.py "/path/to/project/HANDOFF.md" --root "/path/to/project"
```

แทน path ตัวอย่างด้วยโฟลเดอร์งานของคุณ บน Windows ใช้ `python` แทน `python3` และใส่ path ในเครื่องของคุณ `PASS` ยืนยันเพียงว่าไฟล์อ้างอิงอยู่จริง อ่าน [ความหมายของผลตรวจ](WORKFLOW.md) ก่อนสรุปว่างานพร้อมส่ง

### 3 · ให้ agent ใหม่รับไม้

เปิด workspace งานเดียวกัน หรือส่ง HANDOFF.md พร้อมไฟล์อ้างอิงให้ครบ แล้วสั่ง:

```text
ใช้ Songmai ทำงานต่อจาก HANDOFF.md นี้
ตรวจไฟล์กับ workspace จริง รักษาสิ่งที่อนุมัติและ local edits
ทำงานค้างที่ได้รับอนุญาตแล้วต่อจากจุดเดิม
ตรวจผลแล้วอัปเดต HANDOFF.md ถ้าขาดข้อมูลจำเป็นให้ถามเฉพาะจุดนั้น
```

[คำสั่งรับไม้แบบเต็ม](skills/songmai/references/RESUME.md) · [Workflow](WORKFLOW.md)

---

<a id="demo"></a>

## ลองตัวอย่างที่รันได้

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
