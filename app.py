import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import urllib.parse, random

st.set_page_config(page_title="Anannan Studio V4", page_icon="⚡", layout="wide")

st.markdown("""
<style>
.stApp {background-color: #0e0e10; color: #e0e0e0;}
.stButton>button {background: linear-gradient(90deg, #ff00cc, #3333ff); color: white; border-radius: 12px; height: 50px; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

if 'gallery' not in st.session_state: st.session_state.gallery = []
if 'chat' not in st.session_state: st.session_state.chat = []

st.title("⚡ Anannan Studio V4 - دردشة + استوديو")

tab1, tab2, tab3 = st.tabs(["🎨 توليد صور ULTRA", "💬 دردشة Anannan AI", "🖼️ معرضي"])

with tab1:
    col1, col2 = st.columns([2,1])
    with col1:
        prompt = st.text_area("وصف الصورة", "beautiful Jordanian woman, white hijab, ultra-detailed face, 8k", height=100)
        quick = st.selectbox("اقتراحات", ["", "luxury Petra villa sunset 8k", "anime girl Petra desert", "cyberpunk Amman neon", "Jordanian woman portrait 8k"])
        if quick: prompt = quick
    with col2:
        style = st.selectbox("الاستايل", ["Realistic", "Cinematic", "Anime", "3D Pixar", "Luxury"])
        quality = st.selectbox("الجودة", ["1024x1024", "1280x720", "720x1280", "1536x1536"])
        w,h = map(int, quality.split('x'))
        enhance_face = st.checkbox("✨ وجه واضح 8K", True)
        to_video = st.checkbox("🎬 تحويل لفيديو", False)
        upscale_4k = st.checkbox("⬆️ تكبير 4K", False)

    if st.button("⚡ توليد V4", use_container_width=True):
        if prompt:
            with st.spinner("جاري التوليد..."):
                final = prompt + ", ultra-detailed face, perfect eyes, sharp focus, 8k" if enhance_face else prompt
                url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(final)}?width={w}&height={h}&model=flux&seed={random.randint(1,9999999)}&enhance=true&nologo=true"
                r = requests.get(url, timeout=90)
                if r.status_code==200:
                    img = Image.open(BytesIO(r.content)).convert("RGB")
                    img = img.crop((0,0,img.width, img.height-35)).resize((w,h), Image.LANCZOS)
                    if enhance_face:
                        from PIL import ImageEnhance
                        img = ImageEnhance.Sharpness(img).enhance(1.5)
                        img = ImageEnhance.Contrast(img).enhance(1.15)
                    if upscale_4k:
                        img = img.resize((w*2, h*2), Image.LANCZOS)
                        w,h = w*2, h*2
                    # لوجو
                    from PIL import ImageDraw
                    d = ImageDraw.Draw(img)
                    d.rectangle([(w-220,h-45),(w-10,h-15)], fill=(0,0,0))
                    d.text((w-200,h-40), "Anannan Studio ©", fill=(255,255,255))
                    
                    st.image(img, use_container_width=True)
                    buf = BytesIO(); img.save(buf, format="PNG")
                    st.download_button("📥 تحميل صورة", buf.getvalue(), f"anannan_{random.randint(1,9999)}.png", "image/png")
                    
                    # حفظ في المعرض
                    st.session_state.gallery.append(img.copy())
                    
                    # فيديو
                    if to_video:
                        frames=[]
                        for i in range(20):
                            zoom=1+i*0.02
                            nw, nh = int(w/zoom), int(h/zoom)
                            frame = img.crop(((w-nw)//2,(h-nh)//2,(w-nw)//2+nw,(h-nh)//2+nh)).resize((w,h), Image.LANCZOS)
                            frames.append(frame)
                        gif_buf=BytesIO()
                        frames[0].save(gif_buf, format="GIF", save_all=True, append_images=frames[1:], duration=80, loop=0)
                        st.download_button("🎬 تحميل فيديو", gif_buf.getvalue(), "anannan_video.gif", "image/gif")
                        st.success("فيديو زووم جاهز!")

with tab2:
    st.markdown("### 💬 دردشة Anannan AI - ذكاء اصطناعي يتذكرك")
    st.caption("اسأله عن أفكار صور، قصص، تصميم، أي شي!")
    
    for m in st.session_state.chat:
        with st.chat_message(m["role"]):
            st.write(m["content"])
    
    if q := st.chat_input("اكتب رسالتك..."):
        st.session_state.chat.append({"role":"user","content":q})
        with st.chat_message("user"): st.write(q)
        
        with st.chat_message("assistant"):
            with st.spinner("Anannan يفكر..."):
                try:
                    # دردشة مجانية 100%
                    chat_url = f"https://text.pollinations.ai/{urllib.parse.quote(q)}?model=openai&system=You are Anannan Studio AI, friendly assistant from Petra Jordan, created by Taiseer22. Answer in Arabic Jordanian dialect, short and helpful."
                    r = requests.get(chat_url, timeout=30)
                    ans = r.text if r.status_code==200 else "أهلاً! أنا Anannan AI من البتراء، كيف أساعدك؟"
                    st.write(ans)
                    st.session_state.chat.append({"role":"assistant","content":ans})
                except:
                    ans="أهلاً يا عنان! أنا جاهز، اسألني عن أي فكرة صورة!"
                    st.write(ans)
                    st.session_state.chat.append({"role":"assistant","content":ans})

with tab3:
    st.markdown(f"### 🖼️ معرضك - {len(st.session_state.gallery)} صورة")
    if not st.session_state.gallery:
        st.info("لسه ما ولدت صور - روح تبويب التوليد!")
    else:
        cols = st.columns(3)
        for i, im in enumerate(reversed(st.session_state.gallery)):
            with cols[i%3]:
                st.image(im, use_container_width=True)
                buf=BytesIO(); im.save(buf, format="PNG")
                st.download_button(f"📥 تحميل {i+1}", buf.getvalue(), f"gallery_{i}.png", "image/png", key=f"dl_{i}")
        if st.button("🗑️ مسح المعرض"):
            st.session_state.gallery=[]
            st.rerun()

st.caption("© 2026 Taiseer22 | Anannan Studio V4 | دردشة + صور + فيديو + معرض - البتراء 🇯🇴")