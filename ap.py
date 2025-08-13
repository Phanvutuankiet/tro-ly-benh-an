import streamlit as st
import google.generativeai as genai
import os

# --- CẤU HÌNH BAN ĐẦU ---
st.set_page_config(page_title="Trợ lý Soạn thảo Bệnh án", page_icon="🩺")
st.title("🩺 Trợ lý Soạn thảo Bệnh án")
st.write("Nhập thông tin bệnh nhân vào các ô bên dưới và AI sẽ giúp bạn soạn một bản nháp bệnh án.")

try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception:
    st.error("Vui lòng thiết lập GOOGLE_API_KEY trong phần Secrets của Streamlit để ứng dụng hoạt động!")
    st.stop()

# --- GIAO DIỆN NHẬP LIỆU ---
with st.form("benh_an_form"):
    st.header("1. Thông tin bệnh nhân")
    col1, col2, col3 = st.columns(3)
    with col1:
        ho_ten = st.text_input("Họ và tên", "Bệnh nhân A", help="Nhập họ tên hoặc mã số bệnh nhân.")
    with col2:
        tuoi = st.text_input("Tuổi", "52", help="Nhập tuổi của bệnh nhân.")
    with col3:
        gioi_tinh = st.selectbox("Giới tính", ["Nam", "Nữ", "Khác"])

    # THAY ĐỔI 1: Thêm ô nhập "Nghề nghiệp"
    nghe_nghiep = st.text_input("Nghề nghiệp", "Công nhân", help="Nhập nghề nghiệp hiện tại của bệnh nhân.")

    st.header("2. Thông tin y khoa")
    ly_do_vao_vien = st.text_area("Lý do vào viện", "Đau ngực trái dữ dội, khó thở.", help="Bạn có thể tự do chỉnh sửa hoặc xóa nội dung ví dụ trong ô này.")
    benh_su = st.text_area("Bệnh sử", "Bệnh khởi phát cách đây 2 giờ sau khi gắng sức, đau như bóp nghẹt sau xương ức, lan lên vai trái. Kèm vã mồ hôi, khó thở. Đã dùng 1 viên nitroglycerin ngậm dưới lưỡi nhưng không đỡ.", help="Bạn có thể tự do chỉnh sửa hoặc xóa nội dung ví dụ trong ô này.")
    tien_can = st.text_area("Tiền căn", "Tăng huyết áp 10 năm, đái tháo đường type 2, hút thuốc lá 20 gói-năm.", help="Bạn có thể tự do chỉnh sửa hoặc xóa nội dung ví dụ trong ô này.")
    luoc_qua_cac_co_quan = st.text_area("Lược qua các cơ quan", "Hô hấp: không ho, không khó thở. Tiêu hóa: ăn uống được, không đau bụng, tiêu tiểu bình thường. Thần kinh: không đau đầu, không yếu liệt. Cơ xương khớp: không đau mỏi.", help="Ghi nhận các triệu chứng ở các cơ quan khác.")
    kham_thuc_the = st.text_area("Khám thực thể", "Sinh hiệu: Mạch 88 lần/phút, Huyết áp 150/90 mmHg, Nhiệt độ 37°C, Nhịp thở 20 lần/phút. Khám tim: T1, T2 đều rõ, không âm thổi. Khám phổi: Rì rào phế nang êm dịu, không rale.", help="Ghi nhận các dấu hiệu khám thực thể tại giường.")

    submitted = st.form_submit_button("⚕️ Soạn thảo Bệnh án")

