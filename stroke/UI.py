# Tên môn học: Thực Hành Học Máy
# Mã Học Phần: 010110104201
# Lớp Học Phần: 11DHTH10
# Giảng viên hướng dẫn: Trần Đình Toàn
# Nhóm: 1

# Đây là tất cả thư viện phục vụ cho ứng dụng dự đoán bệnh đột quỵ
import streamlit as st # : Thư viện streamlit cho phép tạo giao diện người dùng tương tác và hiển thị dữ liệu trong ứng dụng web.

# Thư viện pandas cung cấp các công cụ và cấu trúc dữ liệu để làm việc với dữ liệu dạng bảng.
# Ngoài ra còn cung cấp lớp DataFrame để đại diện cho dữ liệu dưới dạng bảng và cung cấp nhiều phương thức để thao tác và xử lý dữ liệu.
import pandas as pd 

# Thư viện numpy cung cấp các công cụ để làm việc với mảng và ma trận nhiều chiều trong Python. 
# Nó cung cấp các hàm số và phép toán tối ưu cho việc tính toán số học và xử lý dữ liệu.
import numpy as np

# tensorflow: Thư viện tensorflow là một thư viện mã nguồn mở để xây dựng và huấn luyện mạng neural. 
# Nó cung cấp các công cụ và lớp để tạo ra các mô hình học máy, thực hiện tính toán số và tối ưu hóa các mô hình.
import tensorflow as tf

# load_model là một hàm trong gói tensorflow.keras.models để tải mô hình đã được huấn luyện từ một tệp lưu trữ.
from tensorflow.keras.models import load_model

# LabelEncoder là một lớp trong gói sklearn.preprocessing để mã hoá các biến phân loại thành các giá trị số. 
# Nó sử dụng phương pháp mã hoá một đến một để ánh xạ mỗi giá trị duy nhất của biến đến một số nguyên duy nhất.
from sklearn.preprocessing import LabelEncoder

import pyodbc # Thư viện pyodbc để làm các thao tác với cơ sở dữ liệu

from PIL import Image

# Load mô hình đã được huấn luyện
# load_model() được sử dụng để tải mô hình đã được huấn luyện từ tệp.
model_path = "knn_modelss.pkl"  # Đường dẫn tới file mô hình đã tải xuống
model = load_model(model_path)

# Load dữ liệu huấn luyện
training_data = pd.read_csv("healthcare-dataset-stroke-data.csv")

# data_cleaned là bản sao của training_data sau khi loại bỏ các dòng chứa giá trị bị thiếu bằng cách sử dụng dropna().
# Cột 'id' cũng được loại bỏ bằng cách sử dụng drop() với tham số axis=1 để chỉ định loại bỏ theo cột.
data_cleaned = training_data.dropna()  # Remove rows with missing values
data_cleaned = data_cleaned.drop(['id'], axis=1)  # Drop unnecessary column 'id'

# Hàm label_encoder được viết để thực hiện quá trình mã hóa các nhãn (labels) thành các số nguyên duy nhất.
def label_encoder(labels):
    # unique_labels = list(set(labels)): Hàm này tạo ra một danh sách các giá trị duy nhất trong danh sách nhãn đầu vào bằng cách sử dụng set để loại bỏ các giá trị trùng lặp, 
    # sau đó chuyển đổi nó thành danh sách bằng list.
    unique_labels = list(set(labels))  # Tìm các giá trị duy nhất trong danh sách nhãn
    
    # Khởi tạo một từ điển rỗng có tên label_map. Đây là nơi chúng ta sẽ lưu trữ ánh xạ giữa giá trị nhãn và số.
    label_map = {}  # Tạo bản đồ ánh xạ giữa giá trị nhãn và số
    for i, label in enumerate(unique_labels):
        # label_map[label] = i: Trong mỗi lần lặp, hàm này thêm một cặp khóa-giá trị vào từ điển label_map, 
        # trong đó khóa là giá trị nhãn và giá trị tương ứng là chỉ số của nó trong danh sách các giá trị duy nhất.
        label_map[label] = i
    
    # Cuối cùng, hàm trả về từ điển label_map, trong đó chứa ánh xạ giữa giá trị nhãn và số tương ứng.
    return label_map

