# CHAPTER 2 — Workshop ผลิตวิดีโอด้วย AI (ง่าย → กลาง)

dewviko | Chapter 2 — Workshop พื้นฐาน

---

โรงงานผลิตวิดีโอด้วย AI

dewviko

---

## สารบัญ Chapter 2

PART I — ภาพรวม: เราจะสร้างอะไรในบทนี้
PART II — Workshop 1: สคริป → เสียง (Script to Voice)
PART III — Workshop 2: รูปสินค้า → วิดีโอ (Image to VDO)
PART IV — เปรียบเทียบ 2 Workshops + รวมร่างเป็น pipeline
PART V — Checklist ก่อนไป Chapter 3

---
---

# I

## PART 1
## ภาพรวม: เราจะสร้างอะไรในบทนี้

ถ้าคุณอ่าน Chapter 0 มาแล้ว ตอนนี้คุณรู้จัก n8n พอสมควร

รู้ว่า Node คืออะไร Link คืออะไร API คืออะไร Workflow คืออะไร

แต่รู้แค่ concept ยังไม่พอ

บทนี้เราจะ "ลงมือทำจริง" กัน

---

### เราจะสร้าง 2 Workflows

ทั้ง 2 ตัวนี้คือพื้นฐานของโรงงานผลิตวิดีโอทั้งหมด

ถ้าเข้าใจ 2 ตัวนี้ Chapter 3 จะต่อยอดได้เลย

---

**Workshop 1: Script → Voice (ง่าย)**

ป้อนชื่อสินค้า → AI เขียนสคริป → แปลงเป็นเสียงพูด → ได้ไฟล์ MP3

```
Manual Trigger → OpenAI → ElevenLabs TTS → บันทึกไฟล์ MP3
    (4 Nodes)
```

ผลลัพธ์: ไฟล์เสียง MP3 พร้อมใช้

---

**Workshop 2: Image → VDO (กลาง)**

ป้อนรูปสินค้า → AI เขียน caption → แปลงรูปเป็นวิดีโอ → ได้คลิปสั้น

```
Manual Trigger → OpenAI → Runway → รอ Render → ดาวน์โหลด
    (5 Nodes)
```

ผลลัพธ์: วิดีโอสั้น 5 วินาที พร้อมลง TikTok/Reels

---

### Tools ที่ต้องเตรียม

| Tool | ใช้ทำอะไร | ค่าใช้จ่าย |
|------|----------|-----------|
| OpenAI API | AI เขียนสคริป/caption | ~฿0.5/ครั้ง (gpt-4o-mini) |
| ElevenLabs | แปลง text เป็นเสียงพูด | Free 10,000 chars/เดือน |
| Runway | แปลงรูปเป็นวิดีโอ | ~$0.25/วิดีโอ 5 วิ |

รวมค่าใช้จ่ายต่อคอนเทนต์ 1 ชุด: **ไม่ถึง 10 บาท**

---

### Checklist ก่อนเริ่ม

ก่อนทำ Workshop ต้องมีครบทุกข้อนี้:

☑ n8n ติดตั้งแล้ว ทำงานได้ปกติ (จาก Chapter 0)
☑ มี OpenAI API Key (สมัครที่ platform.openai.com)
☑ มี ElevenLabs API Key (สมัครที่ elevenlabs.io)
☑ มี Runway API Key (สมัครที่ runwayml.com)
☑ สร้าง Credential ใน n8n เรียบร้อย (Header Auth)

ถ้ายังไม่มี API Key ตัวไหน อย่าเพิ่งข้ามไป ต้องมีก่อน ไม่งั้น workflow จะ error

---

### วิธีสมัคร API Key (ทำครั้งเดียว)

**OpenAI:**
1. ไปที่ platform.openai.com → สมัครสมาชิก
2. ไปที่ API Keys → Create new secret key
3. Copy key เก็บไว้ (จะเห็นแค่ครั้งเดียว!)
4. เติมเงินขั้นต่ำ $5

