# CHAPTER 3 — Workshop: AI Avatar พรีเซนเตอร์

dewviko | Chapter 3 — AI Avatar

---

โรงงานผลิตวิดีโอด้วย AI

dewviko

---

## สารบัญ Chapter 3

PART I — ภาพรวม: เราจะสร้างอะไรในบทนี้
PART II — Step 1: Chat Trigger + AI Agent (สร้างสคริป)
PART III — Step 2: ElevenLabs TTS (แปลงสคริปเป็นเสียง)
PART IV — Step 3: เก็บไฟล์เสียงใน Google Drive
PART V — Step 4: fal.ai สร้าง AI Avatar Video
PART VI — Step 5: Wait + เช็คสถานะ + ดาวน์โหลดวิดีโอ
PART VII — Step 6: อัปโหลดวิดีโอ + บันทึกลง Google Sheets
PART VIII — API & Credential ที่ต้องเตรียม (ทำครั้งเดียว)
PART IX — Troubleshoot + Checklist

---
---

# I

## PART 1
## ภาพรวม: เราจะสร้างอะไรในบทนี้

Chapter 1-2 เราได้ "สคริป → เสียง" กับ "รูป → วิดีโอ" ไปแล้ว

บทนี้เราจะรวมทุกอย่างเข้าด้วยกัน แล้วเพิ่มของใหม่เข้ามา คือ AI Avatar

พูดง่ายๆ คือ เราจะพิมพ์หัวข้อเข้าไปแค่บรรทัดเดียว แล้วระบบจะ:

1. AI เขียนสคริปให้อัตโนมัติ
2. แปลงสคริปเป็นเสียงพูด
3. เอาเสียง + รูปหน้าคน → สร้างวิดีโอ Avatar ที่ขยับปากพูดตามเสียง
4. เก็บวิดีโอลง Google Drive
5. บันทึก URL + สคริป + หัวข้อลง Google Sheets

ผลลัพธ์: วิดีโอ AI Avatar พร้อมลง TikTok/Reels

---

### Workflow หน้าตาเป็นแบบนี้

```
Chat Trigger → AI Agent (GPT-4o) → ElevenLabs TTS → Google Drive (เสียง)
→ fal.ai Avatar → Wait 1 นาที → เช็คสถานะ → ดาวน์โหลดวิดีโอ
→ Google Drive (วิดีโอ) → Google Sheets (บันทึก log)
```

รวม 10 Nodes — เยอะที่สุดในหนังสือเล่มนี้ แต่แต่ละ Node ทำงานง่ายๆ ตรงไปตรงมา

---

### Tools ที่ต้องเตรียม

| Tool | ใช้ทำอะไร | ค่าใช้จ่าย |
|------|----------|-----------|
| OpenAI API | AI เขียนสคริป (GPT-4o) | ~฿1-2/ครั้ง |
| ElevenLabs | แปลง text เป็นเสียงพูด | Free 10,000 chars/เดือน |
| fal.ai | สร้าง AI Avatar จากรูป+เสียง | ~$0.10-0.30/วิดีโอ |
| Google Drive | เก็บไฟล์เสียงและวิดีโอ | Free |
| Google Sheets | บันทึก log ของวิดีโอที่สร้าง | Free |

รวมค่าใช้จ่ายต่อวิดีโอ 1 ชิ้น: ประมาณ 5-15 บาท

---

### Checklist ก่อนเริ่ม

ก่อนทำ Workshop ต้องมีครบทุกข้อนี้:

☑ n8n ติดตั้งแล้ว ทำงานได้ปกติ (จาก Chapter 0)
☑ มี OpenAI API Key
☑ มี ElevenLabs API Key + Voice ID ที่ต้องการใช้
☑ มี fal.ai API Key
☑ มี Google account สำหรับ Drive + Sheets
☑ มีรูปหน้าคนที่จะใช้เป็น Avatar (อัปโหลดไว้ใน Google Drive แล้ว)

ถ้ายังไม่มี API Key ตัวไหน ไปดู PART VIII ก่อน มีวิธีสมัครทุกตัว

---
---

# II

## PART 2
## Step 1: Chat Trigger + AI Agent (สร้างสคริป)

### Node 1: When chat message received

Node นี้คือจุดเริ่มต้นของ Workflow ทั้งหมด

