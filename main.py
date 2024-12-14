from flask import Flask, request, render_template_string
import subprocess

app = Flask(__name__)

# HTML template with a form
HTML_TEMPLATE = """
<!doctype html>
<html>
    <head><title>File Downloader</title></head>
    <body>
        <h1>Download a File</h1>
        <form method="POST">
            <label for="filename">Enter filename:</label>
            <input type="text" id="filename" name="filename" required>
            <button type="submit">Download</button>
        </form>
        {% if output %}
            <p><strong>Output:</strong></p>
            <pre>{{ output }}</pre>
        {% endif %}
    </body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    output = None
    if request.method == "POST":
        # Get user-provided input from the form
        user_input = request.form.get("filename")

        # Vulnerable subprocess call
        try:
            result = subprocess.run(
                ['wget.exe', f'http://example.tld/{user_input}.txt'],
                capture_output=True,
                text=True
            )
            output = result.stdout or result.stderr
        except Exception as e:
            output = str(e)

    return render_template_string(HTML_TEMPLATE, output=output)

if __name__ == "__main__":
    app.run(debug=True)
