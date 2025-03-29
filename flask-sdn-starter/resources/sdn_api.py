from flask import request
from flask_smorest import Blueprint
import requests
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt
from .role_required import viewer_required, operator_required

# Base URL for the Ryu controller's REST API
RYU_BASE_URL = "http://localhost:8080"

# Blueprint: Firewall Management APIs
firewall_blp = Blueprint("firewall", "firewall", url_prefix="/firewall", description="Firewall Management APIs")

@firewall_blp.route("/module/status", methods=["GET"])
@firewall_blp.response(200, description="Get firewall status for all switches")
@jwt_required()
@viewer_required
def firewall_status():
    resp = requests.get(f"{RYU_BASE_URL}/firewall/module/status")
    resp.raise_for_status()
    return resp.json()

@firewall_blp.route("/module/enable/<string:switchid>", methods=["PUT"])
@firewall_blp.response(200, description="Enable firewall on a switch")
@jwt_required()
@operator_required
def enable_firewall(switchid):
    resp = requests.put(f"{RYU_BASE_URL}/firewall/module/enable/{switchid}")
    resp.raise_for_status()
    return resp.json()

@firewall_blp.route("/module/disable/<string:switchid>", methods=["PUT"])
@firewall_blp.response(200, description="Disable firewall on a switch")
@jwt_required()
@operator_required
def disable_firewall(switchid):
    resp = requests.put(f"{RYU_BASE_URL}/firewall/module/disable/{switchid}")
    resp.raise_for_status()
    return resp.json()

@firewall_blp.route("/log/status", methods=["GET"])
@firewall_blp.response(200, description="Get firewall log status")
@jwt_required()
@viewer_required
def log_status():
    resp = requests.get(f"{RYU_BASE_URL}/firewall/log/status")
    resp.raise_for_status()
    return resp.json()

@firewall_blp.route("/log/enable/<string:switchid>", methods=["PUT"])
@firewall_blp.response(200, description="Enable firewall logging")
@jwt_required()
@operator_required
def enable_log(switchid):
    resp = requests.put(f"{RYU_BASE_URL}/firewall/log/enable/{switchid}")
    resp.raise_for_status()
    return resp.json()

@firewall_blp.route("/log/disable/<string:switchid>", methods=["PUT"])
@firewall_blp.response(200, description="Disable firewall logging")
@jwt_required()
@operator_required
def disable_log(switchid):
    resp = requests.put(f"{RYU_BASE_URL}/firewall/log/disable/{switchid}")
    resp.raise_for_status()
    return resp.json()

@firewall_blp.route("/rules/<string:switchid>", methods=["GET", "POST", "DELETE"])
@firewall_blp.response(200, description="View, add, or delete firewall rules")
@jwt_required()
def firewall_rules(switchid):
    role = get_jwt().get("role", "viewer")  # Default to viewer if missing

    # Enforce role-based access
    if request.method == "GET":
        if role not in ["viewer", "operator", "admin"]:
            return {"message": "You do not have permission to view rules."}, 403
    elif request.method in ["POST", "DELETE"]:
        if role not in ["operator", "admin"]:
            return {"message": "Only operators and admins can modify firewall rules."}, 403

    # Execute the actual request to Ryu
    if request.method == "GET":
        resp = requests.get(f"{RYU_BASE_URL}/firewall/rules/{switchid}")
    elif request.method == "POST":
        data = request.get_json()
        resp = requests.post(f"{RYU_BASE_URL}/firewall/rules/{switchid}", json=data)
    elif request.method == "DELETE":
        data = request.get_json()
        resp = requests.delete(f"{RYU_BASE_URL}/firewall/rules/{switchid}", json=data)

    resp.raise_for_status()
    return resp.json()

