import streamlit as st
import requests
import streamlit.components.v1 as components

# Вставляем мета-тег Google
components.html(
    """
    <meta name="google-site-verification" content="owjub_FtfLEQBfiFdVcgRRHYXT8unk_T9TGhLjNNfa4" />
    """,
    height=0
)

st.set_page_config(page_title="AI Detector Pro", page_icon="🤖")

st.title("🤖 Детектор ИИ-изображений")
st.write("Загрузи изображение, и я определю, создано ли оно нейросетью.")

uploaded_file = st.file_uploader("Выбери изображение...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='Загруженное фото', width=700)
    
    if st.button("Проверить"):
        st.write("Анализирую...")
        
        # Твои данные (не забудь убедиться, что они корректны)
        api_user = st.secrets["API_USER"]
        api_secret = st.secrets["API_SECRET"]


        # Подготовка файла
        image_bytes = uploaded_file.getvalue()
        files = {'media': ('image.jpg', image_bytes, 'image/jpeg')}
        data = {
            'models': 'genai',
            'api_user': api_user,
            'api_secret': api_secret
        }
        
        # Запрос к API
        response = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=data)
        result = response.json()
        
        # Вывод результата
        if 'type' in result and 'ai_generated' in result['type']:
            ai_score = result['type']['ai_generated']
            st.write(f"Вероятность ИИ: {ai_score * 100:.2f}%")
            
            if ai_score > 0.5:
                st.error("Это изображение создано ИИ!")
            else:
                st.success("Это похоже на работу человека.")
        else:
            st.error("Не удалось получить результат. Проверь настройки API.")
            st.write("Ответ сервера (для отладки):", result)