from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

# सुंदर चैट बॉक्स और बोलने वाले सिस्टम का डिज़ाइन (HTML, CSS, JS)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zenix AI</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121212; color: white; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .chat-container { width: 90%; max-width: 450px; background: #1e1e1e; border-radius: 15px; padding: 20px; box-shadow: 0px 5px 15px rgba(0,0,0,0.5); text-align: center; }
        h2 { color: #00adb5; margin-bottom: 20px; }
        .btn-mic { background-color: #ff2e63; border: none; color: white; padding: 20px; border-radius: 50%; font-size: 24px; cursor: pointer; box-shadow: 0 0 15px #ff2e63; transition: 0.3s; }
        .btn-mic:active { transform: scale(0.9); box-shadow: 0 0 25px #ff2e63; }
        #status { margin-top: 15px; color: #bbb; font-style: italic; }
        #output { margin-top: 20px; padding: 15px; background: #252525; border-radius: 10px; text-align: left; max-height: 150px; overflow-y: auto; border-left: 5px solid #00adb5; }
    </style>
</head>
<body>

<div class="chat-container">
    <h2>Zenix Voice AI ⚡</h2>
    <p>बटन दबाकर बोलें और एआई की आवाज़ सुनें</p>
    
    <button class="btn-mic" id="start-btn">🎙️</button>
    <div id="status">बटन दबाएं और बोलना शुरू करें...</div>
    
    <div id="output">
        <strong>जवाब यहाँ दिखेगा...</strong>
    </div>
</div>

<script>
    const startBtn = document.getElementById('start-btn');
    const statusDiv = document.getElementById('status');
    const outputDiv = document.getElementById('output');

    // बोलने और सुनने का सिस्टम (Web Speech API)
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
        statusDiv.innerText = "आपका ब्राउज़र वॉइस सपोर्ट नहीं करता। Chrome का उपयोग करें।";
    } else {
        const recognition = new SpeechRecognition();
        recognition.lang = 'hi-IN'; // हिंदी भाषा सपोर्ट

        startBtn.addEventListener('click', () => {
            recognition.start();
            statusDiv.innerText = "सुन रहा हूँ... बोलिए...";
        });

        recognition.onresult = async (event) => {
            const userText = event.results[0][0].transcript;
            statusDiv.innerText = "सोच रहा हूँ...";
            outputDiv.innerHTML = `<strong>आप:</strong> ${userText}`;

            // यहाँ सर्वर से जवाब मांग रहे हैं
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: userText })
                });
                const data = await response.json();
                
                // एआई का जवाब स्क्रीन पर दिखाना
                outputDiv.innerHTML += `<br><br><strong>Zenix:</strong> ${data.reply}`;
                statusDiv.innerText = "जवाब दे दिया!";

                // एआई का बोलकर जवाब देना (Text to Speech)
                const speech = new SpeechSynthesisUtterance(data.reply);
                speech.lang = 'hi-IN';
                window.speechSynthesis.speak(speech);

            } catch (err) {
                statusDiv.innerText = "कनेक्शन एरर!";
            }
        };

        recognition.onerror = () => {
            statusDiv.innerText = "आवाज़ समझ नहीं आई, दोबारा कोशिश करें।";
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
    
    # महा शक्तिशाली एआई का रिप्लाई (अभी के लिए बेसिक जवाब, बाद में इसे और बड़ा करेंगे)
    ai_reply = f"नमस्ते अरुण! मैंने सुना आपने कहा: {user_message}। आपका जेनेक्स एआई पूरी तरह तैयार है।"
    
    return jsonify({"reply": ai_reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
