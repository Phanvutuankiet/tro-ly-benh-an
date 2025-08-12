import streamlit as st
import google.generativeai as genai
import pyperclip # Thư viện để sao chép vào clipboard

# --- CẤU HÌNH BAN ĐẦU ---
st.set_page_config(page_title="Trợ lý Soạn thảo Bệnh án", page_icon="🩺", layout="wide")
st.title("🩺 Trợ lý Soạn thảo Bệnh án")
st.write("Nhập thông tin bệnh nhân, AI sẽ giúp bạn soạn một bản nháp bệnh án hoàn chỉnh, có phân tích và biện luận.")

# --- TỐI ƯU 1: Thiết lập API key một cách an toàn ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception:
    st.error("Lỗi: Vui lòng thiết lập `GOOGLE_API_KEY` trong phần Secrets của Streamlit để ứng dụng hoạt động!")
    st.stop()

# --- TỐI ƯU 2: Tách logic tạo prompt ra một hàm riêng để dễ quản lý ---
def tao_prompt(data):
    """Tạo chuỗi prompt hoàn chỉnh từ dữ liệu bệnh nhân."""
    return f"""
    # -- BỐI CẢNH VÀ VAI TRÒ --
    Bạn là một bác sĩ nội trú cẩn thận và dày dạn kinh nghiệm, đang tiến hành biện luận để trình bày một bệnh án.
    Nhiệm vụ của bạn là nhận thông tin thô của bệnh nhân và cấu trúc lại thành một bệnh án hoàn chỉnh, logic và chuyên nghiệp.

    # -- NGUỒN KIẾN THỨC --
    Khi biện luận chẩn đoán và đề nghị cận lâm sàng, hãy dựa trên nền tảng kiến thức từ các nguồn y văn uy tín thế giới như Harrison's Principles of Internal Medicine, Cecil Medicine, và các hướng dẫn từ các tổ chức y tế như AHA, WHO, FDA, cũng như các nghiên cứu từ PubMed và The Lancet.

    # -- DỮ LIỆU ĐẦU VÀO --
    **Thông tin bệnh nhân:**
    - Họ và tên: {data['ho_ten']}
    - Tuổi: {data['tuoi']}
    - Giới tính: {data['gioi_tinh']}
    - Nghề nghiệp: {data['nghe_nghiep']}
    - Lý do vào viện: {data['ly_do_vao_vien']}
    - Bệnh sử: {data['benh_su']}
    - Tiền căn: {data['tien_can']}
    - Lược qua các cơ quan: {data['luoc_qua_cac_co_quan']}
    - Khám thực thể: {data['kham_thuc_the']}

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

# --- TỐI ƯU 3: Dùng cache để lưu kết quả, tránh gọi API lặp lại ---
@st.cache_data(show_spinner=False) # Ẩn spinner mặc định của cache
def soan_thao_benh_an(_prompt):
    """Hàm gọi API Gemini để soạn bệnh án, kết quả sẽ được cache lại."""
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest') # Sử dụng model mới để có kết quả tốt hơn
        response = model.generate_content(_prompt)
        return response.text
    except Exception as e:
        return f"Đã có lỗi xảy ra khi kết nối tới AI: {e}"

# --- GIAO DIỆN NHẬP LIỆU ---
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
        "luoc_qua_cac_co_quan": st.text_area("Lược qua các cơ quan", "Hô hấp: không ho. Tiêu hóa: ăn uống được, không đau bụng. Thần kinh: không đau đầu."),
        "kham_thuc_the": st.text_area("Khám thực thể", "Sinh hiệu: Mạch 88 lần/phút, Huyết áp 150/90 mmHg, Nhiệt độ 37°C, Nhịp thở 20 lần/phút. Tim: T1, T2 đều rõ. Phổi: Rì rào phế nang êm dịu."),
    })

    submitted = st.form_submit_button("⚕️ Soạn thảo Bệnh án")

# --- XỬ LÝ VÀ HIỂN THỊ KẾT QUẢ ---
if submitted:
    # Tạo prompt từ dữ liệu đã thu thập
    final_prompt = tao_prompt(benh_nhan_data)
    
    st.header("Bệnh án được AI soạn thảo:")
    with st.spinner("AI đang phân tích và soạn thảo, vui lòng chờ..."):
        # Gọi hàm đã được cache
        ket_qua_benh_an = soan_thao_benh_an(final_prompt)
        
        # Hiển thị kết quả
        st.markdown(ket_qua_benh_an)

        # --- TỐI ƯU 4: Thêm nút sao chép kết quả ---
        if "Đã có lỗi xảy ra" not in ket_qua_benh_an:
            if st.button("Sao chép nội dung Bệnh án"):
                pyperclip.copy(ket_qua_benh_an)
                st.success("Đã sao chép vào clipboard!")
