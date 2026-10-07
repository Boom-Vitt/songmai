# ส่งไม้ใน 4 ขั้นตอน

1. **แชตเดิมสร้างเอกสาร** — ใช้ [คำสั่งสร้าง](skills/songmai/references/CREATE.md) กับ [เทมเพลต](skills/songmai/templates/HANDOFF.md) ให้ agent อ่านไฟล์และผลตรวจจริง
2. **Seal หลักฐานตอนส่ง** — หลังเขียน HANDOFF.md และ commit สุดท้ายที่ได้รับอนุญาตถ้ามี รัน `python3 skills/songmai/scripts/songmai.py seal HANDOFF.md --root .` ได้ HANDOFF.songmai.json ข้างเอกสาร ถ้าอยู่ในโปรเจกต์อื่นใช้ path เต็มของสคริปต์ Skill อ่านเนื้อหาด้วยว่าเป้าหมายและงานค้างตรงคำสั่งผู้ใช้
3. **ผู้รับตรวจ resume ก่อนแก้ไฟล์** — ส่ง HANDOFF.md, snapshot และ repo/ไฟล์อ้างอิงไปด้วยกัน แล้วรัน `python3 skills/songmai/scripts/songmai.py resume HANDOFF.md --root .` ใช้ [คำสั่งรับไม้](skills/songmai/references/RESUME.md) หาก STALE ให้อ่านสิ่งที่เปลี่ยนและรันเกณฑ์ตรวจใหม่ก่อนเชื่อผลเดิม
4. **ทำต่อและส่งรอบถัดไป** — รักษา local edits และสิทธิ์เดิม ทำงานค้าง ตรวจเกณฑ์เสร็จ อัปเดต HANDOFF.md แล้ว `seal --replace` เพื่อบันทึกหลักฐานใหม่ ไม่ seal ทับเพื่อปิดคำเตือนโดยไม่ได้ตรวจงาน

หากเป็นแชตบนเว็บที่รันสคริปต์ไม่ได้ แนบไฟล์ที่จำเป็นและ SKILL.md พร้อมรายงานข้อจำกัด `RESUME_NOT_RUN` แทนการอ้างว่าได้ตรวจไฟล์ในเครื่องแล้ว

## ตีความผลตรวจ

| สถานะ | ความหมาย |
| --- | --- |
| `SEALED` | บันทึก fingerprint เอกสาร ไฟล์ที่อ้าง และ Git ถ้ามี ไม่ได้ยืนยันว่าเนื้อหาถูกต้อง |
| `UNCHANGED` | เอกสารและหลักฐานที่ตรวจครอบคลุมตรงกับตอน seal ไม่ได้ยืนยันว่างานผ่านหรือพร้อม deploy |
| `CHANGED: path` / `HANDOFF_CHANGED` | เนื้อหาไฟล์/เอกสารต่างจากตอนส่ง ให้อ่านจุดที่เปลี่ยนและตรวจผลใหม่ |
| `REFERENCE_ADDED` / `REFERENCE_REMOVED` | รายการไฟล์ในเอกสารถูกเปลี่ยน; ตรวจว่าข้อมูลส่งต่อยังครบ |
| `GIT_BRANCH_CHANGED` / `GIT_HEAD_CHANGED` / `GIT_WORKTREE_CHANGED` | branch, commit หรือ local edits ต่างจากตอน seal; ตรวจ Git ก่อนทำตามบริบทเก่า |
| `GIT_CONTEXT_CHANGED` | จากมี Git เป็นไม่มี หรือกลับกัน; ไม่มีหลักฐานเทียบ Git ชุดเดียวกัน |
| `STALE` | อย่างน้อยหนึ่งหลักฐานเปลี่ยน ไม่ได้แปลว่าโค้ดผิด แต่ผลทดสอบเก่าต้องตรวจใหม่ |
| `UNSEALED` | ไม่พบ snapshot จากผู้ส่ง ห้ามสร้างใหม่แล้วอ้างว่าตรงกับตอนส่ง |
| `GIT_NOT_CHECKED` | ไม่ได้ตรวจ Git เพราะไม่มี repo หรือ executable; ยังเทียบเอกสารและไฟล์ที่อ้างได้ |
| `PASS: N file references…` | N เส้นทางเป็นไฟล์ที่อยู่ใน workspace ณ เวลาตรวจ |
| `FAIL: missing file…` | อ้างไฟล์ที่ไม่มีอยู่หรือเป็น directory; แก้เอกสารจากไฟล์จริงหรือส่งไฟล์ให้ครบ |
| `FAIL: unsafe path…` / `outside workspace…` | ใช้ absolute path, parent traversal, Windows drive/backslash หรือ symlink ออกนอก root |
| `FAIL: malformed…` / `empty…` | ส่วนอ้างอิงเขียนไม่ตรงรูปแบบ ต้องมี backticks และหนึ่งไฟล์ต่อบรรทัด |
| `SEAL_NOT_RUN` / `RESUME_NOT_RUN` / `CHECKER_NOT_RUN` | ยังไม่ได้รันขั้นตอนนั้น ไม่ใช่ผลผ่าน |

