import streamlit as st
import google.generativeai as genai
import os

# --- CẤU HÌNH BAN ĐẦU ---

# Thiết lập tiêu đề cho trang web
st.set_page_config(page_title="Trợ lý Soạn thảo Bệnh án", page_icon="🩺")

st.title("🩺 Trợ lý Soạn thảo Bệnh án")
st.write("Nhập thông tin bệnh nhân vào các ô bên dưới và AI sẽ giúp bạn soạn một bản nháp bệnh án.")

# Cấu hình API key của Google (Lấy từ Google AI Studio)
# Bạn nên lưu API key vào Streamlit secrets để bảo mật
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception:
    st.error("Vui lòng thiết lập GOOGLE_API_KEY trong phần Secrets của Streamlit để ứng dụng hoạt động!")
    st.stop()


# --- GIAO DIỆN NHẬP LIỆU ---

# Sử dụng st.form để nhóm các ô nhập liệu và chỉ gửi khi nhấn nút
with st.form("benh_an_form"):
    st.header("1. Thông tin bệnh nhân")

    # Sử dụng cột để giao diện gọn gàng hơn
    col1, col2, col3 = st.columns(3)
    with col1:
        ho_ten = st.text_input("Họ và tên", "Bệnh nhân A")
    with col2:
        tuoi = st.text_input("Tuổi", "52")
    with col3:
        gioi_tinh = st.selectbox("Giới tính", ["Nam", "Nữ", "Khác"])

    st.header("2. Thông tin y khoa")
    ly_do_vao_vien = st.text_area("Lý do vào viện", "Đau ngực trái dữ dội, khó thở.")
    benh_su = st.text_area("Bệnh sử", "Bệnh khởi phát cách đây 2 giờ sau khi gắng sức, đau như bóp nghẹt sau xương ức, lan lên vai trái. Kèm vã mồ hôi, khó thở. Đã dùng 1 viên nitroglycerin ngậm dưới lưỡi nhưng không đỡ.")
    tien_su = st.text_area("Tiền sử", "Tăng huyết áp 10 năm, đái tháo đường type 2, hút thuốc lá 20 gói-năm.")

    # Nút bấm để gửi toàn bộ thông tin
    submitted = st.form_submit_button("⚕️ Soạn thảo Bệnh án")


# --- XỬ LÝ VÀ HIỂN THỊ KẾT QUẢ ---

if submitted:
    # 1. Tạo câu lệnh (prompt) chi tiết cho AI
    prompt_template = f"""
    Bạn là một trợ lý y khoa chuyên nghiệp. Dựa vào các thông tin được cung cấp dưới đây, hãy soạn thảo một bản nháp bệnh án hoàn chỉnh theo đúng cấu trúc y khoa của Việt Nam.

    **Thông tin đầu vào:**
    - Họ và tên: {ho_ten}
    - Tuổi: {tuoi}
    - Giới tính: {gioi_tinh}
    - Lý do vào viện: {ly_do_vao_vien}
    - Bệnh sử: {benh_su}
    - Tiền sử: {tien_su}

    **Yêu cầu:**
    Hãy trình bày kết quả dưới dạng một bệnh án có các mục sau:
    1. PHẦN HÀNH CHÍNH
    2. LÝ DO VÀO VIỆN
    3. BỆNH SỬ
    4. TIỀN SỬ
    5. TÓM TẮT BỆNH ÁN (Tự động tóm tắt từ các thông tin trên)
    6. CHẨN ĐOÁN SƠ BỘ (Dựa vào thông tin để đưa ra chẩn đoán có khả năng nhất)
    7. CẬN LÂM SÀNG ĐỀ NGHỊ (Gợi ý các xét nghiệm cần làm)
    """

    # 2. Gọi API của Gemini và hiển thị kết quả
    st.header("Bệnh án được AI soạn thảo:")
    with st.spinner("AI đang phân tích và soạn thảo, vui lòng chờ..."):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            response = model.generate_content(prompt_template)
            st.markdown(response.text)
        except Exception as e:

            st.error(f"Đã có lỗi xảy ra khi kết nối tới AI: {e}")
