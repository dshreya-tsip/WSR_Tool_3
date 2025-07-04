from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    # Use debug=True for auto-reload when you edit files
    app.run(host='0.0.0.0', port=5000, debug=True)
