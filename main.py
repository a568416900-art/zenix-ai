from flask import Flask, request, jsonify, render_template_string
import os
import requests

app = Flask(__name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zenix AI</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #121212; color: white; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .chat-container { width: 90%; max-width: 450px; background: #1e1e1e; border-radius: 15px; padding: 20px; box-shadow: 0px 5px 15px rgba(0,0,0,0.5); text-align: center; }
        h2 { color: #00adb5; margin-bottom: 20px; }
        .btn-mic { background-color: #ff2e63; border: none; color: white; padding: 20px; border-radius: 50%; font-size: 24px; cursor: pointer; box-shadow: 0 0 15px #ff2e63; transition: 0.3s; }
        #status { margin-top: 15px; color: #bbb; font-style: italic; }
        #output { margin-top: 20px; padding: 15px; background: #252525; border-radius: 10px; text-align: left; max-height: 150px; overflow-y: auto; border-left: 5px solid #00adb5; }
    </style>
</head>
<body>
    <div class="chat-container">
        <h2>Zenix Voice AI ⚡</h2>
        <p>बटन दबाकर बोलें</p>
        <button class="btn-mic" id="start-btn">🎙️</button>
        <div id="status">बटन दबाएं...</div>
        <div id="output"><strong>जवाब यहाँ दिखेगा...</strong></div>
    </div>
    <script>
        const startBtn = document.getElementById('start-btn');
        const statusDiv = document.getElementById('status');
        const outputDiv = document.getElementById('output');
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

        if (!SpeechRecognition) {
            statusDiv.innerText = "वॉइस सपोर्ट नहीं है।";
        } else {
            const recognition = new SpeechRecognition();
            recognition.lang = 'hi-IN';

            startBtn.addEventListener('click', () => {
                recognition.start();
                statusDiv.innerText = "सुन रहा हूँ...";
            });

            recognition.onresult = async (event) => {
                const userText = event.results[0][0].transcript;
                statusDiv.innerText = "सोच रहा हूँ...";
                outputDiv.innerHTML = `<strong>आप:</strong> ${userText}`;

                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message: userText })
                    });
                    const data = await response.json();
                    
                    // यहाँ हमने एरर को पूरी तरह ठीक कर दिया है
                    outputDiv.innerHTML += '<br><br><strong>Zenix:</strong> ' + data.reply;
                    statusDiv.innerText = "जवाब दे दिया!";

                    const speech = new SpeechSynthesisUtterance(data.reply);
                    speech.lang = 'hi-IN';
                    window.speechSynthesis.speak(speech);
                } catch (err) {
                    statusDiv.innerText = "कनेक्शन एरर!";
                }
            };
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    if not GEMINI_API_KEY:
        return jsonify({"reply": "कृपया रेंडर सेटिंग्स में अपनी GEMINI_API_KEY जोड़ें।"})

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": user_message}]}]}
    
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        ai_reply = data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        ai_reply = "माफ़ करना अरुण, मैं अभी कनेक्ट नहीं कर पा रहा हूँ। कृपया अपनी एपीआई की चेक करें।"
        
    return jsonify({"reply": ai_reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
