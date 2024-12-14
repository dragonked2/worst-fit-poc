from flask import Flask, request, render_template_string
import subprocess

app = Flask(__name__)

HTML_TEMPLATE = """
<html>
    <body>
        <form method="POST">
            <label for="filename">Enter filename:</label>
            <input type="text" id="filename" name="filename" required>
            <button type="submit">Download</button>
        </form>
        <p><strong>Output:</strong>{{ output }}</p>
    </body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    user_input = request.form.get("filename")
    result = subprocess.run(['wget.exe', f'http://example.tld/{user_input}.txt'])
    output = result.stdout or result.stderr
    return render_template_string(HTML_TEMPLATE, output=output)

if __name__ == "__main__":
    app.run(debug=False)
