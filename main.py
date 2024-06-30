from flask import Flask, request, abort
from app.line_bot import handle_line_event
from app.config import Config

app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handle_line_event(body, signature)
    except Exception as e:
        abort(400)

    return 'OK'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
