from app import db
from datetime import datetime
import bleach
from markdown import markdown

class Text(db.Model):
    __tablename__ = 'texts'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(64))
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)

    @staticmethod
    def on_changed_body(target,value,oldvalue,initator):
        target.body_html = bleach.linkify(markdown(value,output_formal='html5'))

db.event.listen(Text.body,'set',Text.on_changed_body)
