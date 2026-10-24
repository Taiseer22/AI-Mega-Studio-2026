import streamlit as st
import requests
from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageDraw
from io import BytesIO
import urllib.parse, random

st.set_page_config(page_title="Anannan Studio", page_icon="✨", layout="wide")
st.markdown("<style>.stApp{background:#0a0a0a;color:#eee} .stButton>button{background:#fff;color:#000;border-radius:10px;height:48px;font-weight:bold} .stButton>button:hover{background:#eee}</style>", unsafe_allow_html=True)

if 'gallery' not in st.session_state: st.session_state.gallery=[]

st.title("Anannan Studio")
st.caption("Image Generator & Editor")

tab1, tab2, tab3 = st.tabs(["Generate", "Edit", "Gallery"])

with tab1:
    prompt = st.text_area("Prompt", "a beautiful photo, ultra-detailed, 8k", height=80, label_visibility="collapsed", placeholder="Describe anything...")
    if st.button("Generate", use_container_width=True):
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=1024&height=1024&model=flux&seed={random.randint(1,9999999)}&nologo=true&enhance=true"
        r = requests.get(url, timeout=90)
        if r.status_code==200:
            img = Image.open(BytesIO(r.content)).convert("RGB")
            st.image(img, use_container_width=True)
            st.session_state.gallery.append(img)

