from io import BytesIO
from fastapi.responses import StreamingResponse
from app.api.depends.mem_session import mem_session
from marshmallow import fields, Schema
from app.services.CaptchaTool import gen_captcha

# 生成验证码
def get_captcha():
    code, image = gen_captcha()
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = StreamingResponse(out, media_type="image/png")
    return resp, code

class PowerSchema(Schema):
    id = fields.Integer()
    title = fields.Str(attribute="name")
    type = fields.Str()
    code = fields.Str()
    href = fields.Str(attribute="url")
    open_type = fields.Str()
    parent_id = fields.Integer()
    icon = fields.Str()
    sort = fields.Integer()
    create_time = fields.DateTime()
    update_time = fields.DateTime()
    enable = fields.Integer()

# 授权路由存入session
def add_auth_session(current_user):
    role = current_user.role
    user_power = []
    for i in role:
        if i.enable == 0:
            continue
        for p in i.power:
            if p.enable == 0:
                continue
            user_power.append(p.code)
    mem_session[current_user.username] = user_power

def make_menu_tree(current_user):
    # power0 = Power.query.filter(
    #     Power.type == 0,
    # ).all()
    # power1 = Power.query.filter(
    #     Power.type == 1
    # ).all()
    role = current_user.role
    power0 = []
    power1 = []
    for i in role:
        if i.enable == 0:
            continue
        for p in i.power:
            if p.enable == 0:
                continue
            if int(p.type) == 0:
                power0.append(p)
            else:
                power1.append(p)

    # print(power0)
    # print(power1)
    power_schema = PowerSchema(many=True)  # 用已继承ma.ModelSchema类的自定制类生成序列化类
    power0_dict = power_schema.dump(power0)  # 生成可序列化对象
    power1_dict = power_schema.dump(power1)  # 生成可序列化对象
    power0_dict = sorted(power0_dict, key=lambda i: i['sort'])
    power1_dict = sorted(power1_dict, key=lambda i: i['sort'])
    

    menu = []

    for p0 in power0_dict:
        for p1 in power1_dict:
            if p0.get('id') == p1.get('parent_id'):
                if p0.get("children") is None:
                    p0['children'] = []
                p0['children'].append(p1)
        menu.append(p0)
    return menu