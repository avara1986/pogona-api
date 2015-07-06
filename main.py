from google.appengine.api import mail
from webapp2_extras import json

import os
import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())


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
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.write(json.encode(obj))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/send-mail', Sendmail),
], debug=True)
