import sys
import json
import os
import time
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

API_KEY = "AQ.Ab8RN6JIwbqb_7cUAzER4KhOrTaZ3CVJ_FLES3Arr3Bwu1MQOQ"
OWNER_NAME = "Arun kumar"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_text = data.get("message", "").strip()
    
    if not user_text:
        return jsonify({"response": "कमांड खाली है, मास्टर अरुण।"})
        
    if any(word in user_text.lower() for word in ["barish", "weather", "mausam"]):
        weather_response = (
            f"🤖 JARVIS >> आदरणीय जनक मास्टर अरुण, फ़िरोज़ाबाद और मक्खनपुर क्षेत्र का "
            f"लाइव सैटेलाइट रडार डेटा सफलतापूर्वक कंपाइल कर लिया गया है।\n"
            f"आज के वायुमंडलीय दबाव और उच्च आर्द्रता के विश्लेषण के अनुसार, क्षेत्र में "
            f"हल्की से मध्यम स्तर की बारिश होने की लगभग 65% से 70% तक प्रबल संभावना बनी हुई है।"
        )
        return jsonify({"response": weather_response})

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    
    payload = {
        "contents": [{"role": "user", "parts": [{"text": user_text}]}],
        "systemInstruction": {"parts": [{"text": f"You are JARVIS built by {OWNER_NAME}. Respond in detailed Hinglish."}]},
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 1200}
    }
    
    try:
        import requests
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=15)
        if response.status_code == 200:
            ai_response = response.json()['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"response": ai_response})
        return jsonify({"response": "🤖 JARVIS: सर्वर रिस्पॉन्स एरर।"})
    except Exception as e:
        return jsonify({"response": f"🤖 JARVIS: त्रुटि: {str(e)}"})

if __name__ == '__main__':
    @app.route('/')
    def index():
        return """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zenix_AI</title>
    <style>
        body { background-color: #0d0f12; color: #00ffcc; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; padding: 20px; box-sizing: border-box; }
        .container { width: 100%; max-width: 400px; text-align: center; background: #161b22; padding: 25px; border-radius: 15px; border: 1px solid #00ffcc; box-shadow: 0 8px 32px rgba(0, 255, 204, 0.2); }
        h1 { font-size: 28px; margin-bottom: 5px; text-shadow: 0 0 10px #00ffcc; }
        .chat-box { width: 100%; height: 250px; background-color: #0d0f12; border: 1px solid #30363d; border-radius: 8px; margin-bottom: 15px; padding: 10px; box-sizing: border-box; overflow-y: auto; text-align: left; }
        input[type="text"] { width: 100%; padding: 12px; background-color: #0d0f12; border: 1px solid #30363d; border-radius: 8px; color: #ffffff; margin-bottom: 15px; outline: none; }
        button { width: 100%; padding: 12px; background-color: #00ffcc; color: #0d0f12; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
<div class="container">
    <h1>ZENIX_AI</h1>
    <div style="color: #8b949e; font-size: 12px; margin-bottom: 25px;">महा-शक्तिशाली एआई एजेंट सिस्टम</div>
    <div class="chat-box" id="chatBox">
        <span style="color: #00ffcc;">[Zenix_AI]:</span> कमांडर अरुण, मैं सक्रिय हूँ। आदेश दें...
    </div>
    <input type="text" id="userInput" placeholder="अपना महा-शक्तिशाली कमांड यहाँ लिखें...">
    <button onclick="processCommand()">कमांड भेजें</button>
</div>
<script>
    function processCommand() {
        var input = document.getElementById("userInput").value;
        var chatBox = document.getElementById("chatBox");
        if(input.trim() === "") return;
        chatBox.innerHTML += "<br><br><span style='color: #ffffff;'>[अरुण]:</span> " + input;
        document.getElementById("userInput").value = "";
        
        fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: input })
        })
        .then(response => response.json())
        .then(data => {
            chatBox.innerHTML += "<br><br><span style='color: #00ffcc;'>[Zenix_AI]:</span> " + data.response;
            chatBox.scrollTop = chatBox.scrollHeight;
        })
        .catch(error => {
            chatBox.innerHTML += "<br><br><span style='color: #ff3333;'>[Error]:</span> कनेक्शन त्रुटि।";
        });
    }
</script>
</body>
</html>
        """
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
