import os
import time
from marshmallow import fields, Schema
from sqlalchemy import desc
from fastapi_sqlalchemy import db
from sqlalchemy.sql.expression import update
from app.models.admin import Photo

base_url = "app/resources/static/upload/"

class PhotoSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    href = fields.Str()
    mime = fields.Str()
    size = fields.Str()
    ext = fields.Str()
    create_time = fields.DateTime()


def get_photo(page, limit):
    photo = db.session.query(Photo).order_by(desc(Photo.create_time)).offset(page-1).limit(limit).all()
    count = db.session.query(Photo).count()
    role_schema = PhotoSchema(many=True)
    output = role_schema.dump(photo)
    return output, count


def upload_one(photo, mime):
    filename = "".join(photo.filename.split(".")[:-1]) + "_" + str(int(time.time())) + "." + mime.split("/")[-1]
    with open(base_url + filename, "wb") as f:
        f.write(photo.file.read())
    file_url = "/static/upload/" + filename

    size = os.path.getsize(base_url + filename)
    photo = Photo(name=filename, href=file_url, mime=mime, size=size)
    db.session.add(photo)
    db.session.commit()
    return file_url

def delete_photo_by_id(id):
    photo_name = db.session.query(Photo).filter_by(id=id).first().name
    photo = db.session.query(Photo).filter_by(id=id).delete()
    db.session.commit()
    os.remove(base_url + photo_name)
    return photo

def batchRemove(ids):
    photo_name = db.session.query(Photo).filter(Photo.id.in_(ids)).all()
    photo = db.session.query(Photo).filter(Photo.id.in_(ids)).delete(synchronize_session=False)
    db.session.commit()
    for p in photo_name:
        os.remove(base_url + p.name)
    return photo