# --- XỬ LÝ VÀ HIỂN THỊ KẾT QUẢ ---
if submitted:
    # THAY ĐỔI 2: Cập nhật prompt với thông tin "Nghề nghiệp"
    prompt_template = f"""
    # -- BỐI CẢNH VÀ VAI TRÒ --
    Bạn là một bác sĩ nội trú cẩn thận và dày dạn kinh nghiệm, đang tiến hành biện luận để trình bày một bệnh án.
    Nhiệm vụ của bạn là nhận thông tin thô của bệnh nhân và cấu trúc lại thành một bệnh án hoàn chỉnh, logic và chuyên nghiệp.

    # -- NGUỒN KIẾN THỨC --
    Khi biện luận chẩn đoán và đề nghị cận lâm sàng, hãy dựa trên nền tảng kiến thức từ các nguồn y văn uy tín thế giới như Harrison's Principles of Internal Medicine, Cecil Medicine, và các hướng dẫn từ các tổ chức y tế như AHA, WHO, FDA, cũng như các nghiên cứu từ PubMed và The Lancet.

    # -- DỮ LIỆU ĐẦU VÀO --
    **Thông tin bệnh nhân:**
    - Họ và tên: {ho_ten}
    - Tuổi: {tuoi}
    - Giới tính: {gioi_tinh}
    - Nghề nghiệp: {nghe_nghiep}
    - Lý do vào viện: {ly_do_vao_vien}
    - Bệnh sử: {benh_su}
    - Tiền căn: {tien_can}
    - Lược qua các cơ quan: {luoc_qua_cac_co_quan}
    - Khám thực thể: {kham_thuc_the}

    # -- NHIỆM VỤ VÀ ĐỊNH DẠNG ĐẦU RA --
    **Yêu cầu thực hiện:**
    Dựa vào thông tin trên, hãy trình bày bệnh án theo đúng định dạng Markdown dưới đây.

    ### 1. PHẦN HÀNH CHÍNH
    (Điền thông tin hành chính của bệnh nhân, bao gồm cả nghề nghiệp)

    ### 2. LÝ DO VÀO VIỆN
    ### 3. BỆNH SỬ
    ### 4. TIỀN CĂN
    ### 5. LƯỢC QUA CÁC CƠ QUAN
    ### 6. KHÁM THỰC THỂ
    ### 7. TÓM TẮT BỆNH ÁN
    (Tóm tắt bệnh án qua vài dòng, nêu bật các hội chứng/triệu chứng chính từ các phần trên)

    ### 8. BIỆN LUẬN VÀ CHẨN ĐOÁN SƠ BỘ
    Để đưa ra chẩn đoán, hãy suy luận theo các bước sau:
    - **Phân tích triệu chứng:** Các triệu chứng cơ năng và thực thể chính của bệnh nhân là gì?
    - **Phân tích yếu tố nguy cơ:** Bệnh nhân có những yếu tố nguy cơ nào từ tiền căn và nghề nghiệp?
    - **Biện luận và Chẩn đoán sơ bộ:** Kết hợp các yếu tố trên và dựa vào kiến thức y văn, hãy biện luận để đưa ra chẩn đoán sơ bộ có khả năng nhất.

    ### 9. CHẨN ĐOÁN PHÂN BIỆT
    Dựa vào biện luận trên, hãy liệt kê các chẩn đoán phân biệt quan trọng cần được xem xét. Với mỗi chẩn đoán, hãy nêu ngắn gọn lý do tại sao nó được nghĩ đến và hướng để loại trừ.

    ### 10. ĐỀ NGHỊ CẬN LÂM SÀNG
    Đối với mỗi xét nghiệm được đề nghị, hãy ghi rõ mục đích của xét nghiệm đó để làm rõ chẩn đoán, dựa trên các hướng dẫn thực hành lâm sàng hiện hành.
    Ví dụ: '- ECG: Theo hướng dẫn của AHA, đây là xét nghiệm đầu tay để đánh giá đau ngực, tìm dấu hiệu thiếu máu cục bộ.'

    # -- QUY TẮC BẮT BUỘC --
    - Luôn giữ thái độ chuyên nghiệp, sử dụng thuật ngữ y khoa chính xác.
    - Chỉ suy luận dựa trên thông tin được cung cấp, không tự ý thêm thắt dữ liệu.
    """

    st.header("Bệnh án được AI soạn thảo:")
    with st.spinner("AI đang phân tích và soạn thảo, vui lòng chờ..."):
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt_template)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Đã có lỗi xảy ra khi kết nối tới AI: {e}")

