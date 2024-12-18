from celery import shared_task
from django.core.mail import send_mail
from decouple import config
from accounts.models import CustomUser
#from utils.email_code_generator import create_user_code


@shared_task
def send_verification_email(user_id, code):
    user = CustomUser.objects.get(pk=user_id)
    code = code
    subject = 'Verifique seu endereço de email'
    message = f'Use este código para verificar seu email: {code}'
    from_email = config('EMAIL_ADDRESS')
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)
    #create_user_code(user, code)

    return user_id
