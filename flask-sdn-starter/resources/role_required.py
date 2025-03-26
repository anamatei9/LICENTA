from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps
from flask_smorest import abort

def role_required(allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get("role", "viewer")

            if user_role not in allowed_roles:
                abort(403, message="You are not authorized to access this resource.")

            return fn(*args, **kwargs)
        return wrapper
    return decorator

viewer_required = role_required(["viewer", "operator", "admin"])
operator_required = role_required(["operator", "admin"])
admin_required = role_required(["admin"])