# Các hàm label_encoder() được sử dụng để mã hoá các biến phân loại thành các giá trị số.
# Các biến 'ever_married', 'gender', 'work_type', 'Residence_type', 'smoking_status' trong data_cleaned được mã hoá sử dụng các bộ mã hoá tương ứng.
ever_married_encoder = label_encoder(data_cleaned['ever_married'])
gender_encoder = label_encoder(data_cleaned['gender'])
work_type_encoder = label_encoder(data_cleaned['work_type'])
residence_type_encoder = label_encoder(data_cleaned['Residence_type'])
smoking_status_encoder = label_encoder(data_cleaned['smoking_status'])

# Hàm predict_stroke() được sử dụng để dự đoán nguy cơ bị đột quỵ dựa trên thông tin bệnh nhân đầu vào.
def predict_stroke(data):
    # Xử lý dữ liệu giống như khi huấn luyện mô hình
    gender = gender_encoder[data['gender']]
    ever_married = ever_married_encoder[data['ever_married']]
    work_type = work_type_encoder[data['work_type']]
    residence_type = residence_type_encoder[data['Residence_type']]
    smoking_status = smoking_status_encoder[data['smoking_status']]
    age = data['age']
    bmi= data['bmi']
    avg_glucose_level = data['avg_glucose_level']
    hypertension= data['hypertension']
    heart_disease= data['heart_disease']
    # Thông tin bệnh nhân được chuyển đổi sang các giá trị mã hoá tương ứng và được đặt vào danh sách X
    # X được chuyển đổi thành một tensor và được đưa vào mô hình để dự đoán.
    X = [[gender, age ,hypertension,heart_disease,ever_married,work_type,residence_type, avg_glucose_level, bmi,smoking_status]]

    # Dự đoán kết quả
    X_tensor = tf.convert_to_tensor(X, dtype=tf.float32)
    prediction = model.predict(X_tensor)
    print(prediction)
    # Dự đoán được chuyển đổi thành nhãn "Có Bệnh" hoặc "Không Bệnh" dựa trên một ngưỡng xác định.
    if prediction[0] > 0.1:
        result = 'Có Bệnh'
    else:
        result = 'Không Bệnh'
    return result

    #print(np.argmax(prediction))

def connect_to_database():
    # Kết nối đến cơ sở dữ liệu SQL Server
    connection_string = "DRIVER={SQL Server};SERVER=ADMIN-PC\SQLEXPRESS;DATABASE=dulieudotquy;UID=sa;PWD=123"
    conn = pyodbc.connect(connection_string)
    
    # Trả về kết nối
    return conn

def query_data():
    # Kết nối đến cơ sở dữ liệu
    conn = connect_to_database()
    
    # Tạo câu truy vấn SELECT
    query = "SELECT * FROM StrokePrediction"
    
    # Thực thi câu truy vấn và lấy dữ liệu
    data = pd.read_sql(query, conn)
    
    # Đóng kết nối
    conn.close()
    
    # Trả về dữ liệu
    return data

def save_prediction_to_table(conn, data):
    query = "INSERT INTO StrokePrediction (Gender, Age, Hypertension, HeartDisease, EverMarried, WorkType, ResidenceType, AvgGlucoseLevel, BMI, SmokingStatus, Result) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    cursor = conn.cursor()
    cursor.execute(query, data)
    conn.commit()