ทำหน้าที่: รับข้อความที่เราพิมพ์เข้ามา เช่น "อสังหาทำเลดี" แล้วส่งต่อให้ AI Agent

วิธีตั้งค่า:
1. ลาก Node "When chat message received" จากแถบซ้าย
2. เปิด Settings
3. ติ๊ก "Available in Chat" เป็น ON — เพื่อให้มีหน้า Chat ให้เราพิมพ์ข้อความได้

แค่นี้ Node นี้พร้อมใช้งาน

---

### Node 2: AI Agent

Node นี้คือ "สมอง" ของ Workflow

ทำหน้าที่: รับหัวข้อจาก Chat Trigger แล้วเขียนสคริปวิดีโอสั้นออกมา

ความพิเศษของ Node นี้คือ มันไม่ใช่แค่ส่งข้อความไป OpenAI ธรรมดา แต่เป็น AI Agent ที่มี System Prompt กำกับการทำงานอย่างละเอียด

---

### System Prompt ที่ใช้ (สำคัญมาก)

System Prompt คือ "คำสั่งลับ" ที่กำหนดว่า AI จะเขียนออกมาแบบไหน

ใน Workflow นี้ System Prompt กำหนดไว้ว่า:

**บทบาท:** เป็นนักเขียนสคริปวิดีโอสั้น TikTok/Reels ด้านอสังหาริมทรัพย์ แทนตัวเองว่า "พี่เหมียว" พูดเป็นกันเอง จริงใจ เหมือนพี่สาวมาเล่าให้ฟัง

**กฎเหล็ก:**
- ตอบกลับเฉพาะเนื้อหาสคริปที่พร้อมอ่านออกเสียง (TTS) เท่านั้น
- ห้ามมีคำทักทาย คำนำ คำอธิบายเพิ่ม หัวข้อ หรือข้อความสรุป
- ห้ามใช้ Emoji
- ห้ามใช้ Markdown เช่น ตัวหนา ตัวเอียง หัวข้อ Bullet point
- ห้ามใช้ภาษาขายของเด็ดขาด เช่น "ซื้อเลย" "ราคาดี" "น่าลงทุน"
- ใช้ ... (จุดสามจุด) เมื่อต้องการเว้นจังหวะหายใจ
- ห้ามใช้คำอังกฤษยาวๆ ให้เขียนเป็นคำอ่านไทยแทน เช่น DSR → ดีเอสอาร์

**โครงสร้างสคริป:**
1. Hook — เปิดเรื่องดึงคนหยุดดู
2. เนื้อหา — ให้ความรู้จริงๆ มีตัวเลข ขั้นตอน หรือเคล็ดลับ
3. สรุป — ย้ำ Key Takeaway 1-2 ประโยค
4. CTA — ปิดท้ายด้วย "หากอยากปรึกษาเรื่องบ้านกับพี่เหมียว ทักลิงก์หน้าโปรไฟล์ได้เลย พี่เหมียวยินดีให้คำปรึกษาฟรี"

**ความยาว:** 20-30 วินาที (ประมาณ 120-250 ตัวอักษร)

---

### ทำไม System Prompt ถึงสำคัญ

เพราะเสียงที่ได้จาก ElevenLabs จะอ่านสคริปตรงๆ ตามที่ AI เขียนออกมา

ถ้า AI ตอบมาพร้อม Emoji หรือ Markdown เสียงจะอ่านออกมาแปลกๆ

ถ้า AI เขียนยาวเกินไป วิดีโอจะยาวเกิน 30 วินาที ไม่เหมาะกับ TikTok

System Prompt จึงต้องเข้มงวดมาก เพื่อให้ AI output ออกมา "พร้อมใช้" โดยไม่ต้องแก้อะไรเลย

---

### วิธีตั้งค่า AI Agent Node

1. ลาก Node "AI Agent" มาวาง แล้วลากเส้นเชื่อมจาก Chat Trigger
2. เปิด Settings → ไปที่ Options → System Message
3. Copy System Prompt ด้านบนใส่ลงไป (หรือเขียนเวอร์ชันของตัวเองก็ได้)
4. ต่อ Sub-node "OpenAI Chat Model" เข้ากับ AI Agent
   - เลือก Model: gpt-4o (แนะนำ เขียนภาษาไทยได้ดี)
   - ใส่ Credential: OpenAI API Key ที่สร้างไว้

