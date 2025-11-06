def validate_switch_data(data):
    """Validate logical switch data."""
    required_fields = ['name']
    
    if not isinstance(data, dict):
        return "Data must be a dictionary"
    
    for field in required_fields:
        if field not in data:
            return f"Missing required field: {field}"
        
        if not isinstance(data[field], str):
            return f"Field {field} must be a string"
        
        if not data[field].strip():
            return f"Field {field} cannot be empty"
    
    return None

def validate_router_data(data):
    """Validate logical router data."""
    required_fields = ['name']
    
    if not isinstance(data, dict):
        return "Data must be a dictionary"
    
    for field in required_fields:
        if field not in data:
            return f"Missing required field: {field}"
        
        if not isinstance(data[field], str):
            return f"Field {field} must be a string"
        
        if not data[field].strip():
            return f"Field {field} cannot be empty"
    
    return None

def validate_port_data(data):
    """Validate port data."""
    required_fields = ['name', 'type']
    
    if not isinstance(data, dict):
        return "Data must be a dictionary"
    
    for field in required_fields:
        if field not in data:
            return f"Missing required field: {field}"
        
        if not isinstance(data[field], str):
            return f"Field {field} must be a string"
        
        if not data[field].strip():
            return f"Field {field} cannot be empty"
    
    return None

def validate_acl_data(data):
    """Validate ACL data."""
    required_fields = ['match']
    
    if not isinstance(data, dict):
        return "Data must be a dictionary"
    
    for field in required_fields:
        if field not in data:
            return f"Missing required field: {field}"
        
        if not isinstance(data[field], str):
            return f"Field {field} must be a string"
        
        if not data[field].strip():
            return f"Field {field} cannot be empty"
    
    return None

def validate_load_balancer_data(data):
    """Validate load balancer data."""
    required_fields = ['name', 'vip', 'protocol']
    
    if not isinstance(data, dict):
        return "Data must be a dictionary"
    
    for field in required_fields:
        if field not in data:
            return f"Missing required field: {field}"
        
        if not isinstance(data[field], str):
            return f"Field {field} must be a string"
        
        if not data[field].strip():
            return f"Field {field} cannot be empty"
    
    return None
