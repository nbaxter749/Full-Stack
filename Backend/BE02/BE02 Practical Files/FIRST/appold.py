from flask import Flask, make_response

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    return make_response("<h1>Hello world</h1>", 200)

@app.route("/com661", methods=['GET'])
def com661():
    return make_response("<h1>Welcome to COM661</h1>", 200)

@app.route("/module/<string:code>", methods=['GET'])
def module(code):
    return make_response("<h1>Welcome to " + code + "</h1>", 200)

if __name__ == "__main__":
    app.run(debug=True)
