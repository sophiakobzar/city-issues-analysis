# Sentiment Analysis of City Issues

This project analyzes comments related to city issues such as traffic, homelessness, and drug use. It uses Azure OpenAI for sentiment analysis and displays the results using a React frontend with Plotly for visualization.

## Table of Contents

- Installation
- Usage
- Project Structure
- API Endpoints
- Technologies Used
- Contributing
- License

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/sophiakobzar/city-issues-analysis.git
    cd city-issues-analysis
    ```

2. **Install Node.js dependencies**:
    ```bash
    npm install
    ```

3. **Install Python dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up Azure OpenAI**:
    - Create a `config.py` file in the root directory with the following content:
      ```bash
      touch config.py
      ```
   - Add the following to `config.py` file:
      ```python
      AZURE_OPENAI_API_KEY = "your_api_key"
      AZURE_OPENAI_API_VERSION = "2023-05-15"
      AZURE_OPENAI_API_BASE = "https://your-openai-resource-name.openai.azure.com/"
      AZURE_OPENAI_DEPLOYMENT_NAME = "your_deployment_name"
      ```

## Usage

1. **Run the Node.js server**:
    ```bash
    node api.cjs
    ```

2. **Run the React frontend**:
    ```bash
    npm run dev
    ```

3. **Access the application**:
    Open your web browser and navigate to `http://localhost:5173/`.

## Project Structure
