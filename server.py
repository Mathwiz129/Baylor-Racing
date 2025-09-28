# save as gps_server.py
from flask import Flask, request, render_template_string

app = Flask(__name__)

# store latest GPS + speed data
data = {"lat": "NOFIX", "lng": "NOFIX", "speed": 0}

# web dashboard
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Live GPS Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
<h1>Live GPS & Speed Dashboard</h1>
<div id="gps">Waiting for data...</div>

<script>
async function updateDashboard() {
    const resp = await fetch('/data');
    const text = await resp.text();
    document.getElementById('gps').innerText = text;
}
setInterval(updateDashboard, 1000);
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/data')
def get_data():
    lat = data["lat"]
    lng = data["lng"]
    speed = data["speed"]
    return f"Lat: {lat}, Lng: {lng}, Speed: {speed} m/s"

@app.route('/update')
def update():
    lat = request.args.get("lat")
    lng = request.args.get("lng")
    speed = request.args.get("speed", 0)
    if lat and lng:
        data["lat"] = lat
        data["lng"] = lng
        data["speed"] = speed
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
