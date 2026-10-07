# ส่งไม้: แก้ renderer เว็บภาษาไทย

สถานะ: ตัวอย่างจำลอง Claude → Codex; ไม่ใช่ผลรันจริงจากบริการทั้งสอง
สร้างและตรวจครั้งแรก: 2026-10-07 Asia/Bangkok

## เป้าหมายและเกณฑ์เสร็จ

ให้ `render(title, cta)` escape ข้อความทั้งสองสำหรับ HTML โดยผ่าน `python3 check_page.py` ด้วย exit code 0 พร้อมรักษา `lang="th"` และ URL `/signup`

## ขอบเขตและสิทธิ์ที่มี

BRIEF.md อนุญาตแก้ renderer เพื่อให้ผ่านเกณฑ์นี้ ใช้ Python stdlib ไม่ติดตั้ง dependency ไม่เปลี่ยน URL และไม่เผยแพร่เว็บ การสร้างเอกสารส่งต่อไม่ยกเลิกสิทธิ์แก้งานค้างที่บรีฟอนุญาตไว้

## สถานะที่ตรวจพบ

Workspace root สำหรับตัวอย่างนี้: โฟลเดอร์ `examples/landing-page` จาก repo ชุดแจก หรือสำเนาโฟลเดอร์นี้ที่ผู้ใช้เตรียมให้ทดลอง
Git branch / commit: NOT_APPLICABLE สำหรับโฟลเดอร์ตัวอย่างเดี่ยว; ผู้รับต้องตรวจ repo ของตนใหม่
Local edits ในชุดแจกต้นฉบับ: ไม่มีการแก้ fixture baseline หลังจัดทำเอกสารนี้; สถานะสำเนาของผู้รับ UNKNOWN

## งานที่ทำแล้ว

- มี app.py renderer พื้นฐานและ check_page.py เกณฑ์ตรวจที่รันได้
- รัน baseline check แล้ว FAIL ที่ title assertion ด้วย exit code 1
- Assertion ของ CTA และการรักษาภาษา/URL อยู่หลังจุดที่ fail จึงยังไม่ได้พิสูจน์จาก baseline run นี้

## การตัดสินใจที่ต้องรักษา

แก้ตรง renderer ที่ shared caller ใช้ ไม่เปลี่ยนเกณฑ์ตรวจเพื่อให้ผ่าน ใช้ `html.escape` จาก stdlib กับ title และ CTA รักษา HTML และ URL เดิม

## ไฟล์อ้างอิง

- `BRIEF.md` — เป้าหมาย เกณฑ์เสร็จ และขอบเขตที่ได้รับอนุญาต
- `app.py` — renderer ที่ยังแทรก title และ CTA ลง HTML โดยตรง
- `check_page.py` — เกณฑ์ตรวจที่ต้องผ่านหลังแก้

## ผลตรวจและคำสั่ง

| คำสั่ง | Working directory | ผลที่สังเกตจริง | เวลา / ข้อจำกัด |
| --- | --- | --- | --- |
| `python3 check_page.py` | workspace root ของตัวอย่าง | FAIL, exit 1: title must be escaped as HTML text | 2026-10-07; ผลเดิม ผู้รับต้องรันใหม่ |

## งานถัดไปตามลำดับ

1. อ่าน BRIEF.md, app.py และ check_page.py แล้วตรวจ local edits ก่อนแก้
2. รัน check_page.py เพื่อยืนยันว่า baseline ปัจจุบันยังมีปัญหาเดิม
3. แก้ renderer ให้ใช้ `html.escape` กับ title และ CTA แล้วรัน check_page.py ใหม่
4. ต้องได้ exit 0 และ `PASS: title and CTA are escaped; Thai language and signup URL preserved.` อัปเดต HANDOFF.md ด้วยผลที่รันจริง

## สิ่งที่ติด / ยังไม่ทราบ

ไม่มี blocker ใน fixture นี้; Python, git และสถานะสำเนาของผู้รับต้องตรวจใหม่

## คำสั่งรับไม้

ใช้ Songmai อ่านเอกสารนี้และไฟล์อ้างอิง เทียบกับ workspace จริง แล้วทำงานแก้ renderer ที่ BRIEF.md อนุญาตไว้ต่อ ตรวจเกณฑ์เสร็จและอัปเดตเอกสารนี้
