from fastapi_sqlalchemy import db
from app.models.admin import AdminLog
import json

def login_log(request, username, uid, is_access):
    info = {
        'method': request.method,
        'url': request.url.path,
        'ip': request.client.host,
        'user_agent': request.headers.get("user-agent"),
        'desc': username,
        'uid': uid,
        'success': int(is_access)

    }
    log = AdminLog(
        url=info.get('url'),
        ip=info.get('ip'),
        user_agent=info.get('user_agent'),
        desc=info.get('desc'),
        uid=info.get('uid'),
        method=info.get('method'),
        success = info.get('success')
    )
    db.session.add(log)
    db.session.flush()
    db.session.commit()
    return log.id

def admin_log(request, uid, is_access):
    info = {
        'method': request.method,
        'url': request.url.path,
        'ip': request.client.host,
        'user_agent': request.headers.get("user-agent"),
        'desc': str(dict(request.query_params)),
        'uid': uid,
        'success':int(is_access)

    }
    log = AdminLog(
        url=info.get('url'),
        ip=info.get('ip'),
        user_agent=info.get('user_agent'),
        desc=info.get('desc'),
        uid=info.get('uid'),
        method=info.get('method'),
        success=info.get('success')
    )
    db.session.add(log)
    db.session.commit()

    return log.id