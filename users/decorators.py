from django.http import HttpResponse
from functools import wraps

def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user_role = request.user.userprofile.role

            if user_role != required_role:
                return HttpResponse("Acceso denegado: no tienes permisos.", status=403)

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


# Decoradores específicos para comodidad

def gerente_required(view_func):
    return role_required("gerente")(view_func)

def supervisor_required(view_func):
    return role_required("supervisor")(view_func)

def surtidor_required(view_func):
    return role_required("surtidor")(view_func)

def asistente_required(view_func):
    return role_required("asistente")(view_func)

def contador_required(view_func):
    return role_required("contador")(view_func)

def roles_required(allowed_roles):
    """
    Decorador que permite acceso solo si el usuario pertenece 
    a uno de los roles especificados.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user_role = request.user.userprofile.role

            if user_role not in allowed_roles:
                return HttpResponse("Acceso denegado: no tienes permisos.", status=403)

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator