from flask import Blueprint, request, jsonify
from services.ovn_client import OVNClient
from utils.validators import validate_port_data

port_routes = Blueprint('ports', __name__)
ovn_client = OVNClient()

@port_routes.route('/', methods=['GET'])
def get_all_ports():
    try:
        ports = ovn_client.get_all_ports()
        return jsonify(ports)
    except Exception as e:
        return jsonify({"error": "An error occurred processing your request"}), 500

@port_routes.route('/<port_id>', methods=['GET'])
def get_port(port_id):
    try:
        port = ovn_client.get_port(port_id)
        if not port:
            return jsonify({"error": "Port not found"}), 404
        return jsonify(port)
    except Exception as e:
        return jsonify({"error": "An error occurred processing your request"}), 500

@port_routes.route('/', methods=['POST'])
def create_port():
    data = request.get_json()
    validation_error = validate_port_data(data)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    try:
        port = ovn_client.create_port(data)
        return jsonify(port), 201
    except Exception as e:
        return jsonify({"error": "An error occurred processing your request"}), 500

@port_routes.route('/<port_id>', methods=['PUT'])
def update_port(port_id):
    data = request.get_json()
    validation_error = validate_port_data(data)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    try:
        port = ovn_client.update_port(port_id, data)
        if not port:
            return jsonify({"error": "Port not found"}), 404
        return jsonify(port)
    except Exception as e:
        return jsonify({"error": "An error occurred processing your request"}), 500

@port_routes.route('/<port_id>', methods=['DELETE'])
def delete_port(port_id):
    try:
        success = ovn_client.delete_port(port_id)
        if not success:
            return jsonify({"error": "Port not found"}), 404
        return '', 204
    except Exception as e:
        return jsonify({"error": "An error occurred processing your request"}), 500
