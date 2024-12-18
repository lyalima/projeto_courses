import random
from accounts.tasks import send_verification_email
from accounts.models import CustomUser, UserEmailVerificationCode


def email_code_generator(user_id):
    code = random.randint(100000, 999999)
    send_verification_email.delay(user_id, code)
    create_user_code(user_id, code)


def create_user_code(user_id, code):
    user = CustomUser.objects.get(pk=user_id)
    UserEmailVerificationCode.objects.create(
        user=user,
        code=code
    )
