# ผลตรวจ Songmai

วันที่: 2026-10-07 (Asia/Bangkok)

## สิ่งที่ตรวจแล้วในเครื่อง

- Python 3.9.6 บน macOS: CLI integration tests 13 ข้อผ่าน โดยเรียกสคริปต์จริงผ่าน subprocess กับไฟล์ใน temporary workspace
- ชื่อไฟล์ไทย/ช่องว่าง, root ระบุเอง, working directory คนละตำแหน่ง, UTF-8 BOM/CRLF และบรรทัดสุดท้ายไม่มี newline ผ่าน
- ไฟล์หาย, directory แทนไฟล์, path ออกนอก root, Windows drive, symlink ออกนอก workspace, section ว่าง/ซ้ำ/ผิดรูปแบบ, input encoding ผิด และ root หาย ถูกปฏิเสธด้วย exit 1
- `--help` ผ่าน; ไม่มี argument ได้ exit 2
- Sample HANDOFF.md ตรวจผ่าน 3 ไฟล์; baseline check fail จริงที่ title assertion ด้วย exit 1 และสำเนาที่ใช้ solution ผ่านด้วย exit 0
- Skill frontmatter ตรวจด้วย skill-creator quick_validate ผ่าน ชื่อและไฟล์ resources อยู่ใน folder เดียวกันสำหรับการติดตั้ง
- ZIP ที่สร้างจาก git แตกใหม่ใน temporary directory แล้วรัน README demo และ CLI tests ผ่าน ไม่รวม .git, scratch workspace หรือ bytecode
- ทดลองติดตั้งโดยคัดลอกเฉพาะ folder ของ Skill ไปตำแหน่งใหม่ แล้วใช้ checker จาก working directory อีกแห่งได้ โดยไม่พึ่งไฟล์จาก repo เดิม

## ทดลองส่งต่อกับ agent ที่มีบริบทใหม่

ใช้ Codex subagents ใน isolated temporary workspace โดยจำกัดสิทธิ์ให้อ่าน/แก้เฉพาะ fixture และ Skill ที่เกี่ยวข้อง:

1. **Control ไม่มี Skill:** agent เขียนสรุปงานและรายงาน baseline FAIL ถูกต้อง แต่ไม่มีส่วนไฟล์อ้างอิงตาม protocol จึงไม่ผ่าน checker การทดสอบนี้แสดงความต่างของรูปแบบเอกสาร ไม่ได้พิสูจน์ว่า agent ไม่มี Skill สรุปงานไม่ได้
2. **ผู้สร้างใช้ Skill:** agent อีกตัวสร้าง HANDOFF.md จากไฟล์จริง checker ผ่าน 3 reference และ hash ของ BRIEF.md, app.py, check_page.py ก่อน/หลังตรงกัน สร้างเอกสารอย่างเดียวตามคำขอ
3. **ผู้รับในบริบทใหม่:** ให้ agent อีกตัวอ่าน Skill และ HANDOFF.md ที่ผู้สร้างเพิ่งทำ โดยไม่ให้อ่านเฉลยหรือข้อมูลจาก agent อื่น ผู้รับรัน baseline ได้ exit 1 แก้ renderer และอัปเดตเอกสาร จากนั้น acceptance check และ checker ได้ exit 0 ทั้งคู่

ตรวจผลของผู้รับซ้ำจากไฟล์จริงแล้ว: title/CTA escape ถูกต้อง ภาษาไทยและ /signup คงเดิม BRIEF.md กับ check_page.py คง hash เดิม

นี่เป็นการทดลองขนาดเล็กหนึ่งงานกับ Codex subagents ไม่ใช่ live Claude → Codex run หรือ benchmark ความแม่นยำข้ามโมเดล

## ข้อจำกัดของหลักฐาน

ตัวอย่าง Claude → Codex ใน README เป็นการจำลอง role ผ่านไฟล์ fixture/solution ไม่ใช่การเปิดบริการ Claude แล้วสั่ง Codex ต่อจริง ไม่ได้วัด token เวลา ค่าใช้จ่าย หรืออัตราความสำเร็จของโมเดล

ตัวตรวจอ่าน HANDOFF.md และตรวจว่าทุก path เป็นไฟล์ภายใน root เท่านั้น ไม่ตรวจความจริงของสรุป ไม่อ่านเนื้อหาไฟล์อ้างอิง ไม่ตรวจว่า code ถูกต้องหรือคำสั่งได้รับอนุญาต และไม่รับประกันว่าข้อมูลจำเป็นถูกแนบมาครบ

ผล `PASS` ของตัวตรวจและผล `PASS` ของ check_page.py เป็นคนละหลักฐาน: baseline handoff อ้างไฟล์ถูกต้องได้ แม้ renderer ยังไม่ผ่าน acceptance check

## รันซ้ำ

จาก root ของชุดแจก:

```sh
python3 -m unittest discover -s tests -v
python3 skills/songmai/scripts/check_handoff.py examples/landing-page/HANDOFF.md --root examples/landing-page
python3 examples/landing-page/check_page.py
```

คำสั่งสุดท้ายตั้งใจ FAIL ให้ใช้ขั้นตอนสำเนาและเฉลยใน [README](../README.md) เพื่อตรวจผลหลังแก้ ไม่แก้ fixture baseline ในชุดแจก

## ผล CI ที่ยืนยันแล้ว

[Run 37577491674](https://github.com/Boom-Vitt/songmai/actions/runs/37577491674) ของ commit `5a47b3f` ผ่านทั้ง 6 jobs: Ubuntu/macOS/Windows × Python 3.9/3.13 โดยแต่ละ job รัน CLI tests, ตรวจ sample handoff และยืนยัน baseline FAIL → solution PASS

โค้ดและ workflow ของ release v1.0.0 เหมือน commit ที่ตรวจนี้ การแก้ถัดมาเพิ่มเอกสารหลักฐานเท่านั้น ดูผลของ commit ปัจจุบันเพิ่มเติมที่ [Actions](https://github.com/Boom-Vitt/songmai/actions)
