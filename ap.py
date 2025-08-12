import streamlit as st
import google.generativeai as genai
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
    # (Gi-ữ nguyên hàm gọi AI của bạn)
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
    st.header("1. Thông tin bệnh nhân")
    col1, col2, col3 = st.columns(3)
    benh_nhan_data = {
        "ho_ten": col1.text_input("Họ và tên", "Bệnh nhân A"),
        "tuoi": col2.text_input("Tuổi", "52"),
        "gioi_tinh": col3.selectbox("Giới tính", ["Nam", "Nữ", "Khác"]),
        "nghe_nghiep": st.text_input("Nghề nghiệp", "Công nhân"),
    }

    st.header("2. Thông tin y khoa")
    # **KHÔI PHỤC LẠI NỘI DUNG GIỚI THIỆU CHI TIẾT**
    benh_nhan_data.update({
        "ly_do_vao_vien": st.text_area("Lý do vào viện", "Đau ngực trái dữ dội, khó thở."),
        "benh_su": st.text_area("Bệnh sử", "Bệnh khởi phát cách đây 2 giờ sau khi gắng sức, đau như bóp nghẹt sau xương ức, lan lên vai trái. Kèm vã mồ hôi, khó thở. Đã dùng 1 viên nitroglycerin ngậm dưới lưỡi nhưng không đỡ."),
        "tien_can": st.text_area("Tiền căn", "Tăng huyết áp 10 năm, đái tháo đường type 2, hút thuốc lá 20 gói-năm."),
        "luoc_qua_cac_co_quan": st.text_area("Lược qua các cơ quan", "Hô hấp: không ho, không khó thở. Tiêu hóa: ăn uống được, không đau bụng, tiêu tiểu bình thường. Thần kinh: không đau đầu, không yếu liệt. Cơ xương khớp: không đau mỏi."),
        "kham_thuc_the": st.text_area("Khám thực thể", "Sinh hiệu: Mạch 88 lần/phút, Huyết áp 150/90 mmHg, Nhiệt độ 37°C, Nhịp thở 20 lần/phút. Khám tim: T1, T2 đều rõ, không âm thổi. Khám phổi: Rì rào phế nang êm dịu, không rale."),
    })
    submitted = st.form_submit_button("⚕️ Soạn thảo Bệnh án")

# --- XỬ LÝ VÀ HIỂN THỊ KẾT QUẢ ---
if submitted:
    final_prompt = tao_prompt(benh_nhan_data)
    with st.spinner("AI đang phân tích và soạn thảo, vui lòng chờ..."):
        st.session_state.ket_qua_benh_an = soan_thao_benh_an(final_prompt)

if st.session_state.ket_qua_benh_an:
    st.header("Bệnh án được AI soạn thảo:")
    
    if "Lỗi:" not in st.session_state.ket_qua_benh_an:
        if st.button("Sao chép nội dung Bệnh án"):
            copy_to_clipboard(st.session_state.ket_qua_benh_an)
            st.success("Đã sao chép vào clipboard!")

    st.markdown(st.session_state.ket_qua_benh_an)