with tab2:
    uploaded = st.file_uploader("Upload any image", type=["jpg","jpeg","png","webp"], label_visibility="collapsed")
    
    if uploaded:
        orig = Image.open(uploaded).convert("RGB")
        st.image(orig, use_container_width=True)
        
        st.divider()
        
        tool = st.radio("Tools", ["Enhance", "Filters", "Resize", "Transform"], horizontal=True, label_visibility="collapsed")
        
        result = None
        
        if tool == "Enhance":
            c1,c2,c3,c4 = st.columns(4)
            sharp = c1.slider("Sharp", 0.0, 3.0, 1.0)
            color = c2.slider("Color", 0.0, 3.0, 1.0)
            bright = c3.slider("Light", 0.5, 2.0, 1.0)
            contrast = c4.slider("Contrast", 0.5, 2.0, 1.0)
            
            if st.button("Apply", key="enh"):
                img = orig.copy()
                img = ImageEnhance.Sharpness(img).enhance(sharp)
                img = ImageEnhance.Color(img).enhance(color)
                img = ImageEnhance.Brightness(img).enhance(bright)
                img = ImageEnhance.Contrast(img).enhance(contrast)
                result = img
            
            col_fix = st.columns(2)
            if col_fix[0].button("Auto Fix", use_container_width=True):
                img = orig.copy()
                img = ImageEnhance.Sharpness(img).enhance(1.5)
                img = ImageEnhance.Contrast(img).enhance(1.2)
                img = ImageEnhance.Color(img).enhance(1.2)
                img = img.filter(ImageFilter.UnsharpMask(radius=1.2, percent=150, threshold=2))
                result = img
            if col_fix[1].button("Denoise", use_container_width=True):
                result = orig.filter(ImageFilter.MedianFilter(3))

        elif tool == "Filters":
            effect = st.selectbox("Filter", ["None","Cinematic","Vintage","HDR","B&W","Sepia","Vivid","Warm","Cold","Cartoon","Oil Paint","Blur","Golden"], label_visibility="collapsed")
            intensity = st.slider("Strength", 0.0, 1.0, 0.5)
            
            if st.button("Apply Filter", key="filt"):
                img = orig.copy()
                if effect == "Cinematic":
                    overlay = Image.new("RGB", img.size, (20,10,40))
                    img = Image.blend(img, overlay, intensity*0.3)
                    img = ImageEnhance.Contrast(img).enhance(1.3)
                elif effect == "Vintage":
                    img = ImageEnhance.Color(img).enhance(0.6)
                    overlay = Image.new("RGB", img.size, (200,180,120))
                    img = Image.blend(img, overlay, intensity*0.4)
                elif effect == "HDR":
                    img = ImageEnhance.Contrast(img).enhance(1.5)
                    img = ImageEnhance.Sharpness(img).enhance(2.0)
                    img = ImageEnhance.Color(img).enhance(1.4)
                elif effect == "B&W":
                    img = ImageOps.grayscale(img).convert("RGB")
                elif effect == "Sepia":
                    img = ImageOps.grayscale(img).convert("RGB")
                    overlay = Image.new("RGB", img.size, (150,100,50))
                    img = Image.blend(img, overlay, 0.6)
                elif effect == "Vivid":
                    img = ImageEnhance.Color(img).enhance(2.2)
                elif effect == "Warm":
                    overlay = Image.new("RGB", img.size, (255,180,50))
                    img = Image.blend(img, overlay, intensity*0.3)
                elif effect == "Cold":
                    overlay = Image.new("RGB", img.size, (50,100,255))
                    img = Image.blend(img, overlay, intensity*0.2)
                elif effect == "Cartoon":
                    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
                    img = ImageEnhance.Color(img).enhance(1.8)
                elif effect == "Oil Paint":
                    img = img.filter(ImageFilter.GaussianBlur(1))
                    img = ImageEnhance.Color(img).enhance(1.5)
                elif effect == "Blur":
                    img = img.filter(ImageFilter.GaussianBlur(intensity*5))
                elif effect == "Golden":
                    overlay = Image.new("RGB", img.size, (255,180,50))
                    img = Image.blend(img, overlay, intensity*0.25)
                    img = ImageEnhance.Brightness(img).enhance(1.1)
                result = img

        elif tool == "Resize":
            c1,c2 = st.columns(2)
            new_w = c1.number_input("W", 100, 4000, orig.width)
            new_h = c2.number_input("H", 100, 4000, orig.height)
            method = st.selectbox("Method", ["Stretch","Smart Fill","White Frame","Mosaic"])
            
            if st.button("Resize", key="res"):
                if method == "Stretch":
                    result = orig.resize((new_w, new_h), Image.LANCZOS)
                elif method == "Smart Fill":
                    bg = orig.resize((new_w, new_h)).filter(ImageFilter.GaussianBlur(25))
                    x = (new_w - orig.width)//2
                    y = (new_h - orig.height)//2
                    if x>=0 and y>=0: bg.paste(orig, (x,y))
                    result = bg
                elif method == "White Frame":
                    result = ImageOps.expand(orig, border=40, fill="white")
                    result = result.resize((new_w, new_h), Image.LANCZOS)
                else:
                    result = ImageOps.fit(orig, (new_w, new_h), method=Image.LANCZOS)

        else: # Transform
            rot = st.slider("Rotate", -180, 180, 0)
            flip = st.selectbox("Flip", ["None","Horizontal","Vertical"])
            txt = st.text_input("Text (optional)", placeholder="Add text...")
            
            if st.button("Apply Transform", key="trans"):
                img = orig.rotate(rot, expand=True)
                if flip=="Horizontal": img = ImageOps.mirror(img)
                if flip=="Vertical": img = ImageOps.flip(img)
                if txt:
                    draw = ImageDraw.Draw(img)
                    draw.rectangle([(10, img.height-60),(img.width-10, img.height-10)], fill=(0,0,0))
                    draw.text((20, img.height-50), txt, fill=(255,255,255))
                result = img

        if result is not None:
            st.divider()
            st.image(result, use_container_width=True)
            buf = BytesIO(); result.save(buf, format="PNG")
            col1,col2 = st.columns(2)
            col1.download_button("Download", buf.getvalue(), f"edit_{random.randint(1,9999)}.png", "image/png", use_container_width=True)
            if col2.button("Add to Gallery", use_container_width=True):
                st.session_state.gallery.append(result)

with tab3:
    if st.session_state.gallery:
        cols = st.columns(3)
        for i, im in enumerate(reversed(st.session_state.gallery)):
            with cols[i%3]:
                st.image(im, use_container_width=True)
    else:
        st.caption("No images yet")

st.caption("© Anannan Studio")