@firewall_blp.route("/rules/<string:switchid>/<string:vlanid>", methods=["GET", "POST", "DELETE"])
@firewall_blp.response(200, description="View, add, or delete VLAN-specific firewall rules")
@jwt_required()
def firewall_vlan_rules(switchid, vlanid):
    role = get_jwt().get("role", "viewer")  # Default to viewer if missing

    # Enforce role-based access
    if request.method == "GET":
        if role not in ["viewer", "operator", "admin"]:
            return {"message": "You do not have permission to view rules."}, 403
    elif request.method in ["POST", "DELETE"]:
        if role not in ["operator", "admin"]:
            return {"message": "Only operators and admins can modify firewall rules."}, 403

    # Execute the actual request to Ryu
    if request.method == "GET":
        resp = requests.get(f"{RYU_BASE_URL}/firewall/rules/{switchid}/{vlanid}")
    elif request.method == "POST":
        data = request.get_json()
        resp = requests.post(f"{RYU_BASE_URL}/firewall/rules/{switchid}/{vlanid}", json=data)
    elif request.method == "DELETE":
        data = request.get_json()
        resp = requests.delete(f"{RYU_BASE_URL}/firewall/rules/{switchid}/{vlanid}", json=data)

    resp.raise_for_status()
    return resp.json()

# Blueprint: OpenFlow Switch Management APIs
openflow_blp = Blueprint("openflow", "openflow", url_prefix="/stats", description="OpenFlow Switch Management APIs")

@openflow_blp.route("/switches", methods=["GET"])
@openflow_blp.response(200, description="Get a list of all switches")
@jwt_required()
@viewer_required
def get_switches():
    resp = requests.get(f"{RYU_BASE_URL}/stats/switches")
    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/desc/<string:dpid>", methods=["GET"])
@openflow_blp.response(200, description="Get switch description")
@jwt_required()
@viewer_required
def desc_stats(dpid):
    resp = requests.get(f"{RYU_BASE_URL}/stats/desc/{dpid}")
    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/flow/<string:dpid>", methods=["GET", "POST"])
@openflow_blp.response(200, description="View or modify flow stats")
@jwt_required()
def flows(dpid):
    role = get_jwt().get("role", "viewer")

    if request.method == "GET":
        if role not in ["viewer", "operator", "admin"]:
            return {"message": "You do not have permission to view flow stats."}, 403
    else:  # POST (modify)
        if role not in ["operator", "admin"]:
            return {"message": "Only operators and admins can modify flow stats."}, 403

    # Execute the actual request
    if request.method == "GET":
        resp = requests.get(f"{RYU_BASE_URL}/stats/flow/{dpid}")
    else:
        data = request.get_json()
        resp = requests.post(f"{RYU_BASE_URL}/stats/flow/{dpid}", json=data)

    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/aggregateflow/<string:dpid>", methods=["GET", "POST"])
@openflow_blp.response(200, description="View or modify aggregate flow stats")
@jwt_required()
def aggregate_flows(dpid):
    role = get_jwt().get("role", "viewer")  # Default to viewer

    if request.method == "GET":
        # Allow all authenticated users (viewers, operators, admins)
        pass
    elif request.method == "POST":
        # Restrict modifications to operators and admins only
        if role not in ["operator", "admin"]:
            return {"message": "Only operators and admins can modify aggregate flow stats."}, 403

    # Execute the request to Ryu controller
    if request.method == "GET":
        resp = requests.get(f"{RYU_BASE_URL}/stats/aggregateflow/{dpid}")
    else:  # POST
        data = request.get_json()
        resp = requests.post(f"{RYU_BASE_URL}/stats/aggregateflow/{dpid}", json=data)

    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/table/<string:dpid>", methods=["GET"])
@openflow_blp.response(200, description="Get table stats")
@jwt_required()
@viewer_required
def table_stats(dpid):
    resp = requests.get(f"{RYU_BASE_URL}/stats/table/{dpid}")
    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/tablefeatures/<string:dpid>", methods=["GET"])
@openflow_blp.response(200, description="Get table features")
@jwt_required()
@viewer_required
def table_features(dpid):
    resp = requests.get(f"{RYU_BASE_URL}/stats/tablefeatures/{dpid}")
    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/port/<string:dpid>", methods=["GET"])
@openflow_blp.response(200, description="Get port stats")
@jwt_required()
@viewer_required
def port_stats(dpid):
    resp = requests.get(f"{RYU_BASE_URL}/stats/port/{dpid}")
    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/port/<string:dpid>/<string:port>", methods=["GET"])
