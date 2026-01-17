from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Interview Pal is LIVE! (Managed by Member 4)"

if __name__ == '__main__':
    app.run(debug=True)