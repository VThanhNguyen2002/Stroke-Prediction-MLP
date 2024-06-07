import streamlit as st
import pandas as pd
import os
import sys

# Thêm thư mục src/py vào sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from py.prediction.prediction import label_encoder, load_prediction_model
from py.pages.Home.trang_chu import show_trang_chu_page
from py.pages.Prediction.du_doan import show_dudoan_page
from py.pages.DataFromDatabase.du_lieu import show_dulieu_page

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
    model = load_prediction_model(model_path)
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

    encoders = {
        'ever_married': label_encoder(data_cleaned['ever_married']),
        'gender': label_encoder(data_cleaned['gender']),
        'work_type': label_encoder(data_cleaned['work_type']),
        'residence_type': label_encoder(data_cleaned['Residence_type']),
        'smoking_status': label_encoder(data_cleaned['smoking_status'])
    }

    def main():
        st.sidebar.markdown("<h1 style='font-size: 34px; color: red;'>Trang Chủ</h1>", unsafe_allow_html=True)
        page = st.sidebar.radio("Các Chức Năng Chính", ("Trang Chủ", "Dự đoán", "Dữ liệu"))
        if page == "Trang Chủ":
            show_trang_chu_page()
        elif page == "Dự đoán":
            show_dudoan_page(encoders, model)
        elif page == "Dữ liệu":
            show_dulieu_page()

    if __name__ == '__main__':
        main()