**ElevenLabs:**
1. ไปที่ elevenlabs.io → สมัครสมาชิก (Free tier ได้)
2. ไปที่ Profile → API Key → Copy
3. ไปที่ Voices → เลือก voice ที่ชอบ → Copy Voice ID

**Runway:**
1. ไปที่ runwayml.com → สมัครสมาชิก
2. ไปที่ Settings → API Keys → Create Key
3. Copy key เก็บไว้
4. Free trial ได้ credits มาทดลอง

---

### วิธีสร้าง Credential ใน n8n

ทุก API Key ต้อง "บันทึก" ใน n8n ก่อนใช้

1. เปิด n8n → ไปที่ Credentials (เมนูซ้าย)
2. กด "Add Credential" → เลือก "Header Auth"
3. ตั้งค่า:

**สำหรับ OpenAI:** (ไม่ต้องทำ เพราะใช้ OpenAI Node ตรงๆ ที่มี Credential ในตัว)

**สำหรับ ElevenLabs:**
- Name: ElevenLabs API Key
- Header Name: xi-api-key
- Header Value: (วาง API Key ของคุณ)

**สำหรับ Runway:**
- Name: Runway API Key
- Header Name: Authorization
- Header Value: Bearer (วาง API Key ของคุณ)

4. กด Save

เท่านี้ n8n จะจำ API Key ไว้ ไม่ต้องใส่ซ้ำทุกครั้ง


---
---

# II

## PART 2
## Workshop 1: สคริป → เสียง
## Script to Voice

ระดับ: ง่าย | 4 Nodes | ~15 นาที

---

### เป้าหมาย

ป้อนชื่อสินค้าเข้าไป → ได้ไฟล์เสียง MP3 ที่ AI เขียนสคริปให้ + พูดให้

ไม่ต้องเขียนสคริปเอง ไม่ต้องอัดเสียงเอง

---

### Workflow หน้าตาเป็นแบบนี้

```
[Manual Trigger] → [AI เขียนสคริป] → [ElevenLabs TTS] → [บันทึกไฟล์ MP3]
     กดปุ่ม          OpenAI            HTTP Request         Write File
```

4 Nodes ง่ายๆ เรียงเป็นเส้นตรง ไม่มีแยก ไม่มี loop

---

### Step 1: สร้าง Workflow ใหม่ + วาง Manual Trigger

1. เปิด n8n → กด "New Workflow"
2. ตั้งชื่อ: "Workshop 1 — Script to Voice"
3. จะเห็น Manual Trigger อยู่แล้ว (n8n ใส่ให้อัตโนมัติ)

Manual Trigger คือปุ่มเริ่มต้น กดแล้ว workflow ทำงาน

ตอนนี้ใช้แบบกดเทสก่อน พอถึงบทหลังจะเปลี่ยนเป็น Webhook ให้ระบบอื่นสั่งงานได้เอง

---

### Step 2: เพิ่ม OpenAI Node — ให้ AI เขียนสคริป

1. กดปุ่ม + ต่อจาก Trigger
2. ค้นหา "OpenAI" → เลือก OpenAI Node
3. ตั้งค่า:
   - Resource: Chat
   - Model: gpt-4o-mini (ถูกและเร็ว เหมาะกับงานเขียนสคริป)
   - Messages → User Message:

```
เขียนสคริปวิดีโอแนะนำสินค้า "กาแฟดริป DewBrew"
ความยาว 60 วินาที ภาษาไทย โทนเป็นกันเอง
โครงสร้าง: Hook → ปัญหา → แนะนำสินค้า → CTA
ห้ามใช้ภาษาทางการ ใช้ภาษาพูด
```

4. ใส่ OpenAI Credential (จาก Chapter 0 ที่ตั้งไว้แล้ว)

---

#### เทคนิคเขียน Prompt สำหรับสคริปวิดีโอ

