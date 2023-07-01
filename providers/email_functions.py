import smtplib
import email.message
import os
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, select_autoescape, PackageLoader

env = Environment(
    loader=PackageLoader(package_name='main', package_path='./providers'),
    autoescape=select_autoescape(['html', 'xml'])
)

def auth_email(receiver, nome, link):
    
    try:
        '''
        Receiver_list: tupla com os destinatários
        Subject: Assunto do email
        Message: Corpo do e-mail
        '''
        template = env.get_template('auth_email.html')
        html = template.render(
            link=link,
            nome=nome,
        )

        msg = email.message.Message()
        msg['Subject'] = 'Confirme o seu e-mail'
        msg['From'] = os.environ['EMAIL_ACCOUNT']
        msg['To'] = receiver
        password = os.environ['EMAIL_PASSWORD']
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(html)

        s = smtplib.SMTP('smtp.hostinger.com: 587')
        s.starttls()
        s.login(msg['From'], password)
        s.sendmail(msg['From'], msg['To'], msg.as_string().encode('utf-8'))

        print('email enviado')
        return True
    except Exception as error:
        print(str(error))
        return False

def new_password_email(receiver, nome, link):
    
    try:
        '''
        Receiver_list: tupla com os destinatários
        Subject: Assunto do email
        Message: Corpo do e-mail
        '''
        template = env.get_template('new_password_email.html')
        html = template.render(
            link=link,
            nome=nome,
        )

        msg = email.message.Message()
        msg['Subject'] = 'Alteração de senha'
        msg['From'] = os.environ['EMAIL_ACCOUNT']
        msg['To'] = receiver
        password = os.environ['EMAIL_PASSWORD']
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(html)

        s = smtplib.SMTP('smtp.hostinger.com: 587')
        s.starttls()
        s.login(msg['From'], password)
        s.sendmail(msg['From'], msg['To'], msg.as_string().encode('utf-8'))

        print('email enviado')
        return True
    except Exception as error:
        print(str(error))
        return False