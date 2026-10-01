from flask import Flask, jsonify, request

app = Flask(__name__)
applications = []

def validate_application_data(data):
    """Өтінім мәліметтерін тексеретін функция"""
    if not data:
        return False, "Деректер бос болмауы керек"
    if "full_name" not in data or not data["full_name"].strip():
        return False, "Студенттің аты-жөні міндетті"
    if "faculty" not in data or not data["faculty"].strip():
        return False, "Факультет атауы міндетті"
    if "gpa" not in data or not (0.0 <= float(data.get("gpa", -1)) <= 4.0):
        return False, "GPA 0.0 мен 4.0 аралығында болуы тиіс"
    return True, "Деректер дұрыс"

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "online", "message": "Студенттік өтінім жүйесі қосулы"}), 200

@app.route("/applications", methods=["POST"])
def submit_application():
    data = request.get_json()
    is_valid, msg = validate_application_data(data)
    
    if not is_valid:
        return jsonify({"success": False, "error": msg}), 400
    
    app_id = len(applications) + 1
    new_app = {
        "id": app_id,
        "full_name": data["full_name"],
        "faculty": data["faculty"],
        "gpa": float(data["gpa"]),
        "status": "Submitted"
    }
    applications.append(new_app)
    return jsonify({"success": True, "application": new_app}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)