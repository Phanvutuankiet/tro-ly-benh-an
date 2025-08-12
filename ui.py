# ui.py

import streamlit as st
from streamlit_js_eval import copy_to_clipboard

def render_form():
    """Vẽ form nhập liệu và trả về dữ liệu khi người dùng nhấn submit."""
    with st.form("benh_an_form"):
        st.header("1. Thông tin bệnh nhân")
        col1, col2, col3 = st.columns(3)
        benh_nhan_data = {
            "ho_ten": col1.text_input("Họ và tên", "Bệnh nhân A"),
            "tuoi": col2.text_input("Tuổi", "52"),
            "gioi_tinh": col3.selectbox("Giới tính", ["Nam", "Nữ", "Khác"]),
            "nghe_nghiep": st.text_input("Nghề nghiệp", "Công nhân"),
        }

        st.header("2. Thông tin y khoa")
        benh_nhan_data.update({
            "ly_do_vao_vien": st.text_area("Lý do vào viện", "Đau ngực trái dữ dội, khó thở."),
            "benh_su": st.text_area("Bệnh sử", "Bệnh khởi phát cách đây 2 giờ..."),
            "tien_can": st.text_area("Tiền căn", "Tăng huyết áp 10 năm..."),
            "luoc_qua_cac_co_quan": st.text_area("Lược qua các cơ quan", "Hô hấp: không ho..."),
            "kham_thuc_the": st.text_area("Khám thực thể", "Sinh hiệu: Mạch 88..."),
        })

        submitted = st.form_submit_button("⚕️ Soạn thảo Bệnh án")
        if submitted:
            return benh_nhan_data
    return None

def render_results():
    """Hiển thị kết quả bệnh án và nút sao chép."""
    if st.session_state.ket_qua_benh_an:
        st.header("Bệnh án được AI soạn thảo:")
        
        if "Lỗi:" not in st.session_state.ket_qua_benh_an:
            if st.button("Sao chép nội dung Bệnh án"):
                copy_to_clipboard(st.session_state.ket_qua_benh_an)
                st.success("Đã sao chép vào clipboard!")

        st.markdown(st.session_state.ket_qua_benh_an)