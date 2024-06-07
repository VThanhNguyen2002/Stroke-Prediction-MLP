import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
import pyodbc
import os

# Ensure the temporary directory exists
if not os.path.exists("tempDir"):
    os.makedirs("tempDir")

# Function to save the uploaded file to a temporary location
def save_uploadedfile(uploadedfile):
    with open(os.path.join("tempDir", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    return os.path.join("tempDir", uploadedfile.name)

# UI for uploading model file
uploaded_model_file = st.file_uploader("Tải lên tệp mô hình (.h5)", type="h5")
if uploaded_model_file is not None:
    model_path = save_uploadedfile(uploaded_model_file)
    model = load_model(model_path)
    st.success("Đã tải thành công mô hình từ tệp được tải lên.")

# UI for uploading training data file
uploaded_data_file = st.file_uploader("Tải lên tệp dữ liệu huấn luyện (.csv)", type="csv")
if uploaded_data_file is not None:
    data_path = save_uploadedfile(uploaded_data_file)
    training_data = pd.read_csv(data_path)
    st.success("Đã tải thành công dữ liệu huấn luyện từ tệp được tải lên.")

# Ensure training data is loaded before proceeding
if 'training_data' not in locals():
    st.error("Vui lòng tải lên tệp dữ liệu huấn luyện để tiếp tục.")
else:
    data_cleaned = training_data.dropna()  # Remove rows with missing values
    data_cleaned = data_cleaned.drop(['id'], axis=1)  # Drop unnecessary column 'id'

    def label_encoder(labels):
        unique_labels = list(set(labels))
        label_map = {label: i for i, label in enumerate(unique_labels)}
        return label_map

    ever_married_encoder = label_encoder(data_cleaned['ever_married'])
    gender_encoder = label_encoder(data_cleaned['gender'])
    work_type_encoder = label_encoder(data_cleaned['work_type'])
    residence_type_encoder = label_encoder(data_cleaned['Residence_type'])
    smoking_status_encoder = label_encoder(data_cleaned['smoking_status'])

    def predict_stroke(data):
        gender = gender_encoder[data['gender']]
        ever_married = ever_married_encoder[data['ever_married']]
        work_type = work_type_encoder[data['work_type']]
        residence_type = residence_type_encoder[data['Residence_type']]
        smoking_status = smoking_status_encoder[data['smoking_status']]
        age = data['age']
        bmi = data['bmi']
        avg_glucose_level = data['avg_glucose_level']
        hypertension = data['hypertension']
        heart_disease = data['heart_disease']
        X = [[gender, age, hypertension, heart_disease, ever_married, work_type, residence_type, avg_glucose_level, bmi, smoking_status]]

        X_tensor = tf.convert_to_tensor(X, dtype=tf.float32)
        prediction = model.predict(X_tensor)
        result = 'Có Bệnh' if prediction[0] > 0.1 else 'Không Bệnh'
        return result

    def connect_to_database():
        connection_string = "DRIVER={SQL Server};SERVER=ADMIN-PC\\SQLEXPRESS;DATABASE=dulieudotquy;UID=sa;PWD=123"
        conn = pyodbc.connect(connection_string)
        return conn

    def query_data():
        conn = connect_to_database()
        query = "SELECT * FROM StrokePrediction"
        data = pd.read_sql(query, conn)
        conn.close()
        return data

    def save_prediction_to_table(conn, data):
        query = "INSERT INTO StrokePrediction (Gender, Age, Hypertension, HeartDisease, EverMarried, WorkType, ResidenceType, AvgGlucoseLevel, BMI, SmokingStatus, Result) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor = conn.cursor()
        cursor.execute(query, data)
        conn.commit()

    def show_dudoan_page():
        st.markdown('<h1 class="noidung">Nhập thông tin bệnh nhân để dự đoán xem có nguy cơ bị đột quỵ hay không?</h1>', unsafe_allow_html=True)
        st.markdown(
            """
            <style>
            .noidung {
                font-size: 20px;
                font-family: 'Times New Roman', sans-serif;
                color: #009966;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        gender = st.selectbox('Giới tính', list(gender_encoder.keys()))
        age = st.number_input('Tuổi', min_value=0, max_value=120, value=30)
        hypertension = st.selectbox('Có bị tăng huyết áp không?', [1, 0])
        heart_disease = st.selectbox('Có bị bệnh tim không?', [1, 0])
        ever_married = st.selectbox('Đã kết hôn chưa?', list(ever_married_encoder.keys()))
        work_type = st.selectbox('Loại công việc', list(work_type_encoder.keys()))
        residence_type = st.selectbox('Loại nơi ở', list(residence_type_encoder.keys()))
        avg_glucose_level = st.number_input('Mức đường huyết trung bình', min_value=0.0, max_value=300.0, value=100.0)
        bmi = st.number_input('Chỉ số khối cơ thể (BMI)', min_value=0.0, max_value=100.0, value=25.0)
        smoking_status = st.selectbox('Tình trạng hút thuốc', list(smoking_status_encoder.keys()))

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
            st.success("Dữ liệu đã được lưu vào cơ sở dữ liệu SQL Server!")

    def show_TrangChu_page():
        st.markdown(
            """
            <style>
            .title {
                font-size: 60px;
                font-family: 'Times New Roman', sans-serif;
                color: #000033;
            }
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

    def show_dulieu_page():
        st.markdown('<h1 class="title">THÔNG TIN DỮ LIỆU LIÊN QUAN TỚI BỆNH ĐỘT QUỴ</h1>', unsafe_allow_html=True)
        conn = connect_to_database()
        data = query_data()
        if st.button('Kết nối SQL Server'):
            if conn:
                st.success("Đã kết nối thành công đến SQL Server!")
                st.write(data)

    def main():
        st.sidebar.markdown("<h1 style='font-size: 34px; color: red;'>Trang Chủ</h1>", unsafe_allow_html=True)
        page = st.sidebar.radio("Các Chức Năng Chính", ("Trang Chủ", "Dự đoán", "Dữ liệu"))
        if page == "Trang Chủ":
            show_TrangChu_page()
        elif page == "Dự đoán":
            show_dudoan_page()
        elif page == "Dữ liệu":
            show_dulieu_page()

    if __name__ == '__main__':
        main()
