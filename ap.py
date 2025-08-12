# app.py

import streamlit as st
from ui import render_form, render_results
from services import configure_genai, tao_prompt, soan_thao_benh_an

def main():
    """Hàm chính điều phối toàn bộ ứng dụng."""
    # --- CẤU HÌNH BAN ĐẦU ---
    st.set_page_config(page_title="Trợ lý Soạn thảo Bệnh án", page_icon="🩺", layout="wide")
    st.title("🩺 Trợ lý Soạn thảo Bệnh án")
    st.write("Nhập thông tin bệnh nhân, AI sẽ giúp bạn soạn một bản nháp bệnh án.")

    # --- KIỂM TRA API KEY ---
    if not configure_genai():
        st.stop()

    # --- KHỞI TẠO SESSION STATE ---
    if "ket_qua_benh_an" not in st.session_state:
        st.session_state.ket_qua_benh_an = ""

    # --- VẼ GIAO DIỆN VÀ LẤY DỮ LIỆU ---
    user_data = render_form()
    
    # --- XỬ LÝ DỮ LIỆU VÀ GỌI AI ---
    if user_data:
        final_prompt = tao_prompt(user_data)
        with st.spinner("AI đang phân tích và soạn thảo, vui lòng chờ..."):
            st.session_state.ket_qua_benh_an = soan_thao_benh_an(final_prompt)
    
    # --- HIỂN THỊ KẾT QUẢ ---
    render_results()

if __name__ == "__main__":
    main()
