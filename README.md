# AI Article Summarizer

A professional, visually striking AI-powered article summarizer built with Streamlit and GROQ API (Llama 3.1).

## Features
- **Premium UI**: Custom CSS and card-based layout.
- **Instant Summaries**: Fast inference using GROQ API.
- **Length Control**: Toggle between Brief and Detailed summaries.
- **Character Metrics**: Real-time tracking of input and output lengths.
- **Professional Design**: Typography and color schemes tailored for readability.

## Prerequisites
- Python 3.9+
- A [GROQ API Key](https://console.groq.com/keys)

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Article-Summariser
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables**:
   Create a `.env` file in the root directory and add your GROQ API key:
   ```env
   GROQ_API_KEY=your_actual_api_key_here
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## Technical Details
- **Frontend**: Streamlit
- **Model**: `llama-3.1-8b-instant` (GROQ)
- **Styling**: Custom HTML/CSS within Streamlit
