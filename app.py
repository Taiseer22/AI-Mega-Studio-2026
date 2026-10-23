import streamlit as st
from huggingface_hub import InferenceClient
import os

st.set_page_config(page_title="Anannan Studio Pro 2026", layout="centered")
st.markdown("<h2>⚡ Anannan Studio Pro 2026</h2>", unsafe_allow_html=True)
st.caption("صناعة وتحويل التطبيقات الاحترافية - Taiseer22")

prompt = st.text_area("اكتب وصف الصورة", value="luxury Arabic palace, cinematic lighting, ultra detailed, 8k")

if st.button("⚡ توليد بـ Anannan", type="primary", use_container_width=True):
    try:
        token = st.secrets.get("HF_TOKEN") or os.getenv("HF_TOKEN")
        if not token:
            st.error("ما لقيت التوكن! تأكد من Secrets")
        else:
            client = InferenceClient(token=token)
            # موديل جديد شغال 2026
            image = client.text_to_image(
                prompt,
                model="stabilityai/stable-diffusion-xl-base-1.0"
            )
            st.image(image, caption="Anannan Studio - Taiseer22")
            st.success("تم التوليد! 🔥")
    except Exception as e:
        st.error(f"Error: {e}")

st.caption("© 2026 Taiseer22 | Anannan Studio")