@openflow_blp.response(200, description="Get stats for a specific port")
@jwt_required()
@viewer_required
def specific_port_stats(dpid, port):
    resp = requests.get(f"{RYU_BASE_URL}/stats/port/{dpid}/{port}")
    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/portdesc/<string:dpid>", methods=["GET"])
@openflow_blp.response(200, description="Get port descriptions")
@jwt_required()
@viewer_required
def port_desc(dpid):
    resp = requests.get(f"{RYU_BASE_URL}/stats/portdesc/{dpid}")
    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/portdesc/<string:dpid>/<string:port_no>", methods=["GET"])
@openflow_blp.response(200, description="Get description for specific port")
@jwt_required()
@viewer_required
def specific_port_desc(dpid, port_no):
    resp = requests.get(f"{RYU_BASE_URL}/stats/portdesc/{dpid}/{port_no}")
    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/flowentry/<string:cmd>", methods=["POST"])
@openflow_blp.response(200, description="Modify flow entries")
@jwt_required()
@operator_required
def flow_entry(cmd):
    data = request.get_json()
    resp = requests.post(f"{RYU_BASE_URL}/stats/flowentry/{cmd}", json=data)
    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/flowentry/clear/<string:dpid>", methods=["DELETE"])
@openflow_blp.response(200, description="Clear all flow entries")
@jwt_required()
@operator_required
def clear_flow_entries(dpid):
    resp = requests.delete(f"{RYU_BASE_URL}/stats/flowentry/clear/{dpid}")
    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/queue/<string:dpid>", methods=["GET"])
@openflow_blp.response(200, description="Get queue stats")
@jwt_required()
@viewer_required
def queue_stats(dpid):
    resp = requests.get(f"{RYU_BASE_URL}/stats/queue/{dpid}")
    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/queueconfig/<string:dpid>", methods=["GET"])
@openflow_blp.response(200, description="Get queue configuration")
@jwt_required()
@viewer_required
def queue_config(dpid):
    resp = requests.get(f"{RYU_BASE_URL}/stats/queueconfig/{dpid}")
    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/queuedesc/<string:dpid>", methods=["GET"])
@openflow_blp.response(200, description="Get queue descriptions")
@jwt_required()
@viewer_required
def queue_desc(dpid):
    resp = requests.get(f"{RYU_BASE_URL}/stats/queuedesc/{dpid}")
    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/meterfeatures/<string:dpid>", methods=["GET"])
@openflow_blp.response(200, description="Get meter features")
@jwt_required()
@viewer_required
def meter_features(dpid):
    resp = requests.get(f"{RYU_BASE_URL}/stats/meterfeatures/{dpid}")
    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/meterconfig/<string:dpid>", methods=["GET"])
@openflow_blp.response(200, description="Get meter configuration")
@jwt_required()
@viewer_required
def meter_config(dpid):
    resp = requests.get(f"{RYU_BASE_URL}/stats/meterconfig/{dpid}")
    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/meterdesc/<string:dpid>", methods=["GET"])
@openflow_blp.response(200, description="Get meter descriptions")
@jwt_required()
@viewer_required
def meter_desc(dpid):
    resp = requests.get(f"{RYU_BASE_URL}/stats/meterdesc/{dpid}")
    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/meter/<string:dpid>", methods=["GET"])
@openflow_blp.response(200, description="Get meter stats")
@jwt_required()
@viewer_required
def meter_stats(dpid):
    resp = requests.get(f"{RYU_BASE_URL}/stats/meter/{dpid}")
    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/groupfeatures/<string:dpid>", methods=["GET"])
@openflow_blp.response(200, description="Get group features")
@jwt_required()
@viewer_required
def group_features(dpid):
    resp = requests.get(f"{RYU_BASE_URL}/stats/groupfeatures/{dpid}")
    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/groupdesc/<string:dpid>", methods=["GET"])
@openflow_blp.response(200, description="Get group descriptions")
@jwt_required()
@viewer_required
def group_desc(dpid):
    resp = requests.get(f"{RYU_BASE_URL}/stats/groupdesc/{dpid}")
    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/group/<string:dpid>", methods=["GET"])
@openflow_blp.response(200, description="Get group stats")
@jwt_required()
@viewer_required
def group_stats(dpid):
    resp = requests.get(f"{RYU_BASE_URL}/stats/group/{dpid}")
    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/meterentry/<string:cmd>", methods=["POST"])
