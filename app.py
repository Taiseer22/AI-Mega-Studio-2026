import streamlit as st
import requests
import io
from PIL import Image

st.set_page_config(page_title="Anannan Studio Pro 2026", page_icon="⚡", layout="centered")

st.title("⚡ Anannan Studio Pro 2026")
st.markdown("**صناعة وحلول التطبيقات الاحترافية - Taiseer22**")

HF_TOKEN = st.secrets.get("HF_TOKEN", "")
if not HF_TOKEN:
    st.warning("⚠️ ضيف HF_TOKEN في Streamlit Secrets")
    st.stop()

headers = {"Authorization": f"Bearer {HF_TOKEN}"}
API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"

prompt = st.text_area("اكتب وصف الصورة:", "luxury Arabic palace, cinematic lighting, ultra detailed, 8k", height=100)

if st.button("توليد بـ Anannan ⚡", type="primary", use_container_width=True):
    with st.spinner("Anannan يبدع... انتظر 30 ثانية"):
        try:
            r = requests.post(API_URL, headers=headers, json={"inputs": prompt}, timeout=120)
            if r.status_code == 200:
                img = Image.open(io.BytesIO(r.content))
                st.image(img, caption="Anannan Pro 2026", use_container_width=True)
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                st.download_button("📥 تحميل", buf.getvalue(), "anannan.png", "image/png", use_container_width=True)
            elif r.status_code == 503:
                st.info("الموديل بيصحى... استنى دقيقة ودوس مرة ثانية")
            else:
                st.error(f"خطأ: {r.text[:200]}")
        except Exception as e:
            st.error(f"خطأ: {e}")

st.divider()
st.caption("© 2026 Taiseer22 | Anannan Studio")