**จุดสำคัญ:** AI Agent ต่างจาก OpenAI Node ธรรมดาตรงที่มันรองรับ tools และ memory ได้ ถ้าอนาคตอยากเพิ่มความสามารถ เช่น ให้ AI ค้นข้อมูลก่อนเขียน ใช้ Node นี้ต่อยอดได้เลย

---
---

# III

## PART 3
## Step 2: ElevenLabs TTS (แปลงสคริปเป็นเสียง)

### Node 3: สร้างเสียงด้วย ElevenLabs

ทำหน้าที่: รับ text สคริปจาก AI Agent แล้วแปลงเป็นไฟล์เสียง (audio)

Node นี้ใช้ HTTP Request ยิง API ตรงไปที่ ElevenLabs

---

### วิธีตั้งค่า

1. ลาก Node "HTTP Request" มาวาง
2. ตั้งค่าตามนี้:

**Method:** POST

**URL:**
```
https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}
```
เปลี่ยน {VOICE_ID} เป็น Voice ID ของเสียงที่เลือก

ใน Workflow นี้ใช้ Voice ID: `U3dExJoUNcmTY5H6GMuG`

วิธีหา Voice ID: เข้า elevenlabs.io → Voices → เลือก voice → กด Copy Voice ID

**Authentication:**
- เลือก Generic Credential Type → Header Auth
- ตั้ง Credential: ใส่ Header Name เป็น `xi-api-key` และ Value เป็น ElevenLabs API Key ของคุณ

**Headers:**
- เพิ่ม Header: `Content-Type` = `application/json`

**Body (JSON):**
```json
{
  "text": "{{ $json.output }}.",
  "model_id": "eleven_v3",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.75
  }
}
```

---

### อธิบาย Body ทีละตัว

- `text`: เอา output จาก AI Agent มาใส่ — นี่คือสคริปที่ AI เขียน คำว่า `{{ $json.output }}` คือ expression ของ n8n ที่ดึงค่าจาก Node ก่อนหน้า
- `model_id`: `eleven_v3` คือโมเดลเสียงเวอร์ชันล่าสุดของ ElevenLabs รองรับภาษาไทยได้ดี
- `stability`: 0.5 = ความเสถียรของเสียง ค่ายิ่งสูง เสียงยิ่งนิ่งแต่อาจจะดูไม่เป็นธรรมชาติ ค่า 0.5 คือจุดกลางที่ดี
- `similarity_boost`: 0.75 = ความใกล้เคียงกับ voice ต้นแบบ ค่ายิ่งสูง เสียงยิ่งเหมือนต้นแบบ

**สำหรับมือใหม่:** ค่าเหล่านี้ใช้ค่าเดิมตาม Workflow ได้เลย ไม่ต้องเปลี่ยน ถ้าอยากปรับให้ลองทีละนิด แล้วฟังเทียบกัน

---

### Output ที่ได้

Node นี้จะ return กลับมาเป็นไฟล์ binary (ไฟล์เสียง) ไม่ใช่ text

n8n จะเก็บไฟล์นี้ไว้ใน memory ชั่วคราว พร้อมส่งต่อให้ Node ถัดไป

---
---

# IV

## PART 4
## Step 3: เก็บไฟล์เสียงใน Google Drive

### Node 4: เก็บไฟล์เสียงใน Drive

ทำหน้าที่: เอาไฟล์เสียงที่ได้จาก ElevenLabs อัปโหลดไปเก็บใน Google Drive

ทำไมต้องเก็บใน Drive ก่อน? เพราะ fal.ai (ตัวสร้าง Avatar) ต้องการ URL ของไฟล์เสียง ไม่สามารถรับไฟล์ binary ตรงๆ ได้ พอเก็บใน Drive แล้ว เราจะได้ URL ที่ fal.ai เข้าถึงได้

---

### วิธีตั้งค่า

1. ลาก Node "Google Drive" มาวาง
2. ตั้งค่า:
   - Operation: Upload File (ค่า default)
   - Drive: เลือก Shared Drive หรือ My Drive
   - Folder: เลือก folder ที่ต้องการเก็บไฟล์
3. Credential: เชื่อม Google Drive OAuth2