Prompt ที่ดีต้องบอก AI ให้ครบ 5 อย่าง:

[1] **ชื่อสินค้า** — "กาแฟดริป DewBrew"
[2] **ความยาว** — "60 วินาที" (ถ้าไม่บอก AI จะเขียนยาวเกิน)
[3] **ภาษา + โทน** — "ภาษาไทย โทนเป็นกันเอง"
[4] **โครงสร้าง** — "Hook → ปัญหา → สินค้า → CTA"
[5] **ห้ามทำอะไร** — "ห้ามใช้ภาษาทางการ"

ถ้า output ไม่ดี 90% ของปัญหาคือ prompt ไม่ดี ไม่ใช่ AI ไม่เก่ง

ลองเปลี่ยนทีละจุด: เปลี่ยนโทน เปลี่ยนความยาว เปลี่ยนโครงสร้าง

---

#### ลองเปลี่ยน prompt ดู

ไม่จำเป็นต้องขายสินค้าเสมอ ลองเปลี่ยน prompt เป็นแบบอื่น:

**สคริปรีวิว:**
```
เขียนสคริปรีวิวร้านอาหาร "ข้าวมันไก่ ประตูน้ำ"
ความยาว 30 วินาที สไตล์ TikTok
โครงสร้าง: เปิดด้วยคำถาม → รีวิว → คะแนน → CTA
```

**สคริปสอน:**
```
เขียนสคริปสอนใช้ n8n เบื้องต้น
ความยาว 90 วินาที โทนครูสอน แต่ไม่ boring
โครงสร้าง: ปัญหา → n8n แก้ได้ → สาธิต 3 ข้อ → ชวนลอง
```

ทุกครั้งที่เปลี่ยน prompt → กด Execute → ดูผลลัพธ์

---

### Step 3: เพิ่ม HTTP Request Node → ElevenLabs TTS

นี่คือ Node ที่สำคัญที่สุดใน Workshop นี้

เราจะเอาสคริปที่ AI เขียน ส่งไปให้ ElevenLabs แปลงเป็นเสียงพูด

1. กดปุ่ม + ต่อจาก OpenAI Node
2. ค้นหา "HTTP Request" → เลือก
3. ตั้งค่า:

**Method:** POST

**URL:**
```
https://api.elevenlabs.io/v1/text-to-speech/YOUR_VOICE_ID
```
⚠️ ต้องเปลี่ยน YOUR_VOICE_ID เป็น Voice ID จริงของคุณ

**Authentication:** Header Auth → เลือก Credential ที่สร้างไว้ (ElevenLabs API Key)

**Headers:**
- Content-Type: application/json

**Body Parameters:**
- text: `{{ $json.message.content }}` ← ดึงสคริปจาก OpenAI
- model_id: `eleven_multilingual_v2` ← สำคัญมาก! ต้องใช้ตัวนี้ถึงจะพูดไทยได้
- voice_settings: `{"stability": 0.5, "similarity_boost": 0.75}`

**Options → Response:**
- Response Format: File (สำคัญ! ต้องตั้งเป็น File เพราะ output เป็นไฟล์เสียง)

---

#### อธิบาย voice_settings

**stability (0.0 - 1.0):**
- ต่ำ (0.3) = เสียงมีอารมณ์ มีขึ้นลง เหมือนคนพูดจริง
- สูง (0.8) = เสียงนิ่งๆ สม่ำเสมอ เหมือนอ่านข่าว

**similarity_boost (0.0 - 1.0):**
- ต่ำ (0.3) = เสียงอิสระ ไม่ค่อยเหมือนต้นฉบับ
- สูง (0.8) = เสียงเหมือนต้นฉบับมากขึ้น

ผมแนะนำเริ่มที่ stability: 0.5, similarity_boost: 0.75

ถ้าเสียงฟังแปลกๆ ลองปรับทีละ 0.1 ดู

---

#### Voice ID หายังไง?

