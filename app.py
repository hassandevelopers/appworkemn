from flask import Flask, jsonify
from google_play_scraper import app as play_scraper
import time

app = Flask(__name__)

last_request_time = 0
request_interval = 1  # seconds

@app.route('/app_details/<package_name>', methods=['GET'])
def get_app_details(package_name):
    global last_request_time
    
    # Implement rate limiting
    current_time = time.time()
    if current_time - last_request_time < request_interval:
        return jsonify({"error": "Too many requests. Please wait and try again."}), 429

    app_details = play_scraper(package_name)

    app_info = {
        "Name": app_details.get('title'),
        "Image": app_details.get('icon'),
        "Installs": app_details.get('installs'),
        "Developer Name": app_details.get('developer'),
        "Updated Date": app_details.get('updated'),
        "Version": app_details.get('version'),
        "File Size": app_details.get('size'),
        "Requires Android": app_details.get('androidVersion'),
        "Package Name": app_details.get('appId'),
        "Price": app_details.get('price'),
        "Rating": app_details.get('score'),
        "Screenshots": app_details.get('screenshots'),
        "Description": app_details.get('descriptionHTML')
    }

    last_request_time = current_time
    return jsonify(app_info)

# Make sure this part is at the end of your file
if __name__ == '__main__':
    app.run(debug=True)
