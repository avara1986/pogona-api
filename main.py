from google.appengine.api import mail
from google.appengine.ext import db
from webapp2_extras import json

import os
import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Email(db.Model):
    to = db.StringProperty()
    subject = db.StringProperty()
    content = db.StringProperty()


class MainPage(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())


class Createmail(webapp2.RequestHandler):

    def options(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers[
            'Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers[
            'Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

    def get(self):
        save = True
        msg_error = ""
        if len(self.request.get('subject')) > 0:
            subject = self.request.get('subject')
        else:
            save = False
            msg_error = "No se envio asunto"
        if save is True and len(self.request.get('to')) > 0:
            to = self.request.get('to')
        else:
            save = False
            msg_error = "No se envio destinatario"

        if save is True:
            email = Email(to=subject,
                          subject=to)
            email.put()
            obj = {
                'success': True,
                'msg': '',
                'id': str(email.key()),
            }
        else:
            obj = {
                'success': False,
                'msg': msg_error,
            }
        self.response.content_type = 'application/json'
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.write(json.encode(obj))


class Chunkmail(webapp2.RequestHandler):

    def options(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers[
            'Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers[
            'Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

    def get(self):
        q = Email.all()
        try:
            q.filter(
                "__key__ =", db.Key(self.request.get('i')))
            email = q.get()
            if email.content is None:
                email.content = self.request.get('content')
            else:
                email.content = email.content.join(self.request.get('content'))
            email.put()
            obj = {
                'success': True,
                'msg': '',
                'id': str(email.key()),
                'to': email.to,
                'subject': email.subject,
                'content': email.content,
            }
        except db.datastore_errors.BadKeyError:
            obj = {
                'success': False,
                'msg': "no existe",
            }
        self.response.content_type = 'application/json'
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.write(json.encode(obj))


class SendChunkMail(webapp2.RequestHandler):

    def options(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers[
            'Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers[
            'Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

    def get(self):
        q = Email.all()
        try:
            q.filter(
                "__key__ =", db.Key(self.request.get('i')))
            email = q.get()
            obj = {
                'success': True,
                'msg': '',
                'id': str(email.key()),
                'to': email.to,
                'subject': email.subject,
                'content': email.content,
            }
        except db.datastore_errors.BadKeyError:
            obj = {
                'success': False,
                'msg': "no existe",
            }
        self.response.content_type = 'application/json'
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.write(json.encode(obj))

    def post(self):
        q = Email.all()
        try:
            q.filter(
                "__key__ =", db.Key(self.request.get('i')))
            email = q.get()
            send = True
            msg_error = ""
            if len(email.subject) > 0:
                message = mail.EmailMessage(sender="Pogona Test Emailing <a.vara.1986@gmail.com>",
                                            subject=email.subject)
            else:
                send = False
                msg_error = "No se envio asunto"
            if send is True and len(email.to) > 0:
                message.to = email.to
            else:
                send = False
                msg_error = "No se envio destinatario"
            if send is True and len(email.content) > 0:
                message.html = email.content

            else:
                send = False
                msg_error = "No se envio contenido"

            if send is True:
                message.send()
                obj = {
                    'success': True,
                    'msg': 'Envio ok',
                }
            else:
                obj = {
                    'success': False,
                    'msg': msg_error,
                }
        except db.datastore_errors.BadKeyError:
            obj = {
                'success': False,
                'msg': "no existe",
            }

        self.response.content_type = 'application/json'
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.write(json.encode(obj))


class Sendmail(webapp2.RequestHandler):

    def options(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers[
            'Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers[
            'Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

    def post(self):
        self.response.content_type = 'application/json'
        send = True
        msg_error = ""
        if len(self.request.get('subject')) > 0:
            message = mail.EmailMessage(sender="Pogona Test Emailing <a.vara.1986@gmail.com>",
                                        subject=self.request.get('subject'))
        else:
            send = False
            msg_error = "No se envio asunto"
        if send is True and len(self.request.get('to')) > 0:
            message.to = self.request.get('to')
        else:
            send = False
            msg_error = "No se envio destinatario"
        if send is True and len(self.request.get('content')) > 0:
            message.html = self.request.get('content')

        else:
            send = False
            msg_error = "No se envio contenido"

        if send is True:
            message.send()
            obj = {
                'success': True,
                'msg': 'Envio ok',
            }
        else:
            obj = {
                'success': False,
                'msg': msg_error,
            }
        self.response.headers.add_header(
            'Access-Control-Allow-Origin', '*')
        self.response.write(json.encode(obj))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/create-mail', Createmail),
    ('/chunk-content', Chunkmail),
    ('/send-email-chunked', SendChunkMail),
    ('/send-mail', Sendmail)
], debug=True)
