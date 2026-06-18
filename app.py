import streamlit as st
import requests
import streamlit.components.v1 as components

# Google verification
components.html(
    """
    <meta name="google-site-verification" content="owjub_FtfLEQBfiFdVcgRRHYXT8unk_T9TGhLjNNfa4" />
    """,
    height=0
)

st.set_page_config(
    page_title="Kasym AI",
    page_icon="🤖",
    layout="centered"
)

# ===================== PREMIUM UI =====================
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap" rel="stylesheet">

<style>

/* GLOBAL */
html, body, .stApp {
    font-family: 'Inter', sans-serif;
    color: white;
}

/* animated background */
.stApp {
    background: radial-gradient(circle at 10% 10%, rgba(124,58,237,0.35), transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(37,99,235,0.35), transparent 45%),
                radial-gradient(circle at 50% 50%, rgba(16,185,129,0.12), transparent 60%),
                linear-gradient(135deg, #020617, #0b1220);
    overflow-x: hidden;
}

/* soft glow animation */
.stApp::before {
    content: "";
    position: fixed;
    width: 600px;
    height: 600px;
    background: rgba(124,58,237,0.25);
    filter: blur(120px);
    top: -200px;
    left: -200px;
    z-index: -1;
    animation: floatGlow 10s infinite alternate;
}

@keyframes floatGlow {
    from { transform: translateY(0px) translateX(0px); }
    to { transform: translateY(80px) translateX(60px); }
}

.block-container {
    max-width: 950px;
    padding-top: 2rem;
}

/* HERO */
.hero {
    text-align: center;
    padding: 60px 20px 30px 20px;
}

.hero h1 {
    font-size: 4rem;
    font-weight: 800;
    background: linear-gradient(90deg, #7c3aed, #2563eb, #22c55e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
    letter-spacing: -1px;
}

.hero p {
    color: #cbd5e1;
    font-size: 1.25rem;
    opacity: 0.9;
}

/* GLASS CARD */
.card {
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(25px);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 28px;
    padding: 30px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    transition: 0.3s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 25px 80px rgba(124,58,237,0.25);
}

/* BUTTON */
.stButton > button {
    width: 100%;
    height: 62px;
    border: none;
    border-radius: 16px;
    font-size: 18px;
    font-weight: 700;
    color: white;
    background: linear-gradient(90deg,#7c3aed,#2563eb);
    transition: all 0.3s ease;
    box-shadow: 0 10px 30px rgba(124,58,237,0.3);
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.01);
    box-shadow: 0 0 40px rgba(124,58,237,0.6);
}

/* FILE UPLOADER */
[data-testid="stFileUploader"] {
    border: 2px dashed rgba(255,255,255,0.25);
    border-radius: 22px;
    background: rgba(255,255,255,0.03);
    padding: 25px;
    transition: 0.3s ease;
}

[data-testid="stFileUploader"]:hover {
    border-color: rgba(124,58,237,0.7);
    background: rgba(124,58,237,0.05);
}

/* RESULT BOX */
.result {
    text-align: center;
    margin-top: 25px;
    padding: 30px;
    border-radius: 24px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}

.big-score {
    font-size: 72px;
    font-weight: 800;
    background: linear-gradient(90deg,#22c55e,#2563eb,#7c3aed);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 15px 0;
}

/* FOOTER */
.footer {
    text-align: center;
    margin-top: 50px;
    color: #94a3b8;
    font-size: 13px;
    opacity: 0.7;
}

</style>
""", unsafe_allow_html=True)

# ===================== HERO =====================
st.markdown("""
<div class="hero">
    <h1>🤖 Kasym AI </h1>
    <p>Определи, создано ли изображение искусственным интеллектом</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Загрузите изображение",
    type=["jpg", "jpeg", "png"]
)


if uploaded_file is not None:

    st.image(
        uploaded_file,
        caption="Загруженное изображение",
        use_container_width=True
    )

    if st.button("🔍 Проверить изображение"):

        with st.spinner("Анализирую изображение..."):

            api_user = st.secrets["API_USER"]
            api_secret = st.secrets["API_SECRET"]

            image_bytes = uploaded_file.getvalue()

            files = {
                'media': (
                    'image.jpg',
                    image_bytes,
                    'image/jpeg'
                )
            }

            data = {
                'models': 'genai',
                'api_user': api_user,
                'api_secret': api_secret
            }

            response = requests.post(
                'https://api.sightengine.com/1.0/check.json',
                files=files,
                data=data
            )

            result = response.json()

            if 'type' in result and 'ai_generated' in result['type']:

                ai_score = result['type']['ai_generated']
                percent = ai_score * 100

                st.markdown(
                    f"""
                    <div class="result">
                        <h2>Результат анализа</h2>
                        <div class="big-score">{percent:.1f}%</div>
                        <p>Вероятность генерации ИИ</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if ai_score > 0.5:
                    st.error("⚠️ Высокая вероятность ИИ-генерации")
                else:
                    st.success("✅ Похоже на реальное изображение")

            else:
                st.error("Не удалось получить результат")
                st.write(result)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
AI Detector Pro • Powered by SightEngine
</div>
""", unsafe_allow_html=True)


