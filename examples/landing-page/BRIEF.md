# บรีฟเว็บตัวอย่าง

เป้าหมาย: `render(title, cta)` ต้องแสดง title และ CTA เป็นข้อความที่ escape แล้วสำหรับ HTML

เกณฑ์เสร็จ: รัน `python3 check_page.py` ในโฟลเดอร์ตัวอย่างแล้ว exit code 0 ต้องรักษา `lang="th"` และ URL `/signup`

ขอบเขตที่อนุญาต: แก้ renderer เพื่อผ่านเกณฑ์นี้ ใช้ Python stdlib เท่านั้น ไม่ติดตั้ง dependency ไม่เปลี่ยน URL ไม่เผยแพร่เว็บ

ไฟล์ app.py ปัจจุบันเป็นตัวอย่างที่จงใจยังไม่ escape ข้อความ ใช้ฝึกส่งต่อแบบ offline เท่านั้น
