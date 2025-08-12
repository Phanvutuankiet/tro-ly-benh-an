import streamlit as st
import google.generativeai as genai
import pyperclip 

# --- CẤU HÌNH BAN ĐẦU ---
st.set_page_config(page_title="Trợ lý Soạn thảo Bệnh án", page_icon="🩺", layout="wide")
st.title("🩺 Trợ lý Soạn thảo Bệnh án")
st.write("Nhập thông tin bệnh nhân, AI sẽ giúp bạn soạn một bản nháp bệnh án hoàn chỉnh, có phân tích và biện luận.")

# --- THIẾT LẬP API KEY ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception:
    st.error("Lỗi: Vui lòng thiết lập `GOOGLE_API_KEY` trong phần Secrets của Streamlit để ứng dụng hoạt động!")
    st.stop()

# --- CẢI TIẾN 1: KHỞI TẠO SESSION STATE ---
# Giúp lưu lại kết quả bệnh án ngay cả khi người dùng thay đổi input
if "ket_qua_benh_an" not in st.session_state:
    st.session_state.ket_qua_benh_an = ""

def tao_prompt(data):
    """Tạo chuỗi prompt hoàn chỉnh từ dữ liệu bệnh nhân."""
    return f"""
    # -- BỐI CẢNH VÀ VAI TRÒ --
    Bạn là một bác sĩ nội trú cẩn thận và dày dạn kinh nghiệm, đang tiến hành biện luận để trình bày một bệnh án...
    # (Toàn bộ nội dung prompt của bạn ở đây)
    ...
    # -- DỮ LIỆU ĐẦU VÀO --
    - Họ và tên: {data['ho_ten']}
    - Tuổi: {data['tuoi']}
    - Giới tính: {data['gioi_tinh']}
    - Nghề nghiệp: {data['nghe_nghiep']}
    - Lý do vào viện: {data['ly_do_vao_vien']}
    - Bệnh sử: {data['benh_su']}
    - Tiền căn: {data['tien_can']}
    - Lược qua các cơ quan: {data['luoc_qua_cac_co_quan']}
    - Khám thực thể: {data['kham_thuc_the']}
    # ... (Phần còn lại của prompt)
    """

@st.cache_data(show_spinner=False)
def soan_thao_benh_an(_prompt):
    """Hàm gọi API Gemini để soạn bệnh án, kết quả sẽ được cache lại."""
    try:
        model = genai.GenerativeModel('gemini-2.5-pro') 
        response = model.generate_content(_prompt)
        # CẢI TIẾN 2: KIỂM TRA KẾT QUẢ TRẢ VỀ
        if response.text and response.text.strip():
            return response.text
        else:
            return "Lỗi: AI không trả về nội dung hợp lệ. Vui lòng thử lại."
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
        "benh_su": st.text_area("Bệnh sử", "Bệnh khởi phát cách đây 2 giờ..."),
        "tien_can": st.text_area("Tiền căn", "Tăng huyết áp 10 năm..."),
        "luoc_qua_cac_co_quan": st.text_area("Lược qua các cơ quan", "Hô hấp: không ho..."),
        "kham_thuc_the": st.text_area("Khám thực thể", "Sinh hiệu: Mạch 88..."),
    })

    submitted = st.form_submit_button("⚕️ Soạn thảo Bệnh án")

# --- XỬ LÝ VÀ HIỂN THỊ KẾT QUẢ ---
if submitted:
    final_prompt = tao_prompt(benh_nhan_data)
    with st.spinner("AI đang phân tích và soạn thảo, vui lòng chờ..."):
        # Cập nhật kết quả vào session_state
        st.session_state.ket_qua_benh_an = soan_thao_benh_an(final_prompt)

# Luôn hiển thị kết quả cuối cùng từ session_state
if st.session_state.ket_qua_benh_an:
    st.header("Bệnh án được AI soạn thảo:")
    st.markdown(st.session_state.ket_qua_benh_an)

    if "Lỗi:" not in st.session_state.ket_qua_benh_an:
        if st.button("Sao chép nội dung Bệnh án"):
            pyperclip.copy(st.session_state.ket_qua_benh_an)
            st.success("Đã sao chép vào clipboard!")
