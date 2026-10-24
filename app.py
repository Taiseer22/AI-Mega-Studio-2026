import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import urllib.parse
import random

st.set_page_config(page_title="Anannan Studio Pro 2026", page_icon="⚡", layout="wide")

st.markdown("""
<style>
.stApp {background-color: #0e0e10; color: #e0e0e0;}
h1 {color: #f5f5f5; text-align: center;}
.stButton>button {background: linear-gradient(90deg, #ff00cc, #3333ff); color: white; border-radius: 12px; height: 50px; font-weight: bold; width: 100%;}
.stSelectbox, .stSlider {background-color: #1a1a1d;}
</style>
""", unsafe_allow_html=True)

st.title("⚡ Anannan Studio ULTRA 2026")
st.markdown("<p style='text-align:center; color:#888;'>صناعة القطع الفنية الاحترافية - Taiseer22 | جودة 4K خارقة</p>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    prompt = st.text_area("🎨 اكتب وصف الصورة", placeholder="luxury beach villa in Petra mountains, sunset, infinity pool, ultra-detailed", height=130)
    
    # اقتراحات جاهزة
    st.markdown("**💡 اقتراحات سريعة (دوس للنسخ):**")
    suggestions = [
        "luxury Arabic palace in Petra, golden sunset, cinematic lighting, ultra-detailed 8k",
        "futuristic Jordanian city, neon lights, cyberpunk, rainy night, 8k",
        "minimalist luxury living room, marble, warm light, interior design magazine",
        "anime style, beautiful Jordanian girl, desert wind, highly detailed",
        "3D cartoon, cute Bedouin house, Pixar style, vibrant colors"
    ]
    for s in suggestions:
        if st.button(f"📌 {s[:50]}...", key=s):
            st.session_state.prompt_val = s
            prompt = s

with col2:
    st.markdown("### ⚙️ الإعدادات الاحترافية")
    
    style = st.selectbox("🎭 الاستايل", [
        "Realistic - واقعي فائق", 
        "Cinematic - سينمائي", 
        "Anime - انمي ياباني", 
        "3D Pixar - كرتون 3D", 
        "Luxury Interior - ديكور فاخر",
        "Cyberpunk - مستقبلي"
    ])
    
    quality = st.selectbox("💎 الجودة", [
        "ULTRA 4K (1024x1024) - خارقة",
        "Wide 16:9 (1280x720) - عريضة",
        "Portrait 9:16 (720x1280) - طولية",
        "HD Square (1536x1536) - عالية جداً"
    ])
    
    enhance = st.checkbox("✨ تحسين تلقائي للبرومبت", value=True)
    add_logo = st.checkbox("© إضافة لوجو Anannan", value=False)

# تحديد المقاسات
if "1024" in quality: w,h = 1024,1024
elif "1280x720" in quality: w,h = 1280,720
elif "720x1280" in quality: w,h = 720,1280
else: w,h = 1536,1536

# تحديد ستايل البرومبت
style_prompts = {
    "Realistic": ", ultra-realistic, 8k, highly detailed, sharp focus, professional photography",
    "Cinematic": ", cinematic lighting, movie poster, dramatic, 8k, volumetric light",
    "Anime": ", anime style, Studio Ghibli, highly detailed anime art, vibrant",
    "3D Pixar": ", 3D render, Pixar style, octane render, cute, vibrant colors, highly detailed",
    "Luxury Interior": ", luxury interior design, architectural digest, marble, warm lighting, 8k",
    "Cyberpunk": ", cyberpunk, neon lights, futuristic, blade runner style, 8k"
}
selected_style_key = style.split(" -")[0]
final_prompt = prompt + style_prompts.get(selected_style_key, "")

st.markdown("---")

if st.button("⚡ توليد Anannan ULTRA - جودة خارقة", use_container_width=True):
    if not prompt.strip():
        st.warning("اكتب وصف أولاً!")
    else:
        with st.spinner(f"🎨 جاري التوليد بجودة {quality}... (10 ثواني)"):
            try:
                encoded = urllib.parse.quote(final_prompt)
                seed = random.randint(1, 999999)
                model = "flux" if "Realistic" in style or "Cinematic" in style else "turbo"
                url = f"https://image.pollinations.ai/prompt/{encoded}?width={w}&height={h}&model={model}&seed={seed}&enhance={str(enhance).lower()}&nologo=true"
                
                res = requests.get(url, timeout=90)
                if res.status_code == 200:
                    img = Image.open(BytesIO(res.content)).convert("RGBA")
                    
                    # اضافة لوجو
                    if add_logo:
                        draw = ImageDraw.Draw(img)
                        draw.text((w-250, h-40), "Anannan © 2026", fill=(255,255,255,180))
                    
                    st.image(img, caption=f"Prompt: {final_prompt}", use_container_width=True)
                    
                    buf = BytesIO()
                    img.convert("RGB").save(buf, format="PNG")
                    st.download_button("📥 تحميل بجودة ULTRA PNG", buf.getvalue(), file_name=f"anannan_{seed}.png", mime="image/png", use_container_width=True)
                    st.success(f"✅ تم! المقاس: {w}x{h} | الموديل: {model} | Seed: {seed}")
                else:
                    st.error(f"خطأ: {res.status_code}")
            except Exception as e:
                st.error(f"خطأ: {e}")

st.markdown("---")
st.caption("© 2026 Taiseer22 | Anannan Studio ULTRA - مجاني، مفتوح المصدر، بدون حدود | صنع في البتراء - الأردن 🇯🇴")