1. ไปที่ elevenlabs.io → เข้า Voices
2. เลือก voice ที่ชอบ (มีหลายเสียงให้เลือก)
3. กดที่ชื่อ voice → จะเห็น Voice ID
4. Copy มาวางแทน YOUR_VOICE_ID ใน URL

Tip: ถ้าอยากได้เสียงไทย ลองค้นหาเสียงที่มี "Thai" หรือลอง voice หลายๆ ตัว
เพราะ eleven_multilingual_v2 รองรับไทย ทุก voice พูดไทยได้หมด

---

### Step 4: เพิ่ม Write Binary File — บันทึกไฟล์ MP3

1. กดปุ่ม + ต่อจาก HTTP Request
2. ค้นหา "Write Binary File" → เลือก
3. ตั้งค่า:
   - File Name: `script-voice-output.mp3`
   - Property Name: `data`

ไฟล์จะถูกบันทึกที่ server n8n ของคุณ

---

### ทดสอบ!

1. กดปุ่ม "Test Workflow" (มุมขวาบน)
2. รอสักครู่ (ไม่นาน ~5-10 วินาที)
3. ดูผลลัพธ์ที่แต่ละ Node:
   - OpenAI → จะเห็นสคริปที่ AI เขียน
   - ElevenLabs → จะเห็นไฟล์เสียง
   - Write File → ไฟล์ถูกบันทึก

ถ้าทุก Node เป็นสีเขียว = สำเร็จ!

ถ้ามี Node แดง → ดู error message → เทียบกับ Troubleshoot ด้านล่าง

---

### Troubleshoot — ปัญหาที่เจอบ่อย

**Error 401 (Unauthorized)**
→ API Key ผิด สร้างใหม่แล้วลองอีกที

**เสียงออกมาเป็นภาษาอังกฤษ**
→ เช็คว่าใช้ model: eleven_multilingual_v2
→ ไม่ใช่ eleven_monolingual_v1 (ตัวนี้รองรับแค่อังกฤษ)

**เสียงฟังแปลกๆ/หุ่นยนต์**
→ ลอง stability: 0.3 (ธรรมชาติขึ้น)
→ ลอง similarity_boost: 0.8 (เหมือนต้นฉบับมากขึ้น)

**ไฟล์ไม่ถูกบันทึก**
→ เช็ค Property Name ว่าตรงกับ output ของ ElevenLabs

---

### แบบฝึกหัด Workshop 1

ลองทำเองดู:

1. เปลี่ยนสินค้าจาก "กาแฟ" เป็นสินค้าของคุณเอง
2. เปลี่ยน prompt ให้เขียนสคริปแนว "รีวิว" แทน "ขาย"
3. ลองเปลี่ยน Voice ID เป็นเสียงอื่น
4. ลองปรับ voice_settings ให้เสียงธรรมชาติที่สุด

ทำ 4 ข้อนี้ครบ = คุณพร้อมไป Workshop 2 แล้ว


---
---

# III

## PART 3
## Workshop 2: รูปสินค้า → วิดีโอ
## Image to VDO

ระดับ: กลาง | 5 Nodes | ~20 นาที

---

### เป้าหมาย

ป้อนรูปสินค้า + ชื่อ → ได้วิดีโอสั้น 5 วินาที + caption

ไม่ต้องเปิด Premiere ไม่ต้องตัดต่อ

---

### Workflow หน้าตาเป็นแบบนี้

```
[Manual Trigger] → [AI เขียน caption] → [Runway Image→VDO] → [รอ render] → [เช็ค+ดาวน์โหลด]
     กดปุ่ม           OpenAI             HTTP Request        Wait         HTTP Request
```

5 Nodes มากกว่า Workshop 1 แค่ 1 ตัว แต่มี concept ใหม่: **Async Processing**

---

### Concept ใหม่: Async Processing (ส่งงาน → รอ → เช็คผล)

Workshop 1 ทุกอย่างเกิดขึ้นทันที ส่ง text ไป → ได้เสียงกลับมาเลย

