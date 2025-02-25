## Preview
https://crop-yield-prediction-796r.onrender.com

# Crop Yield Prediction

## Team
**Accidental Coders**

## Written By
**Sanchit (Karlex1)** for **GDG Campus Solution**

## Problem Statement
Small and marginal farmers, who constitute approximately 126 million of India's agricultural sector, face significant challenges due to limited landholdings, resource constraints, and the adverse impacts of climate change. In regions like Siddharthnagar and Balrampur in Uttar Pradesh, erratic rainfall, rising temperatures, and extreme weather events have disrupted traditional farming practices, leading to reduced crop yields, economic difficulties, and environmental degradation.

### Key Challenges
- **Climate Change Impacts**: Unpredictable weather patterns and rising temperatures.
- **Resource Constraints**: Limited access to quality seeds, fertilizers, and modern farming equipment.
- **Soil Degradation**: Unsustainable farming practices leading to soil erosion and loss of fertility.
- **Information Gap**: Limited access to accurate and timely agricultural information.
- **Inefficient Practices**: Resource-intensive traditional methods prone to crop failures.

These challenges result in economic losses, food insecurity, and environmental degradation, threatening the livelihoods of small and marginal farmers and the well-being of rural communities.

## Objective
Participants are tasked with creating an **AI-powered agricultural advisory system** to provide timely, relevant, and personalized agricultural information to small and marginal farmers. The solution should leverage **machine learning, remote sensing, and IoT technologies** to address the challenges and improve agricultural productivity, resilience, and sustainability.

## Overview
The **Crop Yield Prediction** project aims to estimate crop yield based on various factors such as pesticide use, item type, and geographical region (country). The model utilizes machine learning techniques and integrates real-time weather data (temperature and rainfall) to enhance prediction accuracy.

## Features
- **Machine Learning Models**: Uses Linear Regression (lr), Lasso (lso), Ridge (rdg), K-Nearest Neighbors (knr), and Decision Tree Regressor (dtr) for prediction.
- **Weather API Integration**: Automatically fetches temperature and rainfall data for the selected region and year.
- **Streamlit Web Application**: Provides an interactive UI for users to input data and view predictions.
- **Intelligent Year Handling**: Ensures proper handling of the year input for meaningful predictions.

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/Karlex1/Crop_yield_Prediction.git
   ```
2. Navigate to the project directory:
   ```sh
   cd Crop_yield_Prediction
   ```
3. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   ```
4. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
### Running the Model
To run the machine learning model, execute the Jupyter Notebook file:
```sh
jupyter notebook Crop_Yield_Prediction.ipynb
```
This will open the notebook interface where you can train and test the model interactively.
### Running the Streamlit App
To launch the Streamlit web application, run:
```sh
streamlit run app.py
```
This will start a local server, and you can access the app in your browser.

### Inputs Required
- **Pesticide Usage**: Amount of pesticide applied.
- **Crop Item**: The specific crop type being analyzed.
- **Country (Area)**: The geographical region for prediction.
- **Year**: The year for which the prediction is being made.

## Future Improvements
- Enhance the model with additional machine learning algorithms.
- Improve UI/UX for better user interaction.
- Add support for more data sources to improve prediction accuracy.
- Deploy the Streamlit app online.

## Contributing
Contributions are welcome! Feel free to fork the repository, make changes, and submit a pull request.

### How to Submit a PR
1. Fork the repository.
2. Create a new branch for your feature or fix:
   ```sh
   git checkout -b feature-branch-name
   ```
3. Make your changes and commit them:
   ```sh
   git commit -m "Add your commit message here"
   ```
4. Push your changes to your fork:
   ```sh
   git push origin feature-branch-name
   ```
5. Open a pull request on GitHub and describe your changes.
Contributions are welcome! Feel free to fork the repository, make changes, and submit a pull request.

This project is licensed under the MIT License.

## Contact
For any queries or suggestions, connect on [LinkedIn](https://www.linkedin.com/in/sanchit-312928214/) or drop an email at **sanchit959871@gmail.com**.
For any queries or suggestions, please reach out via [GitHub Issues](https://github.com/Karlex1/Crop_yield_Prediction/issues).

