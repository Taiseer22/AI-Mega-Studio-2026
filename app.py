import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import urllib.parse

st.set_page_config(page_title="Anannan Studio Pro 2026", page_icon="⚡", layout="centered")

st.markdown("""
<style>
.stApp {background-color: #0e0e10; color: #e0e0e0;}
h1 {color: #f5f5f5;}
</style>
""", unsafe_allow_html=True)

st.title("⚡ Anannan Studio Pro 2026")
st.caption("صناعة وتحويل القطع الفنية الاحترافية - Taiseer22")

prompt = st.text_area("اكتب وصف الصورة", placeholder="beach house, luxury, cinematic lighting, ultra-detailed 4k", height=150)

if st.button("⚡ توليد Anannan", use_container_width=True):
    if not prompt.strip():
        st.warning("اكتب وصف أولاً!")
    else:
        with st.spinner("جاري التوليد في Anannan Studio..."):
            try:
                # استخدام Pollinations المجاني 100%
                encoded_prompt = urllib.parse.quote(prompt)
                url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&model=flux&enhance=true&nologo=true"
                
                response = requests.get(url, timeout=60)
                if response.status_code == 200:
                    img = Image.open(BytesIO(response.content))
                    st.image(img, caption=f"تم التوليد: {prompt}", use_container_width=True)
                    
                    # زر تحميل
                    buf = BytesIO()
                    img.save(buf, format="PNG")
                    st.download_button("📥 تحميل الصورة", buf.getvalue(), file_name="anannan_studio.png", mime="image/png", use_container_width=True)
                else:
                    st.error(f"خطأ: {response.status_code}")
            except Exception as e:
                st.error(f"خطأ: {e}")

st.markdown("---")
st.caption("© 2026 Taiseer22 | Anannan Studio - مجاني 100% وبدون حدود")