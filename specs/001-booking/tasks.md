# Tasks: จองคิวตรวจสุขภาพ (Booking)
- Feature: จองคิวตรวจสุขภาพ (Booking)
- Spec ID: SPEC-BKG-001
- อ้างอิง plan.md: `specs/001-booking/plan.md`
- วันที่: 2569-09-23

## สรุป
- รวม task: 12 task
- รอ Open Question: 1 task (T-12) โดยยังติดกับ Q-02

## รายการ task

### T-01 สร้างฐานข้อมูลและ migration หลัก
- รองรับ: CON-TECH-01, DOM-PDPA-01, IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-01
- ไฟล์ที่แตะ: `backend/app/db/models.py`, `backend/app/db/session.py`, `backend/app/db/migrations/001_init.py`
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: migration สร้างตาราง `slots`, `bookings`, `audit_logs` ใน PostgreSQL พร้อมเก็บ `hn` และไม่เก็บเลขบัตรประชาชน
- สถานะ: พร้อมทำ

### T-02 สร้าง API ค้นหาช่วงเวลาว่าง
- รองรับ: FR-BKG-01, FR-BKG-06, NFR-PERF-01
- ตรวจด้วย: AC-BKG-05
- ไฟล์ที่แตะ: `backend/app/slots/router.py`, `backend/app/slots/service.py`, `backend/tests/test_slots.py`
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: `GET /slots` คืนรายการช่วงเวลาและจำนวนที่นั่งคงเหลือภายใน 30 วัน ตามแพ็กเกจที่เลือก และผ่านเกณฑ์ p95 ภายใต้ 2 วินาทีเมื่อจำลอง 200 ผู้ใช้พร้อมกัน
- สถานะ: พร้อมทำ

### T-03 สร้างการจองพื้นฐานและบันทึกผล
- รองรับ: FR-BKG-04, IF-IDP-01, AC-BKG-01
- ตรวจด้วย: AC-BKG-01
- ไฟล์ที่แตะ: `backend/app/booking/router.py`, `backend/app/booking/service.py`, `backend/app/auth/idp.py`, `backend/tests/test_booking_create.py`
- ต้องทำหลัง: T-01, T-02
- เสร็จเมื่อ: ผู้ใช้ที่ยืนยันตัวตนแล้วสามารถยืนยันการจองได้สำเร็จ บันทึก `booking` และลด `remaining` เป็น 0 พร้อมคืนหมายเลขคิวให้กับผู้ใช้
- สถานะ: พร้อมทำ

### T-04 ป้องกันการจองซ้ำในวันเดียวกัน
- รองรับ: FR-BKG-02
- ตรวจด้วย: AC-BKG-02
- ไฟล์ที่แตะ: `backend/app/booking/service.py`, `backend/tests/test_booking_duplicate.py`
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: ถ้ามีคิวที่ยังไม่ได้ใช้ในวันเดียวกัน ระบบปฏิเสธการจองใหม่และคืนหมายเลขคิวเดิมที่เคยจองไว้
- สถานะ: พร้อมทำ

### T-05 เสนอ 3 ช่วงที่ว่างเมื่อช่วงเวลาที่เลือกเต็ม
- รองรับ: FR-BKG-03, AC-BKG-03
- ตรวจด้วย: AC-BKG-03
- ไฟล์ที่แตะ: `backend/app/slots/service.py`, `backend/app/booking/service.py`, `backend/tests/test_booking_alternatives.py`
- ต้องทำหลัง: T-03, T-04
- เสร็จเมื่อ: ระบบส่งคืน HTTP 409 พร้อมข้อความ “ช่วงเวลาเต็ม” และ 3 ช่วงเวลาที่ยังว่างที่ใกล้ที่สุดภายในวันเดียวกันและวันถัดไป โดยไม่สร้างการจองซ้อน
- สถานะ: พร้อมทำ

### T-06 จัดการคิวส่งข้อความยืนยันแบบ asynchronous และ retry
- รองรับ: FR-BKG-05, IF-NOT-01, NFR-REL-02
- ตรวจด้วย: AC-BKG-04
- ไฟล์ที่แตะ: `backend/app/notify/queue.py`, `backend/app/booking/service.py`, `backend/tests/test_notify_retry.py`
- ต้องทำหลัง: T-03, T-05
- เสร็จเมื่อ: การจองยังถูกบันทึกแม้ส่งข้อความยืนยันไม่สำเร็จ และมีงานค้างส่งอยู่ในคิวที่ต้องส่งซ้ำภายใน 5 นาที
- สถานะ: พร้อมทำ

