from django.db import models
from courses.models import Course
from django.contrib.auth.models import AbstractUser
from multipleselectionfield import MultipleSelectionField
import uuid

    
class CustomUser(AbstractUser):

    choices_education = (
        ('Fundamental Completo', 'Fundamental Completo'),
        ('Fundamental em Andamento', 'Fundamental em Andamento'),
        ('Fundamental Incompleto', 'Fundamental Incompleto'),
        ('Médio Completo', 'Médio Completo'),
        ('Médio em Andamento', 'Médio em Andamento'),
        ('Médio Incompleto', 'Médio Incompleto'),
        ('Superior Completo', 'Superior Completo'),
        ('Superior em Andamento', 'Superior em Andamento'),
        ('Superior Incompleto', 'Superior Incompleto')
    )

    choices_areas = (
        ('Administração', 'Administração'),
        ('Contabilidade', 'Contabilidade'),
        ('Direito', 'Direito'),
        ('Economia', 'Economia'),
        ('Estética', 'Estetica'),
        ('Finanças', 'Finanças'),
        ('Gastronomia', 'Gastronomia'),
        ('Humanidades', 'Humanidades'),
        ('Linguagens', 'Linguagens'),
        ('Massoterapia', 'Massoterapia'),
        ('Saúde', 'Saúde'),
        ('Tecnologia da Informação', 'Tecnologia da Informação')
    )

    full_name = models.CharField(max_length=50, null=False, blank=False, verbose_name='Nome Completo')
    cpf = models.CharField(max_length=14, verbose_name='CPF', blank=False, null=False) 
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Data de Nascimento')
    email = models.EmailField(max_length=100, blank=False, null=False)
    email_verified = models.BooleanField(null=True, blank=True, default=False, verbose_name='Email Verificado')
    verification_code = models.UUIDField(null=True, blank=True, default=uuid.uuid4, editable=False, verbose_name='Código')
    telephone = models.CharField(max_length=16, blank=False, null=False, verbose_name='Telefone')
    zip_code = models.CharField(max_length=9, blank=False, null=False, verbose_name='CEP')
    address = models.CharField(max_length=50, blank=False, null=False, verbose_name='Endereço')
    number = models.IntegerField(blank=True, null=True, verbose_name='Número')
    neighborhood = models.CharField(max_length=50, blank=False, null=False, verbose_name='Bairro')
    city = models.CharField(max_length=50, null=False, blank=False, verbose_name='Cidade')
    state = models.CharField(max_length=2, null=False, blank=False, verbose_name='Estado')
    education = models.CharField(max_length=30, choices=choices_education, verbose_name='Escolaridade')
    areas_of_interest = MultipleSelectionField(blank=True, null=True, choices=choices_areas, max_length=50, verbose_name='Áreas de Interesse')
    photo = models.ImageField(upload_to='profile/', blank=True, null=True)
    user_courses = models.ManyToManyField(Course, related_name='courses')

    def __str__(self):
        return self.username
    
    


