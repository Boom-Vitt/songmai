# ส่งไม้ใน 4 ขั้นตอน

1. **แชตเดิมสร้างเอกสาร** — ใช้ [คำสั่งสร้าง](skills/songmai/references/CREATE.md) กับ [เทมเพลต](skills/songmai/templates/HANDOFF.md) ให้ agent อ่านไฟล์และผลตรวจจริง
2. **ตรวจชุดส่งต่อ** — รัน `python3 skills/songmai/scripts/check_handoff.py HANDOFF.md --root .` จาก repo ชุดแจก หรือใช้ path เต็มของสคริปต์เมื่ออยู่ในโปรเจกต์อื่น ตรวจอ่านเนื้อหาด้วยว่าเป้าหมายและงานค้างตรงคำสั่งผู้ใช้
3. **ส่งไฟล์ไปพร้อมงาน** — ถ้าใช้ workspace เดียวกัน ให้ agent ใหม่อ่าน HANDOFF.md; ถ้าย้ายเครื่อง ส่ง repo/ไฟล์อ้างอิงด้วย ถ้าเป็นแชตบนเว็บ แนบไฟล์ที่จำเป็นและ SKILL.md แทนการอ้าง path ที่แชตอ่านไม่ได้
4. **ผู้รับทำต่อและบันทึก** — ใช้ [คำสั่งรับไม้](skills/songmai/references/RESUME.md) ตรวจสถานะล่าสุด รันเกณฑ์เสร็จ และอัปเดต HANDOFF.md

## ตีความผลตรวจ

| สถานะ | ความหมาย |
| --- | --- |
| `PASS: N file references…` | N เส้นทางเป็นไฟล์ที่อยู่ใน workspace ณ เวลาตรวจ |
| `FAIL: missing file…` | อ้างไฟล์ที่ไม่มีอยู่หรือเป็น directory; แก้เอกสารจากไฟล์จริงหรือส่งไฟล์ให้ครบ |
| `FAIL: unsafe path…` / `outside workspace…` | ใช้ absolute path, parent traversal, Windows drive/backslash หรือ symlink ออกนอก root |
| `FAIL: malformed…` / `empty…` | ส่วนอ้างอิงเขียนไม่ตรงรูปแบบ ต้องมี backticks และหนึ่งไฟล์ต่อบรรทัด |
| `CHECKER_NOT_RUN` | ยังไม่ได้ใช้สคริปต์ตรวจ ไม่ใช่ PASS |

Exit code: `0` ผ่านการตรวจอ้างอิง, `1` เอกสาร/ไฟล์ไม่ผ่าน, `2` ใช้ CLI ผิดรูปแบบ

## รูปแบบไฟล์อ้างอิง

```markdown
## ไฟล์อ้างอิง

- `src/หน้า เว็บ.py` — renderer; ตรวจฟังก์ชัน render ที่บรรทัด 12
- `README.md` — เกณฑ์ส่งงาน

## ผลตรวจและคำสั่ง
```

ใช้ `/` ใน path แม้บน Windows; path สัมพันธ์กับ `--root` ถ้าไม่กำหนด root จะใช้โฟลเดอร์ของ HANDOFF.md รองรับ UTF-8, UTF-8 BOM และ CRLF ไม่รองรับ wildcard, URL, directory หรือเลขบรรทัดในตัว path

ตัวตรวจไม่อ่านเนื้อหาไฟล์อ้างอิง ไม่ตรวจว่าคำสั่งในเอกสารปลอดภัย ไม่ตัดสินว่างานเสร็จ และไม่ตรวจความลับอัตโนมัติ ผู้ส่งต้องตรวจสิ่งที่จะส่งด้วยตนเอง
