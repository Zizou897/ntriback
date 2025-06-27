
from web.models import Journal
from .get_ip import get_client_ip



def log_action(request, action, description):
    ip = get_client_ip(request)
    agent = request.META.get("HTTP_USER_AGENT", "inconnu")
    user = request.user if request.user.is_authenticated else None
    
    Journal.objects.create(
        user=user,
        action=action,
        description=description,
        ip_address=ip,
        user_agent=agent
    )