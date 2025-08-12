# ui.py

import streamlit as st
# THAY ĐỔI: Import thêm hàm 'button_did_it_work'
from streamlit_js_eval import copy_to_clipboard, button_did_it_work

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
            "benh_su": st.text_area("Bệnh sử", "Bệnh khởi phát cách đây 2 giờ sau khi gắng sức, đau như bóp nghẹt sau xương ức, lan lên vai trái. Kèm vã mồ hôi, khó thở. Đã dùng 1 viên nitroglycerin ngậm dưới lưỡi nhưng không đỡ."),
            "tien_can": st.text_area("Tiền căn", "Tăng huyết áp 10 năm, đái tháo đường type 2, hút thuốc lá 20 gói-năm."),
            "luoc_qua_cac_co_quan": st.text_area("Lược qua các cơ quan", "Hô hấp: không ho, không khó thở. Tiêu hóa: ăn uống được, không đau bụng, tiêu tiểu bình thường. Thần kinh: không đau đầu, không yếu liệt. Cơ xương khớp: không đau mỏi."),
            "kham_thuc_the": st.text_area("Khám thực thể", "Sinh hiệu: Mạch 88 lần/phút, Huyết áp 150/90 mmHg, Nhiệt độ 37°C, Nhịp thở 20 lần/phút. Khám tim: T1, T2 đều rõ, không âm thổi. Khám phổi: Rì rào phế nang êm dịu, không rale."),
        })

        submitted = st.form_submit_button("⚕️ Soạn thảo Bệnh án")
        if submitted:
            return benh_nhan_data
    return None

def render_results():
    """Hiển thị kết quả bệnh án và nút sao chép."""
    if st.session_state.get("ket_qua_benh_an"):
        st.header("Bệnh án được AI soạn thảo:")
        
        if "Lỗi:" not in st.session_state.ket_qua_benh_an:
            # THAY ĐỔI: Thêm một key định danh cho nút bấm
            st.button("Sao chép nội dung Bệnh án", key="copy_button")
            
            # THAY ĐỔI: Dùng hàm mới để kiểm tra và thực hiện sao chép
            if button_did_it_work("copy_button"):
                copy_to_clipboard(st.session_state.ket_qua_benh_an)
                st.success("Đã sao chép vào clipboard!")

        st.markdown(st.session_state.ket_qua_benh_an)
