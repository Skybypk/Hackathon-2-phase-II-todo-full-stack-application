import gradio as gr
import requests
import threading
import time
import subprocess
import sys
import os

# ============= FASTAPI KO BACKGROUND MEIN CHALANA =============

def run_fastapi():
    """
    Yeh function FastAPI app ko background mein chalayega
    """
    try:
        # subprocess se FastAPI run karo
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app:app",  # app.py mein 'app' variable hai
            "--host", "0.0.0.0", 
            "--port", "8000",  # Different port use karo
            "--reload"
        ])
    except Exception as e:
        print(f"FastAPI Error: {e}")

# FastAPI ko background thread mein start karo
fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
fastapi_thread.start()

# Wait for FastAPI to start
time.sleep(3)  # 3 seconds wait

# ============= GRADIO FUNCTIONS =============

def call_fastapi_endpoint(text):
    """
    Yeh function FastAPI ke /predict endpoint ko call karega
    """
    try:
        # FastAPI endpoint par request bhejo
        response = requests.post(
            "http://localhost:8000/predict",  # 8000 port use kar rahe hain
            json={"text": text},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return f"✅ Success!\nPrediction: {data['prediction']}\nLength: {data['length']}"
        else:
            return f"❌ Error {response.status_code}: {response.text}"
            
    except requests.exceptions.ConnectionError:
        return "❌ FastAPI connection error! Make sure FastAPI is running."
    except Exception as e:
        return f"❌ Error: {str(e)}"

def check_health():
    """
    Health check endpoint ko call karo
    """
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            return "✅ FastAPI is healthy!"
        else:
            return f"❌ Health check failed: {response.status_code}"
    except:
        return "❌ FastAPI not running"

# ============= GRADIO UI =============

with gr.Blocks(title="My Backend API", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🚀 My FastAPI + Gradio App")
    gr.Markdown("Yeh app FastAPI backend ko Gradio frontend ke saath deploy karta hai")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📊 System Status")
            health_btn = gr.Button("Check FastAPI Health", variant="secondary")
            health_output = gr.Textbox(label="Health Status", lines=2)
            
            health_btn.click(
                fn=check_health,
                outputs=health_output
            )
    
    gr.Markdown("---")
    
    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown("### 🤖 Prediction Interface")
            
            # Input
            text_input = gr.Textbox(
                label="Enter Text",
                placeholder="Kuch bhi likho...",
                lines=4
            )
            
            predict_btn = gr.Button("🚀 Predict", variant="primary", size="lg")
            
            # Output
            text_output = gr.Textbox(
                label="Result",
                lines=6,
                interactive=False
            )
            
            predict_btn.click(
                fn=call_fastapi_endpoint,
                inputs=text_input,
                outputs=text_output
            )
    
    gr.Markdown("---")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 📚 API Documentation")
            gr.Markdown("""
            **Available Endpoints:**
            - `GET /` - Root endpoint
            - `GET /health` - Health check
            - `POST /predict` - Main prediction endpoint
            
            **Example Request:**
            ```json
            POST /predict
            {
                "text": "Hello world"
            }
            ```
            
            **Swagger UI:** `/docs` par jao
            """)
    
    gr.Markdown("---")
    gr.Markdown("### 📝 Example Inputs")
    
    examples = [
        ["This is a test message"],
        ["Machine learning is amazing!"],
        ["FastAPI and Gradio together"]
    ]
    
    for example in examples:
        gr.Examples(
            examples=[example],
            inputs=text_input
        )

# ============= APP LAUNCH =============
if __name__ == "__main__":
    # Gradio ko 7860 port par chalao (Hugging Face default)
    demo.launch(
        server_name="0.0.0.0", 
        server_port=7860,
        share=False  # True karo to temporary public link milega
    ) 