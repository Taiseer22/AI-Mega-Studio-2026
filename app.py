import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from io import BytesIO
import urllib.parse
import random

st.set_page_config(page_title="Anannan Studio ULTRA V3", page_icon="⚡", layout="wide")

st.markdown("""
<style>
.stApp {background-color: #0e0e10; color: #e0e0e0;}
h1 {color: #f5f5f5; text-align: center;}
.stButton>button {background: linear-gradient(90deg, #ff00cc, #3333ff); color: white; border-radius: 12px; height: 55px; font-weight: bold; width: 100%; font-size: 16px;}
</style>
""", unsafe_allow_html=True)

st.title("⚡ Anannan Studio ULTRA V3")
st.markdown("<p style='text-align:center; color:#aaa;'>بدون علامة مائية | وجوه واضحة 8K | تحويل لفيديو - صنع في البتراء 🇯🇴</p>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    prompt = st.text_area("🎨 وصف الصورة", placeholder="beautiful Jordanian woman, traditional white hijab, cinematic lighting", height=120)
    
    st.markdown("**💡 دوس للنسخ السريع:**")
    quick = ["luxury villa in Petra at sunset, 8k", "Jordanian woman, ultra-detailed face, sharp focus, 8k portrait", "anime girl, Petra desert, highly detailed", "cyberpunk Amman city, neon lights"]
    cols = st.columns(2)
    for i, s in enumerate(quick):
        if cols[i%2].button(f"📌 {s[:30]}", key=s):
            st.session_state['p'] = s
            prompt = s

with col2:
    st.markdown("### ⚙️ التحكم الكامل")
    style = st.selectbox("🎭 الاستايل", ["Realistic - واقعي", "Cinematic - سينمائي", "Anime - انمي", "3D Pixar", "Luxury Interior", "Cyberpunk"])
    quality = st.selectbox("💎 الجودة", ["ULTRA 4K (1024x1024)", "Wide 16:9 (1280x720)", "Portrait 9:16 (720x1280)", "HD (1536x1536) خارقة"])
    face_enhance = st.checkbox("✨ تحسين الوجه 8K (يزيل التشويش)", value=True)
    remove_wm = st.checkbox("🚫 إزالة العلامة المائية نهائياً", value=True)
    make_video = st.checkbox("🎬 تحويل لفيديو بعد التوليد", value=False)

if "1024" in quality: w,h = 1024,1024
elif "1280x720" in quality: w,h = 1280,720
elif "720x1280" in quality: w,h = 720,1280
else: w,h = 1536,1536

style_add = {
    "Realistic": ", ultra-realistic, sharp focus, 8k, highly detailed skin, perfect face, DSLR",
    "Cinematic": ", cinematic lighting, 8k, dramatic, movie still, ultra-detailed face",
    "Anime": ", anime, ultra-detailed face, beautiful eyes, Studio Ghibli",
    "3D Pixar": ", 3D Pixar, ultra-detailed face, cute, octane",
    "Luxury Interior": ", luxury interior, 8k, architectural",
    "Cyberpunk": ", cyberpunk, neon, 8k, ultra-detailed"
}
face_add = ", ultra-detailed face, perfect eyes, sharp focus, flawless skin, 8k portrait, high detail face" if face_enhance else ""
final_prompt = prompt + style_add.get(style.split(" -")[0], "") + face_add

if st.button("⚡ توليد ULTRA V3 - بدون علامة + وجه واضح", use_container_width=True):
    if not prompt.strip():
        st.warning("اكتب وصف!")
    else:
        with st.spinner("🎨 جاري التوليد بجودة خارقة..."):
            try:
                encoded = urllib.parse.quote(final_prompt)
                seed = random.randint(1, 9999999)
                url = f"https://image.pollinations.ai/prompt/{encoded}?width={w}&height={h}&model=flux&seed={seed}&enhance=true&nologo=true"
                res = requests.get(url, timeout=90)
                if res.status_code == 200:
                    img = Image.open(BytesIO(res.content)).convert("RGB")
                    
                    # 1. إزالة العلامة المائية - قص 35 بكسل من تحت
                    if remove_wm:
                        img = img.crop((0, 0, img.width, img.height - 35))
                        img = img.resize((w, h), Image.LANCZOS)
                    
                    # 2. تحسين الوجه والحدة
                    if face_enhance:
                        enhancer = ImageEnhance.Sharpness(img)
                        img = enhancer.enhance(1.4)
                        enhancer2 = ImageEnhance.Detail if hasattr(ImageEnhance, 'Detail') else ImageEnhance.Contrast
                        try:
                            img = ImageEnhance.Contrast(img).enhance(1.15)
                            img = ImageEnhance.Color(img).enhance(1.1)
                        except: pass
                    
                    # 3. إضافة لوجو Anannan الخاص
                    draw = ImageDraw.Draw(img)
                    draw.rectangle([(w-220, h-45), (w-10, h-15)], fill=(0,0,0,120))
                    draw.text((w-200, h-40), "Anannan Studio ©", fill=(255,255,255))
                    
                    st.image(img, caption=f"Seed: {seed} | {w}x{h}", use_container_width=True)
                    
                    # تحميل صورة
                    buf = BytesIO()
                    img.save(buf, format="PNG")
                    st.download_button("📥 تحميل صورة ULTRA بدون علامة", buf.getvalue(), f"anannan_ultra_{seed}.png", "image/png", use_container_width=True)
                    
                    # 4. تحويل لفيديو (تأثير زووم سينمائي)
                    if make_video:
                        with st.spinner("🎬 جاري تحويل الصورة لفيديو 3 ثواني..."):
                            frames = []
                            for i in range(24): # 24 فريم
                                zoom = 1 + (i * 0.015)
                                new_w = int(w / zoom)
                                new_h = int(h / zoom)
                                left = (w - new_w)//2
                                top = (h - new_h)//2
                                frame = img.crop((left, top, left+new_w, top+new_h)).resize((w,h), Image.LANCZOS)
                                frames.append(frame)
                            
                            # حفظ كـ GIF فيديو
                            gif_buf = BytesIO()
                            frames[0].save(gif_buf, format="GIF", save_all=True, append_images=frames[1:], duration=80, loop=0)
                            st.download_button("🎬 تحميل الفيديو (GIF)", gif_buf.getvalue(), f"anannan_video_{seed}.gif", "image/gif", use_container_width=True)
                            st.success("🎬 الفيديو جاهز! تأثير زووم سينمائي")
                    
                    st.success(f"✅ تم! بدون علامة | وجه واضح 8K | {w}x{h}")
                else:
                    st.error("حاول مرة ثانية")
            except Exception as e:
                st.error(f"خطأ: {e}")

st.caption("© 2026 Taiseer22 | Anannan Studio ULTRA V3 | صنع في البتراء 🇯🇴 | مجاني للأبد")