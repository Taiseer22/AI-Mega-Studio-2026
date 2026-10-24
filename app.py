import streamlit as st
import requests
from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageDraw
from io import BytesIO
import urllib.parse, random

st.set_page_config(page_title="Anannan Studio V5 - Tourism", page_icon="🏜️", layout="wide")
st.markdown("<style>.stApp{background:#0e0e10; color:#eee} .stButton>button{background:linear-gradient(90deg,#ff8a00,#e52e71); color:white; border-radius:12px; height:50px; font-weight:bold;}</style>", unsafe_allow_html=True)

if 'gallery' not in st.session_state: st.session_state.gallery=[]
if 'chat' not in st.session_state: st.session_state.chat=[]

st.title("🏜️ Anannan Studio V5 - للسياحة والفنادق")
st.caption("توليد + تعديل صور حية + إصلاح + توسيع + استنساخ - صنع في البتراء 🇯🇴")

tab1, tab2, tab3, tab4 = st.tabs(["🎨 توليد", "🛠️ تعديل الصور الحية", "💬 دردشة", "🖼️ المعرض"])

with tab1:
    # نفس توليد V4
    prompt = st.text_area("وصف الصورة", "luxury hotel in Petra, cinematic")
    w,h = 1024,1024
    if st.button("⚡ توليد", use_container_width=True):
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt + ', ultra-detailed, 8k')}?width={w}&height={h}&model=flux&seed={random.randint(1,9999999)}&nologo=true&enhance=true"
        r = requests.get(url, timeout=90)
        if r.status_code==200:
            img = Image.open(BytesIO(r.content)).convert("RGB").crop((0,0,w,h-35)).resize((w,h), Image.LANCZOS)
            st.image(img, use_container_width=True)
            st.session_state.gallery.append(img)

