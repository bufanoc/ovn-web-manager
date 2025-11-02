from flask import Blueprint, request, jsonify
from services.ovn_client import OVNClient
from utils.validators import validate_load_balancer_data

load_balancer_routes = Blueprint('load_balancers', __name__)
ovn_client = OVNClient()

@load_balancer_routes.route('/', methods=['GET'])
def get_all_load_balancers():
    try:
        load_balancers = ovn_client.get_load_balancers()
        return jsonify(load_balancers)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@load_balancer_routes.route('/<lb_id>', methods=['GET'])
def get_load_balancer(lb_id):
    try:
        load_balancer = ovn_client.get_load_balancer(lb_id)
        if not load_balancer:
            return jsonify({"error": "Load balancer not found"}), 404
        return jsonify(load_balancer)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@load_balancer_routes.route('/', methods=['POST'])
def create_load_balancer():
    data = request.get_json()
    validation_error = validate_load_balancer_data(data)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    try:
        load_balancer = ovn_client.create_load_balancer(data)
        return jsonify(load_balancer), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@load_balancer_routes.route('/<lb_id>', methods=['PUT'])
def update_load_balancer(lb_id):
    data = request.get_json()
    validation_error = validate_load_balancer_data(data)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    try:
        load_balancer = ovn_client.update_load_balancer(lb_id, data)
        if not load_balancer:
            return jsonify({"error": "Load balancer not found"}), 404
        return jsonify(load_balancer)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@load_balancer_routes.route('/<lb_id>', methods=['DELETE'])
def delete_load_balancer(lb_id):
    try:
        success = ovn_client.delete_load_balancer(lb_id)
        if not success:
            return jsonify({"error": "Load balancer not found"}), 404
        return '', 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500
