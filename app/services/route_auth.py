from app.services.admin_log import admin_log
from app.api.depends.mem_session import mem_session

mem_session = {"admin": ['', 'admin:user:main', 'admin:power:main', 'admin:role:main', 'admin:monitor:main', 'admin:log:index', '', 'admin:file:main', 'admin:power:add', 'admin:user:add', 'admin:user:edit', 'admin:user:remove', 'admin:power:edit', 'admin:power:remove', 'admin:role:add', 'admin:role:edit', 'admin:role:remove', 'admin:role:power', 'admin:file:add', 'admin:file:delete']}

def authorize(power: str, user):
    if not power in mem_session.get(user.username, []):
        return False
    return True

def authorize_and_log(power: str, user, request):
    if not power in mem_session.get(user.username, []):
        admin_log(request=request, uid=user.id, is_access=False)
        return False
    admin_log(request=request, uid=user.id, is_access=True)
    return True