แต่ Workshop 2 ไม่ใช่แบบนั้น

Runway ต้องใช้เวลา render วิดีโอ (30 วิ - 2 นาที)

เราส่งงานไป → Runway บอก "รับแล้ว นี่ task ID" → เราต้องรอ → แล้วกลับมาถามว่า "เสร็จยัง?"

เหมือนสั่งอาหารแล้วรอเสิร์ฟ ไม่ใช่ซื้อข้าวกล่องได้ทันที

```
สั่งงาน (POST) → ได้ task_id → รอ 30 วิ → เช็คสถานะ (GET) → ได้ URL วิดีโอ
```

concept นี้จะเจออีกใน Chapter 3 (HeyGen ก็ต้องรอ render เหมือนกัน)

---

### Step 1: สร้าง Workflow + ตั้ง Input

1. สร้าง Workflow ใหม่: "Workshop 2 — Image to VDO"
2. Manual Trigger มาให้แล้ว

สิ่งที่ต้องเตรียม:
- **URL รูปสินค้า** — ต้องเป็น URL ที่เข้าถึงได้ (อัพขึ้น hosting หรือใช้ link จาก Google Drive/Imgur)
- **ชื่อสินค้า + จุดเด่น** — จะใส่ใน prompt

---

### Step 2: OpenAI Node — เขียนคำบรรยาย TikTok

1. เพิ่ม OpenAI Node ต่อจาก Trigger
2. ตั้งค่า:
   - Model: gpt-4o-mini
   - Message:

```
เขียนคำบรรยายสินค้าสำหรับวิดีโอ TikTok ความยาว 15 วินาที
สินค้า: กาแฟดริป DewBrew
จุดเด่น: กาแฟสดคั่วจากเชียงใหม่ หอมมาก
โครงสร้าง: ปัญหาที่พบ → โชว์สินค้า → ประโยชน์ → CTA ซื้อเลย
ภาษาไทย โทนกันเอง สั้นกระชับ
```

**ต่างจาก Workshop 1:**
Workshop 1 เขียน "สคริป" สำหรับคนพูด
Workshop 2 เขียน "caption" สำหรับวิดีโอสินค้า — สั้นกว่า ตรงกว่า

---

### Step 3: HTTP Request → Runway API (Image-to-Video)

นี่คือหัวใจของ Workshop นี้

1. เพิ่ม HTTP Request Node
2. ตั้งค่า:

**Method:** POST
**URL:** `https://api.runwayml.com/v1/image_to_video`

**Headers:**
- Content-Type: application/json
- X-Runway-Version: 2024-11-06

**Authentication:** Header Auth → เลือก Credential ที่สร้างไว้ (Runway API Key)

**Body (JSON):**
```json
{
  "model": "gen4_turbo",
  "promptImage": "https://YOUR-IMAGE-URL.jpg",
  "promptText": "smooth zoom in on product, professional lighting, clean background",
  "duration": 5,
  "ratio": "720p"
}
```

---

#### อธิบายค่าใน Body

**model: "gen4_turbo"**
รุ่นล่าสุดของ Runway เร็วและคุณภาพดี ใช้ตัวนี้

**promptImage:**
URL ของรูปสินค้า ต้องเป็น URL ที่ Runway เข้าถึงได้
⚠️ รูปจาก Google Drive ต้อง set sharing เป็น "Anyone with the link"

**promptText:**
บอก Runway ว่าอยากให้วิดีโอเคลื่อนไหวยังไง
- "smooth zoom in" = ซูมเข้าช้าๆ
- "slow pan left to right" = แพนจากซ้ายไปขวา
- "gentle rotation" = หมุนเบาๆ
- "product showcase, professional lighting" = แสงสวย สไตล์โฆษณา

**duration:** 5 (วินาที) — เริ่มที่ 5 ก่อน ประหยัด credit

