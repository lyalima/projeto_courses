from django.core.mail import send_mail
import os


def send_verification_email(user):
    subject = 'Verifique seu endereço de email'
    message = f'Use este código para verificar seu email: {user.verification_code}'
    from_email = os.environ['EMAIL_ADDRESS']
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)
