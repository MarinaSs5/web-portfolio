import flask_mail
import application





application.handle.config['MAIL_SERVER'] = 'mail.hosting.reg.ru'
application.handle.config['MAIL_PORT'] = 465
application.handle.config['MAIL_USE_SSL'] = True
application.handle.config['MAIL_USERNAME'] = 'noreply@lingfolio.ru'
application.handle.config['MAIL_PASSWORD'] = 'yZ7rH9iN9fgT5fK6'

handle = flask_mail.Mail(application.handle)

def send_message(caption, html, address):
    message = flask_mail.Message(caption, sender = application.handle.config['MAIL_USERNAME'], recipients = [address])
    message.body = message.html = html
    with application.handle.app_context():
        handle.send(message)