**ratio:** "720p" — สำหรับ TikTok/Reels ใช้ 720p แนวตั้ง

---

#### เทคนิครูปที่ได้ผลดี

ไม่ใช่ทุกรูปจะได้วิดีโอสวย

**รูปที่ดี:**
- พื้นหลังสะอาด สีเดียว หรือสีขาว
- สินค้าอยู่กลางภาพ
- แสงสว่างสม่ำเสมอ
- ความละเอียดสูง (1024px ขึ้นไป)

**รูปที่แย่:**
- พื้นหลังรก มีของเยอะ
- สินค้าเล็กจิ๋ว อยู่มุมภาพ
- มืด หรือแสงจ้าเกินไป
- ภาพเบลอ ความละเอียดต่ำ

ถ้ารูปไม่ดี → วิดีโอจะเบลอ/แปลก → แก้ที่รูป ไม่ใช่แก้ที่ Runway

---

### Step 4: Wait Node — ทำไมต้องรอ

1. เพิ่ม Wait Node ต่อจาก Runway
2. ตั้งค่า: Amount: 30, Unit: Seconds

ทำไมต้องรอ?

เพราะ Runway ไม่ได้ให้วิดีโอทันที มันต้อง render ก่อน

พอเราส่ง request ไป Runway จะตอบกลับมาแค่:
```json
{
  "id": "task_abc123..."
}
```

นี่คือ "หมายเลขคิว" ของงาน ยังไม่มีวิดีโอ

เราต้อง "รอ" แล้วค่อยไปถามว่าวิดีโอเสร็จยัง

30 วินาทีมักจะพอ แต่ถ้าไม่เสร็จก็เปลี่ยนเป็น 60 วินาที

---

### Step 5: HTTP Request GET — เช็คสถานะ + ดาวน์โหลด

1. เพิ่ม HTTP Request Node อีกตัว
2. ตั้งค่า:

**Method:** GET
**URL:** `https://api.runwayml.com/v1/tasks/{{ $json.id }}`

⚠️ `{{ $json.id }}` คือ Expression ที่ดึง task ID จาก Step 3 มาใช้

**Authentication:** Header Auth → ใช้ Credential เดิม (Runway API Key)

---

#### สถานะที่เป็นไปได้

| สถานะ | ความหมาย | ทำยังไง |
|-------|---------|--------|
| PROCESSING | กำลังทำ | รอแล้วกด Execute อีกที |
| COMPLETED | เสร็จ! | ดู output → ได้ URL วิดีโอ |
| FAILED | ผิดพลาด | เช็ครูป/prompt แล้วลองใหม่ |

ถ้า COMPLETED → URL วิดีโออยู่ใน `$json.output`

Copy URL ไปเปิดในเบราว์เซอร์ → จะเห็นวิดีโอ!

---

### ทดสอบ!

1. เตรียม URL รูปสินค้า
2. กด "Test Workflow"
3. รอ... (นานกว่า Workshop 1 เพราะต้องรอ Runway render)
4. เช็ค Node สุดท้าย:
   - ถ้า status: COMPLETED → สำเร็จ!
   - ถ้า status: PROCESSING → กดรัน Node สุดท้ายอีกทีเพื่อเช็คใหม่

---

### Troubleshoot — ปัญหาที่เจอบ่อย

**Error 401/403**
→ API Key ผิด หรือหมด credit ลองสร้าง Key ใหม่

**วิดีโอออกมาแปลกๆ/เบลอ**
→ เปลี่ยนรูป ใช้พื้นหลังสะอาด
→ promptText ให้ชัดเจน: "slow pan", "gentle zoom"

**ยัง PROCESSING อยู่**
→ รอนานขึ้น เปลี่ยน Wait เป็น 60 วินาที
→ หรือกด Execute Node สุดท้ายซ้ำ

**Failed**
→ เช็คว่ารูป URL เข้าถึงได้จริง (ลองเปิดใน browser)
→ เช็คว่า format เป็น JPEG/PNG

