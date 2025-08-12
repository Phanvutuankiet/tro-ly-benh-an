# services.py

import streamlit as st
import google.generativeai as genai
from constants import PROMPT_TEMPLATE

def configure_genai():
    """Cấu hình API key cho Google Generative AI."""
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        return True
    except Exception:
        st.error("Lỗi: Vui lòng thiết lập `GOOGLE_API_KEY` trong phần Secrets của Streamlit!")
        return False

def tao_prompt(data):
    """Tạo chuỗi prompt hoàn chỉnh từ dữ liệu bệnh nhân."""
    return PROMPT_TEMPLATE.format(**data)

@st.cache_data(show_spinner=False)
def soan_thao_benh_an(_prompt):
    """Hàm gọi API Gemini để soạn bệnh án, kết quả sẽ được cache lại."""
    try:
        model = genai.GenerativeModel('gemini-2.5-pro')
        response = model.generate_content(_prompt)
        
        if response.text and response.text.strip():
            return response.text
        else:
            return "Lỗi: AI không trả về nội dung hợp lệ. Vui lòng thử lại."
    except Exception as e:
        return f"Đã có lỗi xảy ra khi kết nối tới AI: {e}"