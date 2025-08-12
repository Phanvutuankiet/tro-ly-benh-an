import streamlit as st
import google.generativeai as genai
# TỐI ƯU: Bỏ pyperclip và thêm thư viện mới
from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard

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

# --- KHỞI TẠO SESSION STATE ---
if "ket_qua_benh_an" not in st.session_state:
    st.session_state.ket_qua_benh_an = ""

def tao_prompt(data):
    """Tạo chuỗi prompt hoàn chỉnh từ dữ liệu bệnh nhân."""
    # (Giữ nguyên hàm tạo prompt của bạn)
    return f"""
    # -- BỐI CẢNH VÀ VAI TRÒ --
    Bạn là một bác sĩ nội trú cẩn thận và dày dạn kinh nghiệm...
    # ... (Toàn bộ prompt của bạn) ...
    - Họ và tên: {data['ho_ten']}
    - Tuổi: {data['tuoi']}
    # ...
    """

@st.cache_data(show_spinner=False)
def soan_thao_benh_an(_prompt):
    """Hàm gọi API Gemini để soạn bệnh án, kết quả sẽ được cache lại."""
    # (Giữ nguyên hàm gọi AI của bạn)
    try:
        model = genai.GenerativeModel('gemini-2.5-pro') 
        response = model.generate_content(_prompt)
        
        if response.text and response.text.strip():
            return response.text
        else:
            return "Lỗi: AI không trả về nội dung hợp lệ. Vui lòng thử lại."
    except Exception as e:
        return f"Đã có lỗi xảy ra khi kết nối tới AI: {e}"

# --- GIAO DIỆN NHẬP LIỆU ---
with st.form("benh_an_form"):
    # (Toàn bộ phần form nhập liệu giữ nguyên như cũ)
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
        st.session_state.ket_qua_benh_an = soan_thao_benh_an(final_prompt)

if st.session_state.ket_qua_benh_an:
    st.header("Bệnh án được AI soạn thảo:")
    
    # TỐI ƯU QUAN TRỌNG: Thay thế logic nút bấm cũ
    if "Lỗi:" not in st.session_state.ket_qua_benh_an:
        # Khi nút này được nhấn, nó sẽ gọi hàm copy_to_clipboard
        if st.button("Sao chép nội dung Bệnh án"):
            copy_to_clipboard(st.session_state.ket_qua_benh_an)
            st.success("Đã sao chép vào clipboard!")

    # Hiển thị nội dung bệnh án
    st.markdown(st.session_state.ket_qua_benh_an)
