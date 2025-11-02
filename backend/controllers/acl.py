from flask import Blueprint, request, jsonify
from services.ovn_client import OVNClient
from utils.validators import validate_acl_data

acl_routes = Blueprint('acls', __name__)
ovn_client = OVNClient()

@acl_routes.route('/', methods=['GET'])
def get_all_acls():
    try:
        acls = ovn_client.get_acls()
        return jsonify(acls)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@acl_routes.route('/<switch_id>/acls', methods=['GET'])
def get_switch_acls(switch_id):
    try:
        acls = ovn_client.get_switch_acls(switch_id)
        return jsonify(acls)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@acl_routes.route('/<switch_id>/acls', methods=['POST'])
def create_acl(switch_id):
    data = request.get_json()
    validation_error = validate_acl_data(data)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    try:
        acl = ovn_client.create_acl(switch_id, data)
        return jsonify(acl), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@acl_routes.route('/<switch_id>/acls/<acl_id>', methods=['DELETE'])
def delete_acl(switch_id, acl_id):
    try:
        success = ovn_client.delete_acl(switch_id, acl_id)
        if not success:
            return jsonify({"error": "ACL not found"}), 404
        return '', 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500
