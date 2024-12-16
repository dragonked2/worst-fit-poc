from flask import Flask, request, render_template_string, abort
import subprocess
import shlex
import validators
import re

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
    <head>
        <title>Secure File Downloader</title>
    </head>
    <body>
        <h1>File Downloader</h1>
        <form method="POST">
            <label for="filename">Enter filename (without extensions or path traversal):</label><br>
            <input type="text" id="filename" name="filename" pattern="[a-zA-Z0-9_-]+" required>
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
        user_input = request.form.get("filename", "").strip()

        if not re.match(r"^[a-zA-Z0-9_-]+$", user_input):
            abort(400, "Invalid filename. Only alphanumeric characters, hyphens, and underscores are allowed.")

        base_url = "https://example.tld"
        file_url = f"{base_url}/{user_input}.txt"

        if not validators.url(file_url) or not file_url.startswith(base_url):
            abort(400, "Invalid URL constructed. Please try again.")

        try:
            result = subprocess.run(
                ['wget', file_url],
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode == 0:
                output = f"File downloaded successfully from {file_url}."
            else:
                output = f"Failed to download file. Error:\n{result.stderr}"
        except subprocess.SubprocessError as e:
            abort(500, f"An internal error occurred during the download: {e}")

    return render_template_string(HTML_TEMPLATE, output=output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
