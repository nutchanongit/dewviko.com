# dewviko.com — AI Consultant & Educator

Personal website / landing page + blog ของ Nutchanon Khongkaew (Dew)
เว็บไซต์ภาษาไทย สำหรับให้บริการ AI Consulting, Automation, และ Workshop

## Tech Stack

- **Pure HTML/CSS/JS** — ไม่มี framework, ไม่มี build tool
- **CSS** — embedded ใน `<style>` tag ของแต่ละหน้า (ไม่มีไฟล์ CSS แยก)
- **JS** — embedded ใน `<script>` tag ของแต่ละหน้า (ไม่มีไฟล์ JS แยก)
- **Font** — Google Fonts: Noto Sans Thai
- **Analytics** — Google Analytics 4 (ID: `G-3E36ECZ567`)
- **Email** — SendFox สำหรับ newsletter subscription
- **Hosting** — GitHub Pages + custom domain `dewviko.com` (ตั้งค่าใน CNAME)

## Project Structure

```
/
├── index.html              # Homepage — landing page หลัก
├── 404.html                # Custom error page
├── favicon.svg             # Site icon
├── og-image.html           # Open Graph image template
├── robots.txt              # SEO crawler config
├── sitemap.xml             # Sitemap (อัปเดตทุกครั้งที่เพิ่มหน้าใหม่)
├── CNAME                   # Custom domain config
├── blog/
│   ├── index.html          # Blog listing page
│   ├── _template.html      # Template สำหรับสร้าง blog post ใหม่
│   ├── img/                # รูปภาพของ blog posts
│   ├── *.html              # Blog posts แต่ละบทความ
│   └── fb-posts-data.json  # Facebook posts dataset
├── ebook_factory_vdo/
│   ├── index.html          # eBook/Video factory guide
│   ├── img/                # รูปภาพ
│   └── vdo/                # วิดีโอ
└── dewviko.com/            # (subdirectory เก่า — ไม่ใช้งาน)
```

## Design System / CSS Variables

```css
--green: #2D6B2D;          /* Primary color */
--green-light: #3A8A3A;    /* Primary hover */
--mint: #EEFBEE;           /* Light background accent */
--white: #FFFFFF;
--off-white: #F8F9FA;
--dark-gray: #333333;      /* Body text */
--med-gray: #6B7280;       /* Secondary text */
--light-gray: #E5E7EB;     /* Borders */
--font: 'Noto Sans Thai', sans-serif;
--radius: 12px;
--max-w: 1100px;
```

## Blog Post Workflow

เมื่อสร้าง blog post ใหม่:

1. **Copy template** — ใช้ `blog/_template.html` เป็นต้นแบบ
2. **แก้ไข meta tags** — title, description, canonical URL, OG tags
3. **แก้ไข JSON-LD** — structured data (Article schema) พร้อม datePublished
4. **เขียนเนื้อหา** — ใส่เนื้อหาบทความในส่วน body
5. **เพิ่มรูปภาพ** — ใส่ใน `blog/img/`
6. **อัปเดต sitemap.xml** — เพิ่ม `<url>` entry ใหม่
7. **อัปเดต blog/index.html** — เพิ่มลิงก์บทความใหม่ใน listing
8. **อัปเดต index.html** — ถ้าต้องการแสดงในหน้าแรก (ส่วน recent posts)

## Development & Deployment

- **Edit** — แก้ไขไฟล์ HTML โดยตรง
- **Test** — เปิดไฟล์ใน browser หรือใช้ Live Server
- **Deploy** — `git push origin main` → GitHub Pages auto-deploy
- **Domain** — dewviko.com (DNS ชี้ไป GitHub Pages)

## Conventions

- เนื้อหาทั้งหมดเป็น **ภาษาไทย** (ยกเว้น technical terms)
- ทุกหน้าต้องมี **GA4 tracking code**
- ทุกหน้าต้องมี **Open Graph meta tags** สำหรับ social sharing
- Blog posts ต้องมี **Schema.org JSON-LD** (Article type)
- ใช้ **Intersection Observer** สำหรับ fade-in animations
- Mobile responsive ด้วย CSS media queries (breakpoint: 768px)
