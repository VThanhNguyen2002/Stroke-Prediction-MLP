# Introduction:
The StrokePython project is a Python-based initiative focused on training an Artificial Intelligence (AI) model and deploying it to a user interface (UI) for stroke diagnosis. This project is developed as part of a Machine Learning course within the field of Data Analytics and Artificial Intelligence at Ho Chi Minh City University of Industry and Trade.
# Project Details
- Course: Machine Learning
- Language Used: Python
- Database: SQL Server
- Model Training Files: You can open them on Google Colab with the filename "stroke_NguyenVietThanh.ipynb" and also on Visual Studio Code with the filename "stroke_NguyenVietThanh.py" (all code explanations are provided in that file in Vietnamese).
- UI.py: Interface designed to load the trained model ("mymodel.h5") for stroke diagnosis.

# Stroke Prediction Model

## Project Description
This project involves a machine learning model that utilizes a neural network to predict the likelihood of a stroke based on various health-related features of patients. The model is built using the TensorFlow and NumPy libraries for data processing and model training.

## Model Architecture
The model employs a neural network structure with 4 layers:
- First layer: 64 neurons, ReLU activation.
- Second layer: 64 neurons, ReLU activation.
- Third layer: 64 neurons, ReLU activation.
- Final layer: 1 neuron with sigmoid activation for binary classification.

## Training Process
The model is trained on health data from the "healthcare-dataset-stroke-data.csv" CSV file. Data is preprocessed by removing missing values and encoding categorical variables. Training is carried out over 100 epochs with Adam optimization and binary_crossentropy loss function.

## Model Evaluation
The model is evaluated on the test set, providing accuracy and loss metrics. The results are printed to the console after the training process is complete.

## Model Storage
The trained model is saved in the "my_model.h5" file after the training process concludes.

## Usage Guide
- Ensure that the required libraries are installed.
- Run the notebook or Python script to train the model.
- Check the results and evaluate the model on the test set.
- Use the saved model to predict stroke status on new data.

## References
- TensorFlow Library
- NumPy Library
- Pandas Library
- Scikit-learn Library
