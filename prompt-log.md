# Prompt log

บันทึกทุกครั้งที่ใช้ AI กับ repo นี้ เขียนต่อท้ายเรื่อย ๆ ไม่ต้องลบของเก่า

---

## 2569-09-16 คำสั่ง: /plan

- เครื่องมือ: GitHub Copilot ใน VS Code
- ไฟล์: `specs/001-booking/spec.md`, `specs/001-booking/plan.md`
- ผลลัพธ์: สร้าง `specs/001-booking/plan.md` ตามโครงสร้างของ prompt `/plan`
- Constraint ที่ AI ยังไม่ได้ใช้: ไม่มี Constraint ที่ถูกข้าม แต่พฤติกรรมเมื่อระบบภายนอกไม่ตอบสนองยังรอคำตอบจากทีมตาม `IF-IDP-01`, `IF-HIS-01` และ `IF-NOT-01`
- สิ่งที่ AI บอกว่าอยากเดาแต่ไม่ได้เดา: ขอบเขตช่วงเวลาใกล้เคียง (`Q-01`), รูปแบบหมายเลขคิว (`Q-02`), สถานะคิวที่ยังไม่ได้ใช้, พฤติกรรมระบบภายนอกไม่พร้อมใช้งาน, นโยบาย retry และการป้องกันการยืนยันพร้อมกัน

---

## 2569-09-16 คำสั่ง: คำตอบจากทีมต่อ /clarify

- เครื่องมือ: GitHub Copilot ใน VS Code
- ไฟล์: `specs/001-booking/spec.md`, `specs/001-booking/plan.md`
- คำถามที่ AI ถาม: Q1. "ช่วงเวลาใกล้เคียง" นับเฉพาะวันเดียวกัน หรือรวมวันถัดไปด้วย?; Q2. หมายเลขคิวรีเซ็ตทุกวัน หรือนับต่อเนื่อง?
- คำตอบของทีม: Q1 ส่งกลับเป็นคำถามเดิม จึงยังไม่มีคำตอบ; Q2 หมายเลขคิวรีเซ็ตทุกวัน
- สิ่งที่แก้ใน `spec.md`: เปลี่ยนสถานะเป็น `Draft v2` และวันที่เป็น `2569-09-16`; เพิ่ม `ASM-03` ว่าหมายเลขคิวรีเซ็ตทุกวัน; คง `Q-01` ไว้เพราะยังไม่ได้รับคำตอบ; ลบ `Q-02` หลังทีมตอบแล้ว
- สิ่งที่แก้ใน `plan.md`: เปลี่ยนการอ้างอิงกติกาหมายเลขคิวจาก `Q-02` เป็น `ASM-03` และนำ `Q-02` ออกจากรายการงานค้าง

---

## 2569-09-23 คำสั่ง: /tasks

- เครื่องมือ: GitHub Copilot ใน VS Code
- ไฟล์: `specs/001-booking/spec.md`, `specs/001-booking/plan.md`
- ผลลัพธ์: สร้าง `specs/001-booking/tasks.md` ตามรูปแบบ task decomposition ที่ต้องระบุ dependency, AC mapping, constraint mapping และ Open Question blocker
- จำนวน task: 12 task
- task ที่รอ Q-02: 1 task (`T-12`)
- สิ่งที่ AI ให้ความสำคัญ: ระบุให้ทุก AC มี task ตรวจสอบอย่างน้อย 1 ตัว, ขณะเดียวกันเก็บ Q-02 เป็น blocker เพื่อหลีกเลี่ยงการเดาแบบผิดกฎ
- บันทึกเพิ่มเติม: สถานะ spec เป็น Draft v2 และมี Open Question ที่ยังไม่ได้ตอบ (`Q-02`) จึงติดสถานะ `รอ Q-02` ใน task ที่เกี่ยวข้องกับหมายเลขคิว

---

## 2569-09-23 คำสั่ง: /implement T-01

- เครื่องมือ: GitHub Copilot ใน VS Code
- ไฟล์ที่สร้าง/แก้: `backend/app/db/models.py`, `backend/app/db/session.py`, `backend/app/db/migrations/001_init.py`, `backend/tests/test_T_01_db_schema.py`
- ผล test: `cd backend && pytest tests/test_T_01_db_schema.py -q` (รันหลังแก้ import ที่ทำให้ test ไม่ collect ได้) -> ผลลัพธ์ผ่าน
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ไม่มี; ไฟล์ package init ที่จำเป็นสำหรับ import ถูกจัดการตามความจำเป็นของ Python package เพื่อให้ test โหลด module ได้
