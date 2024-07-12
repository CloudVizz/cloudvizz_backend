from flask import Flask, request, jsonify
from config import Config
from utils.sts import assume_role
from services.aws_service import list_all_resources, get_resource_details

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/assume_role', methods=['POST'])
def assume_role_endpoint():
    data = request.get_json()
    account_id = data.get('account_id')
    role_name = data.get('role_name')
    external_id = data.get('external_id')

    try:
        creds = assume_role(account_id, role_name, external_id)
        return jsonify({"message": "Role assumed successfully", "credentials": creds}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/list_resources', methods=['POST'])
def list_resources_endpoint():
    data = request.get_json()
    account_id = data.get('account_id')
    role_name = data.get('role_name')
    external_id = data.get('external_id')

    try:
        creds = assume_role(account_id, role_name, external_id)
        resources = list_all_resources(creds)
        return jsonify({"resources": resources}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/resource_details', methods=['POST'])
def resource_details_endpoint():
    data = request.get_json()
    account_id = data.get('account_id')
    role_name = data.get('role_name')
    external_id = data.get('external_id')
    region = data.get('region')
    resource_id = data.get('resource_id')
    resource_type = data.get('resource_type')

    try:
        creds = assume_role(account_id, role_name, external_id)
        details = get_resource_details(creds, region, resource_id, resource_type)
        if details:
            return jsonify({"resource_details": details}), 200
        else:
            return jsonify({"error": "Resource not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
