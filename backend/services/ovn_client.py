import subprocess
import json
import os
from typing import Dict, List, Optional

class OVNClient:
    def __init__(self):
        # Use the correct socket path for OVN
        self.nb_db = os.getenv('OVN_NB_DB', "unix:/var/run/ovn/ovnnb_db.sock")

    def _check_ovn_status(self) -> bool:
        """Check if OVN services are running"""
        try:
            subprocess.run(["ovn-nbctl", "show"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def _execute_ovn_command(self, command: List[str]) -> str:
        if not self._check_ovn_status():
            raise Exception("OVN services are not running or not properly configured")
            
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise Exception(f"OVN command failed: {e.stderr}")
        except FileNotFoundError:
            raise Exception("OVN commands not found. Please ensure OVN is properly installed")

    def get_logical_switches(self) -> List[Dict]:
        command = ["ovn-nbctl", "--format=json", "ls-list"]
        output = self._execute_ovn_command(command)
        return json.loads(output)

    def get_logical_switch(self, switch_id: str) -> Optional[Dict]:
        command = ["ovn-nbctl", "--format=json", "ls-get", switch_id]
        try:
            output = self._execute_ovn_command(command)
            return json.loads(output)
        except Exception:
            return None

    def create_logical_switch(self, switch_data: Dict) -> Dict:
        name = switch_data.get("name")
        if not name:
            raise ValueError("Switch name is required")

        command = ["ovn-nbctl", "ls-add", name]
        
        # Add optional parameters
        if "external_ids" in switch_data:
            for key, value in switch_data["external_ids"].items():
                command.extend(["--", "set", "Logical_Switch", name,
                              f"external_ids:{key}={value}"])

        self._execute_ovn_command(command)
        return self.get_logical_switch(name)

    def update_logical_switch(self, switch_id: str, switch_data: Dict) -> Optional[Dict]:
        if not self.get_logical_switch(switch_id):
            return None

        command = ["ovn-nbctl"]
        
        if "external_ids" in switch_data:
            for key, value in switch_data["external_ids"].items():
                command.extend(["set", "Logical_Switch", switch_id,
                              f"external_ids:{key}={value}"])

        self._execute_ovn_command(command)
        return self.get_logical_switch(switch_id)

    def delete_logical_switch(self, switch_id: str) -> bool:
        if not self.get_logical_switch(switch_id):
            return False

        command = ["ovn-nbctl", "ls-del", switch_id]
        self._execute_ovn_command(command)
        return True

    def get_switch_ports(self, switch_id: str) -> List[Dict]:
        command = ["ovn-nbctl", "--format=json", "lsp-list", switch_id]
        try:
            output = self._execute_ovn_command(command)
            return json.loads(output)
        except Exception:
            return []

    # Additional methods for other OVN operations can be added here
    def get_logical_routers(self) -> List[Dict]:
        command = ["ovn-nbctl", "--format=json", "lr-list"]
        output = self._execute_ovn_command(command)
        return json.loads(output)

    def create_logical_router(self, router_data: Dict) -> Dict:
        name = router_data.get("name")
        if not name:
            raise ValueError("Router name is required")

        command = ["ovn-nbctl", "lr-add", name]
        self._execute_ovn_command(command)
        return {"name": name, "id": name}

    def get_logical_router(self, router_id: str) -> Optional[Dict]:
        command = ["ovn-nbctl", "--format=json", "lr-get", router_id]
        try:
            output = self._execute_ovn_command(command)
            return json.loads(output)
        except Exception:
            return None

    def update_logical_router(self, router_id: str, router_data: Dict) -> Optional[Dict]:
        if not self.get_logical_router(router_id):
            return None

        command = ["ovn-nbctl"]
        
        if "external_ids" in router_data:
            for key, value in router_data["external_ids"].items():
                command.extend(["set", "Logical_Router", router_id,
                              f"external_ids:{key}={value}"])

        if len(command) > 1:
            self._execute_ovn_command(command)
        return self.get_logical_router(router_id)

    def delete_logical_router(self, router_id: str) -> bool:
        if not self.get_logical_router(router_id):
            return False

        command = ["ovn-nbctl", "lr-del", router_id]
        self._execute_ovn_command(command)
        return True

    def get_router_ports(self, router_id: str) -> List[Dict]:
        command = ["ovn-nbctl", "--format=json", "lrp-list", router_id]
        try:
            output = self._execute_ovn_command(command)
            return json.loads(output)
        except Exception:
            return []

    def get_acls(self) -> List[Dict]:
        """Get all ACLs across all switches"""
        try:
            switches = self.get_logical_switches()
            all_acls = []
            for switch in switches:
                switch_name = switch.get("name", "")
                if switch_name:
                    acls = self.get_switch_acls(switch_name)
                    all_acls.extend(acls)
            return all_acls
        except Exception:
            return []

    def get_switch_acls(self, switch_id: str) -> List[Dict]:
        command = ["ovn-nbctl", "--format=json", "acl-list", switch_id]
        try:
            output = self._execute_ovn_command(command)
            return json.loads(output)
        except Exception:
            return []

    def create_acl(self, switch_id: str, acl_data: Dict) -> Dict:
        direction = acl_data.get("direction", "to-lport")
        priority = acl_data.get("priority", "1000")
        match = acl_data.get("match")
        action = acl_data.get("action", "allow")

        if not all([switch_id, match]):
            raise ValueError("Switch ID and match criteria are required")

        command = [
            "ovn-nbctl", "acl-add", switch_id,
            direction, priority, match, action
        ]
        self._execute_ovn_command(command)
        return acl_data

    def delete_acl(self, switch_id: str, acl_id: str) -> bool:
        """Delete an ACL by its ID"""
        try:
            command = ["ovn-nbctl", "acl-del", switch_id, acl_id]
            self._execute_ovn_command(command)
            return True
        except Exception:
            return False

    def get_load_balancers(self) -> List[Dict]:
        command = ["ovn-nbctl", "--format=json", "lb-list"]
        try:
            output = self._execute_ovn_command(command)
            return json.loads(output)
        except Exception:
            return []

    def get_load_balancer(self, lb_id: str) -> Optional[Dict]:
        command = ["ovn-nbctl", "--format=json", "lb-get", lb_id]
        try:
            output = self._execute_ovn_command(command)
            return json.loads(output)
        except Exception:
            return None

    def create_load_balancer(self, lb_data: Dict) -> Dict:
        name = lb_data.get("name")
        vip = lb_data.get("vip")
        protocol = lb_data.get("protocol", "tcp")
        
        if not name or not vip:
            raise ValueError("Load balancer name and VIP are required")

        command = ["ovn-nbctl", "lb-add", name, vip, "", protocol]
        self._execute_ovn_command(command)
        return {"name": name, "id": name, "vip": vip, "protocol": protocol}

    def update_load_balancer(self, lb_id: str, lb_data: Dict) -> Optional[Dict]:
        if not self.get_load_balancer(lb_id):
            return None

        # For simplicity, we'll just return the existing load balancer
        # In a real implementation, you would update the load balancer properties
        return self.get_load_balancer(lb_id)

    def delete_load_balancer(self, lb_id: str) -> bool:
        if not self.get_load_balancer(lb_id):
            return False

        command = ["ovn-nbctl", "lb-del", lb_id]
        self._execute_ovn_command(command)
        return True

    def get_all_ports(self) -> List[Dict]:
        """Get all ports across all switches"""
        try:
            switches = self.get_logical_switches()
            all_ports = []
            for switch in switches:
                switch_name = switch.get("name", "")
                if switch_name:
                    ports = self.get_switch_ports(switch_name)
                    all_ports.extend(ports)
            return all_ports
        except Exception:
            return []

    def get_port(self, port_id: str) -> Optional[Dict]:
        command = ["ovn-nbctl", "--format=json", "lsp-get", port_id]
        try:
            output = self._execute_ovn_command(command)
            return json.loads(output)
        except Exception:
            return None

    def create_port(self, port_data: Dict) -> Dict:
        name = port_data.get("name")
        switch_id = port_data.get("switch_id")
        
        if not name or not switch_id:
            raise ValueError("Port name and switch ID are required")

        command = ["ovn-nbctl", "lsp-add", switch_id, name]
        self._execute_ovn_command(command)
        
        # Set port type if specified
        port_type = port_data.get("type")
        if port_type:
            command = ["ovn-nbctl", "lsp-set-type", name, port_type]
            self._execute_ovn_command(command)
        
        # Set addresses if specified
        addresses = port_data.get("addresses")
        if addresses:
            command = ["ovn-nbctl", "lsp-set-addresses", name, addresses]
            self._execute_ovn_command(command)
        
        return {"name": name, "id": name, "switch_id": switch_id}

    def update_port(self, port_id: str, port_data: Dict) -> Optional[Dict]:
        if not self.get_port(port_id):
            return None

        # Update port properties
        port_type = port_data.get("type")
        if port_type:
            command = ["ovn-nbctl", "lsp-set-type", port_id, port_type]
            self._execute_ovn_command(command)
        
        addresses = port_data.get("addresses")
        if addresses:
            command = ["ovn-nbctl", "lsp-set-addresses", port_id, addresses]
            self._execute_ovn_command(command)
        
        return self.get_port(port_id)

    def delete_port(self, port_id: str) -> bool:
        if not self.get_port(port_id):
            return False

        command = ["ovn-nbctl", "lsp-del", port_id]
        self._execute_ovn_command(command)
        return True