with tab2:
    st.markdown("### 🛠️ استوديو تعديل الصور الحية - للفنادق والمطاعم")
    st.info("ارفع صورة حقيقية من فندق / مطعم / سياح وعدلها باحتراف")
    
    uploaded = st.file_uploader("📤 ارفع صورة حية (JPG/PNG)", type=["jpg","jpeg","png"])
    
    if uploaded:
        original = Image.open(uploaded).convert("RGB")
        st.image(original, caption="الصورة الأصلية", use_container_width=True)
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.markdown("#### ✨ إصلاح وترميم")
            if st.button("🔧 إصلاح تلقائي ULTRA"):
                # إصلاح تلقائي
                img = original.copy()
                img = ImageEnhance.Sharpness(img).enhance(1.6)
                img = ImageEnhance.Contrast(img).enhance(1.2)
                img = ImageEnhance.Color(img).enhance(1.25)
                img = ImageEnhance.Brightness(img).enhance(1.05)
                # إزالة تشويش خفيف
                img = img.filter(ImageFilter.UnsharpMask(radius=1.5, percent=150, threshold=2))
                st.image(img, caption="بعد الإصلاح", use_container_width=True)
                buf=BytesIO(); img.save(buf, format="PNG")
                st.download_button("📥 تحميل بعد الإصلاح", buf.getvalue(), "fixed.png", "image/png", key="fix")
                st.session_state.gallery.append(img)
                
            if st.button("🎨 تلوين وتحسين الألوان"):
                img = ImageEnhance.Color(original).enhance(1.6)
                img = ImageEnhance.Contrast(img).enhance(1.15)
                st.image(img, use_container_width=True)
                buf=BytesIO(); img.save(buf, format="PNG")
                st.download_button("📥 تحميل ملون", buf.getvalue(), "color.png", "image/png", key="color")

        with col_b:
            st.markdown("#### 🎭 تأثيرات احترافية")
            effect = st.selectbox("اختر التأثير", ["بدون", "سينمائي - Cinematic", "فينتاج سياحي", "HDR للفنادق", "أبيض وأسود فاخر", "إضاءة ذهبية - Golden Hour", "Petra Rose Filter"])
            
            if st.button("✨ تطبيق التأثير"):
                img = original.copy()
                if effect == "سينمائي - Cinematic":
                    img = ImageEnhance.Contrast(img).enhance(1.3)
                    img = ImageEnhance.Color(img).enhance(0.8)
                    overlay = Image.new("RGB", img.size, (20, 10, 40))
                    img = Image.blend(img, overlay, 0.15)
                elif effect == "فينتاج سياحي":
                    img = ImageEnhance.Color(img).enhance(0.7)
                    img = img.filter(ImageFilter.GaussianBlur(0.5))
                    overlay = Image.new("RGB", img.size, (200,180,120))
                    img = Image.blend(img, overlay, 0.2)
                elif effect == "HDR للفنادق":
                    img = ImageEnhance.Contrast(img).enhance(1.4)
                    img = ImageEnhance.Sharpness(img).enhance(2.0)
                    img = ImageEnhance.Color(img).enhance(1.3)
                elif effect == "أبيض وأسود فاخر":
                    img = ImageOps.grayscale(img).convert("RGB")
                    img = ImageEnhance.Contrast(img).enhance(1.2)
                elif effect == "إضاءة ذهبية - Golden Hour":
                    overlay = Image.new("RGB", img.size, (255,180,50))
                    img = Image.blend(img, overlay, 0.18)
                    img = ImageEnhance.Brightness(img).enhance(1.1)
                elif effect == "Petra Rose Filter":
                    overlay = Image.new("RGB", img.size, (180, 60, 60))
                    img = Image.blend(img, overlay, 0.12)
                    img = ImageEnhance.Color(img).enhance(1.2)
                
                st.image(img, caption=f"تأثير: {effect}", use_container_width=True)
                buf=BytesIO(); img.save(buf, format="PNG")
                st.download_button(f"📥 تحميل {effect}", buf.getvalue(), f"{effect}.png", "image/png", key="eff")
                st.session_state.gallery.append(img)

        with col_c:
            st.markdown("#### ↔️ توسيع واستنساخ")
            
            expand = st.selectbox("توسيع الصورة", ["بدون", "توسيع 16:9 للبنر", "توسيع 9:16 ستوري", "توسيع بانوراما 2x", "إضافة إطار أبيض احترافي"])
            if st.button("↔️ توسيع"):
                img = original.copy()
                ow, oh = img.size
                if "16:9" in expand:
                    # توسيع للعرض
                    new_w = int(oh * 16/9)
                    if new_w > ow:
                        # إنشاء خلفية موسعة بتمويه الحواف
                        bg = img.resize((new_w, oh)).filter(ImageFilter.GaussianBlur(25))
                        bg.paste(img, ((new_w-ow)//2, 0))
                        img = bg
                elif "9:16" in expand:
                    new_h = int(ow * 16/9)
                    bg = img.resize((ow, new_h)).filter(ImageFilter.GaussianBlur(25))
                    bg.paste(img, (0, (new_h-oh)//2))
                    img = bg
                elif "بانوراما" in expand:
                    bg = Image.new("RGB", (ow*2, oh), (0,0,0))
                    bg.paste(img, (0,0))
                    mirrored = ImageOps.mirror(img).filter(ImageFilter.GaussianBlur(15))
                    bg.paste(mirrored, (ow,0))
                    img = bg
                elif "إطار" in expand:
                    img = ImageOps.expand(img, border=40, fill="white")
                    draw = ImageDraw.Draw(img)
                    draw.rectangle([(0,0),(img.width-1, img.height-1)], outline="black", width=2)
                
                st.image(img, caption=expand, use_container_width=True)
                buf=BytesIO(); img.save(buf, format="PNG")
                st.download_button("📥 تحميل موسعة", buf.getvalue(), "expanded.png", "image/png", key="exp")
                st.session_state.gallery.append(img)

            st.markdown("---")
            clone_style = st.selectbox("استنساخ الاستايل", ["", "حولها لصورة فاخرة للفندق", "حولها لكرتون سياحي", "حولها ليلية بإضاءة رومانسية", "Petra Luxury Style"])
            if st.button("🧬 استنساخ وتحويل"):
                if clone_style:
                    # استنساخ عن طريق AI - نولد صورة مشابهة
                    prompt_map = {
                        "حولها لصورة فاخرة للفندق": "luxury hotel photo, professional photography, 8k, same composition, ultra-detailed",
                        "حولها لكرتون سياحي": "cartoon style, tourist poster, vibrant, same composition",
                        "حولها ليلية بإضاءة رومانسية": "night version, romantic lighting, warm lights, same place, 8k",
                        "Petra Luxury Style": "Petra Jordan luxury tourism style, rose red rocks, dramatic lighting, 8k"
                    }
                    p = prompt_map.get(clone_style, clone_style)
                    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p)}?width=1024&height=1024&model=flux&seed={random.randint(1,9999999)}&nologo=true"
                    r = requests.get(url, timeout=90)
                    if r.status_code==200:
                        new_img = Image.open(BytesIO(r.content)).convert("RGB")
                        st.image(new_img, caption=f"مستنسخة: {clone_style}", use_container_width=True)
                        buf=BytesIO(); new_img.save(buf, format="PNG")
                        st.download_button("📥 تحميل مستنسخة", buf.getvalue(), "cloned.png", "image/png", key="clone")
                        st.session_state.gallery.append(new_img)

with tab3:
    st.markdown("### 💬 دردشة سياحية")
    for m in st.session_state.chat:
        with st.chat_message(m["role"]): st.write(m["content"])
    if q := st.chat_input("اسأل عن أفكار سياحية..."):
        st.session_state.chat.append({"role":"user","content":q})
        with st.chat_message("user"): st.write(q)
        with st.chat_message("assistant"):
            try:
                r = requests.get(f"https://text.pollinations.ai/{urllib.parse.quote(q)}?model=openai&system=You are Anannan tourism expert from Petra, help with tourism marketing ideas in Arabic.", timeout=20)
                ans = r.text
            except:
                ans = "أهلاً! أنا خبير سياحة البتراء، كيف أساعدك تسوق لفندقك؟"
            st.write(ans)
            st.session_state.chat.append({"role":"assistant","content":ans})

with tab4:
    st.markdown(f"### معرض - {len(st.session_state.gallery)} صورة")
    cols = st.columns(3)
    for i, im in enumerate(reversed(st.session_state.gallery)):
        with cols[i%3]:
            st.image(im, use_container_width=True)

st.caption("© 2026 Taiseer22 | V5 Tourism Edition | البتراء 🇯🇴")