**วิธีสร้าง Google Drive Credential:**
1. ไปที่ n8n → Settings → Credentials → Add Credential
2. เลือก Google Drive OAuth2 API
3. ทำตาม flow login Google ที่ขึ้นมา (ต้อง Allow access)
4. กด Save

**จุดสำคัญ:** ต้องตั้ง sharing ของ folder ใน Drive ให้เป็น "Anyone with the link can view" เพราะ fal.ai จะต้องเข้าถึงไฟล์เสียงได้ผ่าน URL

---

### Output ที่ได้

Node นี้จะ return ข้อมูลไฟล์ที่อัปโหลดสำเร็จ รวมถึง `webContentLink` ซึ่งเป็น URL สำหรับดาวน์โหลดไฟล์โดยตรง — URL นี้จะถูกใช้ใน Step ถัดไป

---
---

# V

## PART 5
## Step 4: fal.ai สร้าง AI Avatar Video

### Node 5: สร้าง Video Avatar

นี่คือ Node ที่น่าตื่นเต้นที่สุดใน Workflow

ทำหน้าที่: เอารูปหน้าคน + ไฟล์เสียง → สร้างวิดีโอที่คนในรูปขยับปากพูดตามเสียง

ใช้ fal.ai เป็นตัวสร้าง ใช้โมเดล LTX 2.0 19B (audio-to-video)

---

### วิธีตั้งค่า

1. ลาก Node "HTTP Request" มาวาง
2. ตั้งค่าตามนี้:

**Method:** POST

**URL:**
```
https://queue.fal.run/fal-ai/ltx-2-19b/distilled/audio-to-video
```

**Authentication:**
- Generic Credential Type → Header Auth
- Header Name: `Authorization`
- Header Value: `Key {FAL_API_KEY}` (เปลี่ยน {FAL_API_KEY} เป็น key ของคุณ)

**Body (JSON):**
```json
{
  "prompt": "A professional woman speaking naturally to the camera, subtle head and lip movement, high quality, natural lighting",
  "image_url": "https://drive.google.com/uc?export=download&id={IMAGE_FILE_ID}",
  "audio_url": "{{ $json.webContentLink }}",
  "video_size": {
    "width": 576,
    "height": 1024
  },
  "match_audio_length": true
}
```

---

### อธิบาย Body ทีละตัว

- `prompt`: คำอธิบายวิดีโอที่ต้องการ — บอก AI ว่าอยากได้ท่าทางแบบไหน ใช้ภาษาอังกฤษ ไม่ต้องยาว แค่บอกว่า "ผู้หญิงมืออาชีพพูดกับกล้อง ขยับหัวและปากเป็นธรรมชาติ"
- `image_url`: URL ของรูปหน้าคนที่จะใช้เป็น Avatar — ต้องอัปโหลดรูปไว้ใน Google Drive ก่อน แล้วเอา File ID มาใส่ (วิธีหา File ID: คลิกขวาที่ไฟล์ → Get link → ID คือส่วนที่อยู่ระหว่าง /d/ กับ /view)
- `audio_url`: URL ของไฟล์เสียง — ดึงมาจาก Google Drive Node ก่อนหน้าด้วย expression `{{ $json.webContentLink }}`
- `video_size`: ขนาดวิดีโอ 576x1024 คือแนวตั้ง (portrait) สำหรับ TikTok/Reels
- `match_audio_length`: true = ให้วิดีโอยาวเท่ากับเสียง ไม่ต้องกำหนดความยาวเอง

---

### เรื่องรูป Avatar ที่ต้องรู้

รูปที่ใช้เป็น Avatar ควรเป็น:
- รูปหน้าตรง มองกล้อง
- พื้นหลังสะอาด ไม่รกเกินไป
- ความละเอียดอย่างน้อย 576x1024 pixels
- เห็นหน้าชัด ไม่มีอะไรบังปาก

รูปนี้จะใช้ซ้ำได้ทุกวิดีโอ อัปโหลดครั้งเดียว ใช้ได้ตลอด

---

### Output ที่ได้

เพราะ fal.ai ใช้ระบบ Queue (คิว) — Node นี้จะไม่ return วิดีโอกลับมาทันที

สิ่งที่ได้คือ `response_url` ซึ่งเป็น URL สำหรับเช็คสถานะว่าวิดีโอสร้างเสร็จหรือยัง

เราจึงต้องมี Node ถัดไปเพื่อ "รอ" แล้ว "เช็คสถานะ"