---

### แบบฝึกหัด Workshop 2

1. เปลี่ยนรูปเป็นสินค้าของคุณเอง
2. ลองเปลี่ยน promptText: "dramatic zoom out" / "slow rotate" / "cinematic pan"
3. ลอง duration: 10 (ดูว่าต่างจาก 5 วินาทียังไง)
4. เอา caption จาก OpenAI Node มาใช้เป็น caption จริงตอนโพส


---
---

# IV

## PART 4
## เปรียบเทียบ 2 Workshops

---

### WS1 vs WS2 — ใช้ตอนไหน?

| | Workshop 1 | Workshop 2 |
|---|---|---|
| **Output** | เสียง MP3 | วิดีโอ MP4 |
| **AI Tool** | ElevenLabs | Runway |
| **ค่าใช้จ่าย** | ต่ำมาก (Free tier) | ~$0.25/ตัว |
| **เวลา** | ~5 วินาที | ~30-60 วินาที |
| **Nodes** | 4 | 5 |
| **Concept ใหม่** | TTS API | Async Processing |
| **เหมาะกับ** | Podcast, voiceover, สคริปพูด | TikTok, Reels, วิดีโอสินค้า |

---

### รวมร่าง: ใช้ WS1 + WS2 ด้วยกัน

นี่คือ power ที่แท้จริง — เอา 2 workshops มารวมกัน

**WS1 → เสียง + WS2 → วิดีโอ = คอนเทนต์ชุดเดียว**

ตัวอย่าง:
- WS1 สร้างเสียงพากย์สินค้า
- WS2 สร้างวิดีโอจากรูปสินค้า
- เอามารวมกัน → ได้วิดีโอพร้อมเสียง

(จะสอนรวมร่างจริงๆ ใน Chapter 3 ตอนทำ AI Clone)


---
---

# V

## PART 5
## Checklist ก่อนไป Chapter 3

---

ก่อนไปต่อ เช็คตัวเองให้ครบ:

☑ Workshop 1: สร้าง workflow ได้ กดรันแล้วได้ไฟล์เสียง MP3
☑ Workshop 2: สร้าง workflow ได้ กดรันแล้วได้วิดีโอ
☑ เข้าใจ Prompt Engineering เบื้องต้น (บอก AI ให้ครบ 5 อย่าง)
☑ เข้าใจ Async Processing (ส่งงาน → รอ → เช็คผล)
☑ สร้าง Credential ใน n8n ได้เอง
☑ แก้ปัญหา Error 401 ได้เอง

ถ้ายังทำไม่ครบ กลับไปลองอีกรอบ ไม่ต้องรีบ

---

### Preview: Chapter 3 จะทำอะไร

Chapter 3 คือระดับยาก — **AI Avatar + AI Clone**

| | Workshop 3 | Workshop 4 |
|---|---|---|
| Output | วิดีโอ Avatar พูด | วิดีโอ "ตัวเอง" พูด (AI Clone) |
| AI Tool | HeyGen | ElevenLabs + HeyGen |
| ระดับ | ยาก | ยากสุด |
| Nodes | 5 | 6 |
| Concept | Avatar Video API | Voice Clone + Face Clone |

Workshop 4 รวมทุก skill จาก Workshop 1-3 เข้าด้วยกัน:
- สคริป (จาก WS1)
- เสียง Clone (จาก WS1 + ขั้นสูง)
- วิดีโอ Avatar (จาก WS3)

ถ้า WS1-2 ยังไม่แม่น → WS3-4 จะยากมาก

ลองจนมั่นใจก่อนครับ แล้วไปต่อกัน

---

จบเนื้อหา
หลายคนอ่านเสร็จอาจจะยังงงๆ ไม่เป็นไร
ผมไม่ค่อยชอบอ่านหนังสือเหมือนกัน
เน้นลงมือทำจริงกันดีกว่าครับ จะได้เห็นภาพมากขึ้น

---
