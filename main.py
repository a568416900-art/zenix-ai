from flask import Flask, request, jsonify

app = Flask(__name__)

# मुख्य पेज के लिए रास्ता (ताकि Not Found न आए)
@app.route('/')
def home():
    return "<h1>Zenix AI Server is Running Successfully!</h1><p>Use /chat to talk with AI.</p>"

# चैट करने के लिए सही रास्ता
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_message = request.json.get('message', '')
        # यहाँ आपका एआई जवाब देगा
        return jsonify({"reply": f"Zenix AI received: {user_message}"})
    return "<h1>Zenix AI Chat Endpoint is Ready!</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