# Hiển thị các phần tử của trang dự đoán
def show_dudoan_page():
    st.markdown('<h1 class="noidung">Nhập thông tin bệnh nhân để dự đoán xem có nguy cơ bị đột quỵ hay không?</h1>', unsafe_allow_html=True)
    st.markdown(
    """
    <style>
    /* Căn giữa tiêu đề */
    .noidung {
        font-size: 20px;
        font-family: 'Times New Roman', sans-serif;
        color: #009966;
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    # Tạo các trường đầu vào cho người dùng nhập thông tin
    gender = st.selectbox('Giới tính', list(gender_encoder.keys()))
    age = st.number_input('Tuổi', min_value=0, max_value=120, value=30)
    hypertension = st.selectbox('Có bị tăng huyết áp không?', [1, 0])
    heart_disease = st.selectbox('Có bị bệnh tim không?', [1, 0])
    ever_married = st.selectbox('Đã kết hôn chưa?', list(ever_married_encoder.keys()))
    work_type = st.selectbox('Loại công việc', list(work_type_encoder.keys()))
    residence_type = st.selectbox('Loại nơi ở', list(residence_type_encoder.keys()))
    avg_glucose_level = st.number_input('Mức đường huyết trung bình', min_value=0.0, max_value=300.0, value=100.0)
    bmi = st.number_input('Chỉ số khối cơ thể (BMI)', min_value=0.0, max_value=100.0, value=25.0)
    smoking_status = st.selectbox('Tình trạng hút thuốc',  list(smoking_status_encoder.keys()))

    # Xử lý dự đoán khi người dùng nhấp vào nút "Dự đoán"
    if st.button('Dự đoán'):
        data = {
            'gender': gender,
            'age': age,
            'hypertension': hypertension,
            'heart_disease': heart_disease,
            'ever_married': ever_married,
            'work_type': work_type,
            'Residence_type': residence_type,
            'avg_glucose_level': avg_glucose_level,
            'bmi': bmi,
            'smoking_status': smoking_status,
        }
        result = predict_stroke(data)
        st.write("Kết quả dự đoán: ", result)
        conn = connect_to_database()
        data = (gender, age, hypertension, heart_disease, ever_married, work_type, residence_type, avg_glucose_level, bmi, smoking_status, result)
        save_prediction_to_table(conn, data)
        conn.close()
        # Hiển thị thông báo thành công
        st.success("Dữ liệu đã được lưu vào cơ sở dữ liệu SQL Server!")

# Hiển thị các phần tử của Trang Chủ
def show_TrangChu_page():
    st.markdown(
        """
        <style>
        /* Thay đổi font và màu cho tiêu đề */
        .title {
            font-size: 60px;
            font-family: 'Times New Roman', sans-serif;
            color: #000033;
        }
        /* Căn giữa tiêu đề */
        .centered-title {
            font-size: 30px;
            font-family: 'Times New Roman', sans-serif;
            color: #FF00FF;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .noidung {
            font-size: 25px;
            font-family: 'Times New Roman', sans-serif;
            color: #FF3366;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<h1 class="title">CHÀO MỪNG ĐẾN VỚI TRANG CHỦ</h1>', unsafe_allow_html=True)
    st.markdown('<h1 class="centered-title">CHỦ ĐỀ VỀ DỰ ĐOÁN BỆNH ĐỘT QUỴ</h1>', unsafe_allow_html=True)
    st.markdown('<h1 class="noidung">Tên môn học: Thực Hành Học Máy</h1>', unsafe_allow_html=True)
    st.markdown('<h1 class="noidung">Mã Học Phần: 010110104201</h1>', unsafe_allow_html=True)
    st.markdown('<h1 class="noidung">Lớp Học Phần: 11DHTH10</h1>', unsafe_allow_html=True)
    st.markdown('<h1 class="noidung">Giảng viên hướng dẫn: Trần Đình Toàn</h1>', unsafe_allow_html=True)
    st.markdown('<h1 class="noidung">Nhóm: 1</h1>', unsafe_allow_html=True)

# Hiển thị các phần tử của trang dữ liệu
def show_dulieu_page():
    st.markdown('<h1 class="title">THÔNG TIN DỮ LIỆU LIÊN QUAN TỚI BỆNH ĐỘT QUỴ</h1>', unsafe_allow_html=True)
    conn = connect_to_database()
    data = query_data()
    if st.button('Kết nối SQL Server'):
        if conn:
            st.success("Đã kết nối thành công đến SQL Server!")
            st.write(data) # Hiển thị dữ liệu
        else:
            st.warning("Kết nối thất bại đến SQL Server!")
    st.markdown(
        """
        <style>
        /* Thay đổi font và màu cho tiêu đề */
        .title {
            font-size: 40px;
            font-family: 'Time News Roman', sans-serif;
            color: #FF0000;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Giao diện người dùng với Streamlit
def main():
    st.sidebar.markdown("<h1 style='font-size: 34px; color: red;'>Trang Chủ</h1>", unsafe_allow_html=True)
    page = st.sidebar.radio("Các Chức Năng Chính", ("Trang Chủ", "Dự đoán","Dữ liệu"))
    if page == "Trang Chủ":
        show_TrangChu_page()
    elif page == "Dự đoán":
        show_dudoan_page()
    elif page == "Dữ liệu":
        show_dulieu_page()

      
if __name__ == '__main__':
    main()