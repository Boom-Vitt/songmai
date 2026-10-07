# ผลตรวจ Songmai

วันที่: 2026-10-07 (Asia/Bangkok)

## สิ่งที่ตรวจแล้วในเครื่อง

- Python 3.9.6 บน macOS: CLI integration tests 13 ข้อผ่าน โดยเรียกสคริปต์จริงผ่าน subprocess กับไฟล์ใน temporary workspace
- ชื่อไฟล์ไทย/ช่องว่าง, root ระบุเอง, working directory คนละตำแหน่ง, UTF-8 BOM/CRLF และบรรทัดสุดท้ายไม่มี newline ผ่าน
- ไฟล์หาย, directory แทนไฟล์, path ออกนอก root, Windows drive, symlink ออกนอก workspace, section ว่าง/ซ้ำ/ผิดรูปแบบ, input encoding ผิด และ root หาย ถูกปฏิเสธด้วย exit 1
- `--help` ผ่าน; ไม่มี argument ได้ exit 2
- Sample HANDOFF.md ตรวจผ่าน 3 ไฟล์; baseline check fail จริงที่ title assertion ด้วย exit 1 และสำเนาที่ใช้ solution ผ่านด้วย exit 0
- Skill frontmatter ตรวจด้วย skill-creator quick_validate ผ่าน ชื่อและไฟล์ resources อยู่ใน folder เดียวกันสำหรับการติดตั้ง

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

CI ตรวจบน Ubuntu/macOS/Windows กับ Python 3.9 และ 3.13 ดูผลของ commit ปัจจุบันที่ [Actions](https://github.com/Boom-Vitt/songmai/actions) การมี workflow file เพียงอย่างเดียวไม่พิสูจน์ว่าทุก OS ผ่านแล้ว
