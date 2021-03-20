from flask import Flask, request,render_template
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/analyse')
def vmd_timestamp():
    return render_template('vmd_timestamp.html')
# run the application
if __name__ == "__main__":
    app.run(debug=True)