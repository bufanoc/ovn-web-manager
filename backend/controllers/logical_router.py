from flask import Blueprint, request, jsonify
from services.ovn_client import OVNClient
from utils.validators import validate_router_data

logical_router_routes = Blueprint('logical_routers', __name__)
ovn_client = OVNClient()

@logical_router_routes.route('/', methods=['GET'])
def get_all_routers():
    try:
        routers = ovn_client.get_logical_routers()
        return jsonify(routers)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@logical_router_routes.route('/<router_id>', methods=['GET'])
def get_router(router_id):
    try:
        router = ovn_client.get_logical_router(router_id)
        if not router:
            return jsonify({"error": "Router not found"}), 404
        return jsonify(router)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@logical_router_routes.route('/', methods=['POST'])
def create_router():
    data = request.get_json()
    validation_error = validate_router_data(data)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    try:
        router = ovn_client.create_logical_router(data)
        return jsonify(router), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@logical_router_routes.route('/<router_id>', methods=['PUT'])
def update_router(router_id):
    data = request.get_json()
    validation_error = validate_router_data(data)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    try:
        router = ovn_client.update_logical_router(router_id, data)
        if not router:
            return jsonify({"error": "Router not found"}), 404
        return jsonify(router)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@logical_router_routes.route('/<router_id>', methods=['DELETE'])
def delete_router(router_id):
    try:
        success = ovn_client.delete_logical_router(router_id)
        if not success:
            return jsonify({"error": "Router not found"}), 404
        return '', 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@logical_router_routes.route('/<router_id>/ports', methods=['GET'])
def get_router_ports(router_id):
    try:
        ports = ovn_client.get_router_ports(router_id)
        return jsonify(ports)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
