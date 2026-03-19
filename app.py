import streamlit as st
import requests
import io
from PIL import Image
import os

# --- إعدادات الواجهة ---
st.set_page_config(page_title="استوديو الذكاء الاصطناعي 2026", layout="wide")
st.title("🎨 AI-Creative-Studio-2026")

# --- الحصول على المفتاح من إعدادات النظام ---
# ملاحظة: إذا كنت تجرب على جهازك الشخصي، استبدل os.getenv بـ "توكن_الخاص_بك"
HF_TOKEN = os.getenv("HF_TOKEN") 

# رابط المحرك (سأختار لك أقوى موديل صور حالياً)
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        st.error(f"خطأ في الاتصال بالسحابة: {response.text}")
        return None
    return response.content

# --- واجهة المستخدم ---
with st.sidebar:
    st.header("إعدادات التصميم")
    style = st.selectbox("نمط الصورة", ["سينمائي", "واقعي", "رسم رقمي", "أنمي"])

prompt = st.text_area("أدخل وصف الصورة بالتفصيل (بالإنجليزي):", 
                     "A futuristic luxury car driving through a neon city at night, 8k, hyper-realistic.")

if st.button("توليد الصورة فوراً ✨"):
    if not HF_TOKEN:
        st.warning("تحذير: لم يتم العثور على مفتاح HF_TOKEN. تأكد من إضافته في Secrets.")
    else:
        with st.spinner("جاري التواصل مع الخوادم السحابية..."):
            image_bytes = query({"inputs": prompt})
            if image_bytes:
                image = Image.open(io.BytesIO(image_bytes))
                st.image(image, caption="تم التوليد بواسطة استوديو 2026", use_column_width=True)
                st.success("تم التوليد بنجاح في ثوانٍ!")