---
---

# VI

## PART 6
## Step 5: Wait + เช็คสถานะ + ดาวน์โหลดวิดีโอ

ส่วนนี้มี 3 Nodes ทำงานต่อกัน เข้าใจง่ายมาก

---

### Node 6: รอสร้างวิดีโอ 1 นาที

ทำหน้าที่: หยุดรอ 1 นาที ให้ fal.ai มีเวลาสร้างวิดีโอ

วิธีตั้งค่า:
1. ลาก Node "Wait" มาวาง
2. ตั้ง Resume: After Time Interval
3. ตั้ง Amount: 1
4. ตั้ง Unit: Minutes

ทำไมต้องรอ? เพราะ fal.ai สร้างวิดีโอใช้เวลาประมาณ 30 วินาที ถึง 2 นาที ขึ้นอยู่กับความยาวเสียง การรอ 1 นาทีคือค่าที่เหมาะสมสำหรับวิดีโอ 20-30 วินาที

**เทคนิค:** ถ้าสคริปยาว (เกิน 30 วินาที) อาจต้องเพิ่มเวลารอเป็น 2 นาที

---

### Node 7: เช็คสถานะวิดีโอ

ทำหน้าที่: ถาม fal.ai ว่าวิดีโอเสร็จหรือยัง ถ้าเสร็จแล้วจะได้ URL วิดีโอกลับมา

วิธีตั้งค่า:
1. ลาก Node "HTTP Request" มาวาง
2. ตั้งค่า:
   - Method: GET (ค่า default)
   - URL: `={{ $('สร้าง Video Avatar').first().json.response_url }}`
   - Authentication: เหมือน Node สร้าง Avatar (Header Auth ของ fal.ai)

**อธิบาย URL:**
expression `$('สร้าง Video Avatar').first().json.response_url` คือการ "ย้อนกลับไปดึงค่าจาก Node ชื่อ สร้าง Video Avatar" — เพราะ response_url ได้มาจาก Node นั้น ไม่ใช่จาก Node Wait

นี่เป็นเทคนิคสำคัญใน n8n: เราสามารถดึงข้อมูลจาก Node ไหนก็ได้ใน Workflow ไม่จำเป็นต้องเป็น Node ก่อนหน้าโดยตรง

---

### Node 8: ดาวน์โหลดวิดีโอ

ทำหน้าที่: โหลดไฟล์วิดีโอจาก URL ที่ fal.ai ให้มา เก็บเป็นไฟล์ binary ใน n8n

วิธีตั้งค่า:
1. ลาก Node "HTTP Request" มาวาง
2. ตั้งค่า:
   - Method: GET
   - URL: `={{ $json.video.url }}` (URL ของวิดีโอที่ fal.ai สร้างเสร็จ)
   - Options → Response → Response Format: File
   - Output Property Name: `avatarVideo`

**จุดสำคัญ:** ต้องตั้ง Response Format เป็น "File" ไม่งั้น n8n จะพยายามอ่านเป็น text แล้ว error

---
---

# VII

## PART 7
## Step 6: อัปโหลดวิดีโอ + บันทึกลง Google Sheets

### Node 9: อัปโหลดวิดีโอไป Drive

ทำหน้าที่: เอาไฟล์วิดีโอที่โหลดมา อัปโหลดไปเก็บใน Google Drive

วิธีตั้งค่า:
1. ลาก Node "Google Drive" มาวาง
2. ตั้งค่า:
   - Operation: Upload File
   - Input Data Field Name: `avatarVideo` (ชื่อตรงกับที่ตั้งใน Node ดาวน์โหลด)
   - File Name: `Avatar_VDO.mp4`
   - Drive: My Drive
   - Folder: เลือก folder ที่ต้องการ
3. Credential: ใช้ Google Drive OAuth2 ตัวเดิม

**เทคนิค:** ถ้าอยากให้ชื่อไฟล์ไม่ซ้ำกัน สามารถเพิ่ม expression ได้ เช่น `Avatar_{{ $now.format('yyyyMMdd_HHmmss') }}.mp4` จะได้ชื่อไฟล์ตามวันเวลาที่สร้าง

---

### Node 10: บันทึกลง Google Sheets

ทำหน้าที่: บันทึกข้อมูลของวิดีโอที่สร้างไว้ใน Google Sheets เพื่อเป็น log