### T-07 บันทึก audit log ทุกครั้งที่เข้าถึงข้อมูลการจอง
- รองรับ: DOM-PDPA-01
- ตรวจด้วย: AC-BKG-06
- ไฟล์ที่แตะ: `backend/app/audit/middleware.py`, `backend/app/booking/router.py`, `backend/tests/test_audit_log.py`
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: ทุกครั้งที่เรียกดูข้อมูลการจองมี audit log ที่บันทึก `actor_id`, `hn`, `accessed_at` และยังไม่เก็บเลขบัตรประชาชนใน log
- สถานะ: พร้อมทำ

### T-08 ค้น HN จาก HIS และจำกัดข้อมูลที่เก็บในระบบ
- รองรับ: IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-08
- ไฟล์ที่แตะ: `backend/app/his/client.py`, `backend/app/booking/service.py`, `backend/tests/test_his_lookup.py`
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: ระบบสามารถ lookup ผู้รับบริการจาก HIS ด้วยเลขบัตรประชาชนได้ และบันทึกเฉพาะ HN ในตารางการจองเท่านั้น
- สถานะ: พร้อมทำ

### T-09 สร้างหน้าเลือกแพ็กเกจและช่วงเวลา (mock API)
- รองรับ: FR-BKG-01, FR-BKG-06
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-09
- ไฟล์ที่แตะ: `frontend/src/pages/SlotPicker.jsx`, `frontend/src/App.jsx`, `frontend/src/api/client.js`
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: ผู้ใช้สามารถเลือกแพ็กเกจ และเห็นรายการช่วงเวลาว่างพร้อมจำนวนที่นั่งคงเหลือจาก API จำลอง ตามสัญญาใน plan.md
- สถานะ: พร้อมทำ

### T-10 สร้างหน้้ายืนยันและแสดงตัวเลือกช่วงเวลาเต็ม
- รองรับ: FR-BKG-03, AC-BKG-03
- ตรวจด้วย: AC-BKG-03
- ไฟล์ที่แตะ: `frontend/src/pages/ConfirmBooking.jsx`, `frontend/src/__tests__/AC-BKG-03.test.jsx`
- ต้องทำหลัง: T-09
- เสร็จเมื่อ: เมื่อ API จำลองตอบ 409 หน้าจอแสดง “ช่วงเวลาเต็ม” พร้อม 3 ตัวเลือกที่ใกล้เวลาที่เลือกที่สุด และยังคงไม่มีการสร้างการจองซ้อนบน UI
- สถานะ: พร้อมทำ

### T-11 ต่อหน้าจอกับ API จริงและเชื่อมการจอง
- รองรับ: FR-BKG-01, FR-BKG-03, FR-BKG-04
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-11
- ไฟล์ที่แตะ: `frontend/src/pages/SlotPicker.jsx`, `frontend/src/pages/ConfirmBooking.jsx`, `frontend/src/pages/BookingResult.jsx`, `frontend/src/api/client.js`
- ต้องทำหลัง: T-02, T-05, T-09, T-10
- เสร็จเมื่อ: หน้าเลือกเวลาและหน้าจอยืนยันใช้งานต่อกับ API จริง และแสดงผลการจองได้ตามสัญญา API ที่กำหนดใน plan.md
- สถานะ: พร้อมทำ

### T-12 เตรียมงานออกหมายเลขคิวหลังได้รับคำตอบ Q-02
- รองรับ: FR-BKG-04, AC-BKG-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-12
- ไฟล์ที่แตะ: `backend/app/booking/service.py`, `backend/app/db/models.py`, `frontend/src/pages/BookingResult.jsx`
- ต้องทำหลัง: T-03, T-06
- เสร็จเมื่อ: ได้คำตอบจาก Q-02 แล้วจึงกำหนดรูปแบบเลขคิวให้ตรงกับนโยบายของโรงพยาบาล และแสดงเลขคิวอย่างถูกต้องบนหน้าจอ
- สถานะ: รอ Q-02

## ตารางตรวจความครบ

### 1) AC ID | task ที่ตรวจ AC นี้
| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-BKG-01 | T-03 |
| AC-BKG-02 | T-04 |
| AC-BKG-03 | T-05, T-10 |
| AC-BKG-04 | T-06 |
| AC-BKG-05 | T-02 |
| AC-BKG-06 | T-07 |

### 2) Constraint ID | task ที่ทำให้เป็นจริง
| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| CON-TECH-01 | T-01 |
| DOM-PDPA-01 | T-01, T-07 |
| IF-IDP-01 | T-03 |
| IF-HIS-01 | T-08 |
| IF-NOT-01 | T-06 |

## สิ่งที่ยังไม่ทำ
- Q-02: หมายเลขคิวรีเซ็ตรายวัน หรือนับต่อเนื่อง และมีรูปแบบอย่างไร (เช่น A001)? -> ถามเจ้าหน้าที่เวชระเบียน; task ที่รออยู่: T-12

