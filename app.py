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
    page_title="AI Detector Pro",
    page_icon="🤖",
    layout="centered"
)

# Стили
st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at top left, #7c3aed 0%, transparent 30%),
        radial-gradient(circle at bottom right, #2563eb 0%, transparent 30%),
        linear-gradient(135deg, #020617, #0f172a);
    color: white;
}

.block-container {
    max-width: 900px;
    padding-top: 2rem;
}

.hero {
    text-align: center;
    padding: 40px 20px;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 3.5rem;
    margin-bottom: 10px;
}

.hero p {
    color: #cbd5e1;
    font-size: 1.2rem;
}

.card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 25px;
    padding: 25px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}

.stButton > button {
    width: 100%;
    height: 60px;
    border: none;
    border-radius: 15px;
    font-size: 18px;
    font-weight: bold;
    color: white;
    background: linear-gradient(90deg,#7c3aed,#2563eb);
    transition: 0.3s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 30px rgba(124,58,237,0.6);
}

[data-testid="stFileUploader"] {
    border: 2px dashed rgba(255,255,255,0.2);
    border-radius: 20px;
    background: rgba(255,255,255,0.04);
    padding: 20px;
}

.result {
    text-align: center;
    margin-top: 20px;
    padding: 25px;
    border-radius: 20px;
    background: rgba(255,255,255,0.08);
}

.big-score {
    font-size: 60px;
    font-weight: bold;
    margin: 10px 0;
}

.footer {
    text-align: center;
    margin-top: 40px;
    color: #94a3b8;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# Заголовок
st.markdown("""
<div class="hero">
    <h1>🤖 AI Detector Pro</h1>
    <p>Проверь, создано ли изображение нейросетью</p>
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

            # Оставляем твои API данные
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
                        <h2>Вероятность генерации ИИ</h2>
                        <div class="big-score">{percent:.1f}%</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if ai_score > 0.5:
                    st.error("⚠️ Высока вероятность, что изображение создано нейросетью")
                else:
                    st.success("✅ Изображение похоже на настоящее фото")

            else:
                st.error("Не удалось получить результат")
                st.write(result)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
AI Detector Pro • Powered by SightEngine
</div>
""", unsafe_allow_html=True)