@openflow_blp.response(200, description="Modify meter entries")
@jwt_required()
@operator_required
def meter_entry(cmd):
    data = request.get_json()
    resp = requests.post(f"{RYU_BASE_URL}/stats/meterentry/{cmd}", json=data)
    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/groupentry/<string:cmd>", methods=["POST"])
@openflow_blp.response(200, description="Modify group entries")
@jwt_required()
@operator_required
def group_entry(cmd):
    data = request.get_json()
    resp = requests.post(f"{RYU_BASE_URL}/stats/groupentry/{cmd}", json=data)
    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/portdesc/<string:cmd>", methods=["POST"])
@openflow_blp.response(200, description="Modify port behavior")
@jwt_required()
@operator_required
def modify_port(cmd):
    data = request.get_json()
    resp = requests.post(f"{RYU_BASE_URL}/stats/portdesc/{cmd}", json=data)
    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/role/<string:dpid>", methods=["GET"])
@openflow_blp.response(200, description="Get controller role")
@jwt_required()
@viewer_required
def get_role(dpid):
    resp = requests.get(f"{RYU_BASE_URL}/stats/role/{dpid}")
    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/role", methods=["POST"])
@openflow_blp.response(200, description="Set controller role")
@jwt_required()
@operator_required
def set_role():
    data = request.get_json()
    resp = requests.post(f"{RYU_BASE_URL}/stats/role", json=data)
    resp.raise_for_status()
    return resp.json()

# Add topology API
@openflow_blp.route("/topology/switches", methods=["GET"])
@openflow_blp.response(200, description="Get all switches in the topology")
@jwt_required()
@viewer_required
def get_topology_switches():
    resp = requests.get(f"{RYU_BASE_URL}/v1.0/topology/switches")
    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/topology/links", methods=["GET"])
@openflow_blp.response(200, description="Get all links in the topology")
@jwt_required()
@viewer_required
def get_topology_links():
    resp = requests.get(f"{RYU_BASE_URL}/v1.0/topology/links")
    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/topology/hosts", methods=["GET"])
@openflow_blp.response(200, description="Get all hosts in the topology")
@jwt_required()
@viewer_required
def get_topology_hosts():
    resp = requests.get(f"{RYU_BASE_URL}/v1.0/topology/hosts")
    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/meterconfig/<string:dpid>/<string:meter_id>", methods=["GET"])
@openflow_blp.response(200, description="Get specific meter configuration")
@jwt_required()
@viewer_required
def specific_meter_config(dpid, meter_id):
    resp = requests.get(f"{RYU_BASE_URL}/stats/meterconfig/{dpid}/{meter_id}")
    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/meterdesc/<string:dpid>/<string:meter_id>", methods=["GET"])
@openflow_blp.response(200, description="Get specific meter description")
@jwt_required()
@viewer_required
def specific_meter_desc(dpid, meter_id):
    resp = requests.get(f"{RYU_BASE_URL}/stats/meterdesc/{dpid}/{meter_id}")
    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/meter/<string:dpid>/<string:meter_id>", methods=["GET"])
@openflow_blp.response(200, description="Get specific meter stats")
@jwt_required()
@viewer_required
def specific_meter_stats(dpid, meter_id):
    resp = requests.get(f"{RYU_BASE_URL}/stats/meter/{dpid}/{meter_id}")
    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/groupdesc/<string:dpid>/<string:group_id>", methods=["GET"])
@openflow_blp.response(200, description="Get specific group description")
@jwt_required()
@viewer_required
def specific_group_desc(dpid, group_id):
    resp = requests.get(f"{RYU_BASE_URL}/stats/groupdesc/{dpid}/{group_id}")
    resp.raise_for_status()
    return resp.json()

@openflow_blp.route("/group/<string:dpid>/<string:group_id>", methods=["GET"])
@openflow_blp.response(200, description="Get specific group stats")
@jwt_required()
@viewer_required
def specific_group_stats(dpid, group_id):
    resp = requests.get(f"{RYU_BASE_URL}/stats/group/{dpid}/{group_id}")
    resp.raise_for_status()
    return resp.json()