วิธีตั้งค่า:
1. ลาก Node "Google Sheets" มาวาง
2. ตั้งค่า:
   - Operation: Append Row
   - Document: เลือก Google Sheets ที่เตรียมไว้
   - Sheet: Sheet1
3. Credential: สร้าง Google Sheets OAuth2 (ทำเหมือน Google Drive)

**Columns ที่ต้องเตรียมใน Sheets:**

| Column | ข้อมูลที่บันทึก | Expression ใน n8n |
|--------|----------------|-------------------|
| Video URL | ลิงก์วิดีโอ | `{{ $('อัปโหลดวิดีโอไป Drive').item.json.webContentLink }}` |
| Title | หัวข้อที่พิมพ์เข้ามา | `{{ $('When chat message received').item.json.chatInput }}` |
| Description | สคริปที่ AI เขียน | `{{ $('AI Agent').item.json.output }}` |

**วิธีเตรียม Google Sheets:**
1. สร้าง Google Sheets ใหม่
2. แถวแรก (Row 1) ใส่หัวตาราง: Video URL, Title, Description
3. Copy URL ของ Sheets มาใส่ใน Node

**จุดสำคัญ:** ชื่อ Column ใน Sheets ต้องตรงกับชื่อที่ตั้งใน n8n เป๊ะๆ ถ้าสะกดผิดแม้แต่เว้นวรรค จะ error

---
---

# VIII

## PART 8
## API & Credential ที่ต้องเตรียม (ทำครั้งเดียว)

### 1. OpenAI API Key

1. ไปที่ platform.openai.com → สมัครสมาชิก
2. ไปที่ API Keys → Create new secret key
3. Copy key เก็บไว้ (จะเห็นแค่ครั้งเดียว)
4. เติมเงินขั้นต่ำ $5

ใน n8n: Settings → Credentials → Add Credential → OpenAI API → ใส่ key → Save

---

### 2. ElevenLabs API Key

1. ไปที่ elevenlabs.io → สมัครสมาชิก (Free tier ได้)
2. ไปที่ Profile → API Key → Copy
3. ไปที่ Voices → เลือก voice → Copy Voice ID

ใน n8n: ใช้ Header Auth Credential
- Header Name: `xi-api-key`
- Header Value: (ใส่ API Key ของคุณ)

---

### 3. fal.ai API Key

1. ไปที่ fal.ai → สมัครสมาชิก
2. ไปที่ Dashboard → Keys → Create Key
3. Copy key เก็บไว้
4. เติมเงินขั้นต่ำ $5 (pay-as-you-go)

ใน n8n: ใช้ Header Auth Credential
- Header Name: `Authorization`
- Header Value: `Key {ใส่ API Key ของคุณ}`

**สำคัญ:** ต้องมีคำว่า "Key " (มีเว้นวรรค) นำหน้า API Key ด้วย

---

### 4. Google Drive & Sheets OAuth2

1. ไปที่ n8n → Settings → Credentials → Add Credential
2. เลือก Google Drive OAuth2 API
3. กด Sign in with Google → เลือกบัญชี → Allow
4. กด Save

ทำเหมือนกันสำหรับ Google Sheets OAuth2 API

**เทคนิค:** ถ้าใช้ Google account เดียวกัน ตั้ง Credential แยกกัน 2 ตัว (Drive กับ Sheets) จะจัดการง่ายกว่า

---
---

# IX

## PART 9
## Troubleshoot + Checklist

### ปัญหาที่เจอบ่อย

**1. ElevenLabs error 401 (Unauthorized)**
- สาเหตุ: API Key ผิด หรือ Header Name สะกดผิด
- แก้: เช็คว่า Header Name เป็น `xi-api-key` (ตัวเล็กทั้งหมด)

**2. fal.ai error 401**
- สาเหตุ: API Key ผิด หรือลืมใส่ "Key " นำหน้า
- แก้: ต้องเป็น `Key sk-fal-xxxxx` ไม่ใช่แค่ `sk-fal-xxxxx`

**3. วิดีโอยังสร้างไม่เสร็จ (เช็คสถานะได้ "IN_QUEUE" หรือ "IN_PROGRESS")**
- สาเหตุ: เวลารอไม่พอ
- แก้: เพิ่มเวลา Wait เป็น 2-3 นาที หรือเพิ่ม loop เช็คสถานะซ้ำ

