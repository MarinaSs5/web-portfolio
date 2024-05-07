import flask_mail
from misc import shared





shared.app.config['MAIL_SERVER'] = 'mail.hosting.reg.ru'
shared.app.config['MAIL_PORT'] = 465
shared.app.config['MAIL_USE_SSL'] = True
shared.app.config['MAIL_USERNAME'] = 'noreply@lingfolio.ru'
shared.app.config['MAIL_PASSWORD'] = 'yZ7rH9iN9fgT5fK6'

mail = flask_mail.Mail(shared.app)





def send_message(caption, html, address):
    message = flask_mail.Message(caption, sender = shared.app.config['MAIL_USERNAME'], recipients = [address])
    message.body = message.html = html
    with shared.app.app_context():
        mail.send(message)