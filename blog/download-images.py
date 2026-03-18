"""
รันบนเครื่องตัวเอง: python download-images.py
จะดึงรูปจาก FB posts data แล้ว save ลง img/
"""
import json, urllib.request, os

with open("fb-posts-data.json") as f:
    posts = json.load(f)

sorted_posts = sorted(posts, key=lambda x: x["shares"], reverse=True)
filenames = [
    "sachin-claude-code.jpg",
    "ai-video-factory.jpg",
    "claude-browser-mcp.jpg",
    "digital-twin-case-study.jpg",
    "claude-whisper-interview.jpg",
    "claude-ad-analysis.jpg"
]

os.makedirs("img", exist_ok=True)

for post, fname in zip(sorted_posts[:6], filenames):
    url = post.get("image_url", "")
    if not url:
        print(f"SKIP {fname}")
        continue
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            with open(os.path.join("img", fname), "wb") as f:
                f.write(data)
            print(f"OK {fname}: {len(data)} bytes")
    except Exception as e:
        print(f"FAIL {fname}: {e}")

print("\nDone! Check img/ folder")