**4. Google Drive error "File not found"**
- สาเหตุ: folder ID ผิด หรือยังไม่ได้ give access
- แก้: เช็ค folder URL ใน Node ว่าถูกต้อง และ sharing เปิดอยู่

**5. Google Sheets error "Column not found"**
- สาเหตุ: ชื่อ Column ไม่ตรงกัน
- แก้: เช็คชื่อ Column ใน Sheets กับใน n8n ต้องตรงเป๊ะ รวมถึงเว้นวรรค

**6. AI Agent เขียนสคริปยาวเกินไป**
- สาเหตุ: System Prompt ไม่ได้กำหนดความยาวชัดเจน
- แก้: เพิ่มบรรทัด "ความยาวต้องไม่เกิน 250 ตัวอักษร" ใน System Prompt

---

### Checklist สุดท้ายก่อนกด Test Workflow

☑ Chat Trigger → ติ๊ก Available in Chat แล้ว
☑ AI Agent → ใส่ System Prompt แล้ว + ต่อ OpenAI Chat Model แล้ว
☑ OpenAI → เลือก Model (gpt-4o) + ใส่ Credential แล้ว
☑ ElevenLabs → URL มี Voice ID ถูกต้อง + Header Auth ถูกต้อง
☑ Google Drive (เสียง) → เลือก folder แล้ว + Credential ใช้ได้
☑ fal.ai → URL ถูกต้อง + image_url ถูกต้อง + Header Auth ถูกต้อง
☑ Wait → ตั้ง 1 นาที
☑ เช็คสถานะ → URL ดึงจาก Node "สร้าง Video Avatar" ถูกต้อง
☑ ดาวน์โหลด → Response Format เป็น File + Output Name เป็น avatarVideo
☑ Google Drive (วิดีโอ) → Input Field Name เป็น avatarVideo + เลือก folder แล้ว
☑ Google Sheets → สร้าง Sheet พร้อม 3 Columns แล้ว + Credential ใช้ได้
☑ Google Drive folder → sharing เปิดเป็น "Anyone with the link"

---

### วิธีทดสอบ

1. กด "Test Workflow" (ปุ่มด้านบน)
2. จะมี Chat popup ขึ้นมา
3. พิมพ์หัวข้อ เช่น "อสังหาทำเลดี"
4. รอสักครู่ ดูว่า Node แต่ละตัวทำงานผ่านไหม (เขียวคือผ่าน แดงคือ error)
5. ถ้าผ่านทุก Node: เข้า Google Drive เช็คว่ามีไฟล์เสียงและวิดีโอ แล้วเข้า Google Sheets เช็คว่ามี row ใหม่

ถ้า Node ไหน error ให้คลิกที่ Node นั้น → ดู error message → เทียบกับ Troubleshoot ด้านบน

---

### สรุป Workflow ทั้งหมด

```
[พิมพ์หัวข้อ] → [AI เขียนสคริป] → [แปลงเป็นเสียง] → [เก็บเสียงใน Drive]
    → [สร้าง Avatar Video] → [รอ 1 นาที] → [เช็คสถานะ]
    → [โหลดวิดีโอ] → [เก็บวิดีโอใน Drive] → [บันทึก log ใน Sheets]
```

Input: หัวข้อ 1 บรรทัด
Output: วิดีโอ AI Avatar + สคริป + log ทั้งหมดเก็บไว้เรียบร้อย

เวลาทั้งหมด: ประมาณ 2-3 นาทีต่อวิดีโอ 1 ชิ้น
ค่าใช้จ่าย: ประมาณ 5-15 บาทต่อวิดีโอ

---

### ไอเดียต่อยอด

- เปลี่ยน System Prompt ให้เป็นธีมอื่น เช่น รีวิวอาหาร รีวิวสินค้า ให้ความรู้การเงิน
- เปลี่ยนรูป Avatar เป็นหน้าตัวเอง หรือตัวละครที่สร้างจาก AI
- เพิ่ม Node ตัดต่อวิดีโอ เช่น ใส่ subtitle หรือเพลงประกอบ
- สร้างแบบ batch: ป้อนหัวข้อ 10 อัน ให้สร้างวิดีโอ 10 ตัวอัตโนมัติ