Exit code: `0` seal สำเร็จ/สถานะไม่เปลี่ยน/ตัวตรวจเดิมผ่าน, `1` STALE หรือเอกสาร/ไฟล์/หลักฐานไม่ผ่าน, `2` ใช้ CLI ผิดรูปแบบ

`seal` เขียนเฉพาะ snapshot ข้างเอกสาร ค่าเริ่มต้นไม่ทับไฟล์เดิม `--replace` แทนได้เฉพาะ snapshot ที่ตรง schema และไม่เป็น symlink `resume` กับ `check_handoff.py` อ่านอย่างเดียว ไม่แก้ไฟล์งานและไม่รันคำสั่งจากเอกสาร

## รูปแบบไฟล์อ้างอิง

```markdown
## ไฟล์อ้างอิง

- `src/หน้า เว็บ.py` — renderer; ตรวจฟังก์ชัน render ที่บรรทัด 12
- `README.md` — เกณฑ์ส่งงาน

## ผลตรวจและคำสั่ง
```

ใช้ `/` ใน path แม้บน Windows; path สัมพันธ์กับ `--root` ถ้าไม่กำหนด root จะใช้โฟลเดอร์ของ HANDOFF.md รองรับ UTF-8, UTF-8 BOM และ CRLF ไม่รองรับ wildcard, URL, directory หรือเลขบรรทัดในตัว path

ตัวตรวจเดิม `check_handoff.py` ไม่อ่านเนื้อหาไฟล์อ้างอิง ส่วน Songmai seal/resume อ่านเพื่อคำนวณ SHA-256 แต่ไม่เก็บเนื้อหาไฟล์ Git fingerprint ครอบคลุม branch/HEAD, staged/unstaged tracked diff และสถานะ/รายชื่อ untracked ใน root ที่เลือก ไม่ hash เนื้อหา untracked ที่ไม่ได้อยู่ในส่วนอ้างอิง ไม่ตรวจ ignored files ที่ไม่ได้อ้าง และไม่เทียบไฟล์นอก root

Snapshot ไม่มี absolute workspace path หรือ patch แต่มีรายชื่อไฟล์ ชื่อ branch และ commit; ตรวจสิ่งที่จะส่งด้วยตนเอง Hash เป็นหลักฐานเทียบสถานะ ไม่ใช่ลายเซ็นยืนยันผู้ส่ง หากใครแก้ทั้งเอกสารและ snapshot สามารถสร้างหลักฐานใหม่ได้ ไม่มีการตรวจความลับ ความจริงของสรุป ความปลอดภัยของคำสั่ง หรือสิทธิ์ดำเนินการอัตโนมัติ

เมื่อย้ายเครื่องใช้ไฟล์ไบต์เดียวกัน Git checkout ที่แปลง LF/CRLF อาจทำให้ไฟล์ถูกแจ้ง CHANGED แม้เจตนาของโค้ดเดิมเหมือนกัน ให้ตรวจและบันทึกบริบทเครื่องใหม่ก่อน seal ใหม่ การ commit หลัง seal จะทำให้ HEAD เปลี่ยนและถูกแจ้ง STALE ตามจริง
