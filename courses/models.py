from django.db import models


class CourseCategory(models.Model):
    category_name = models.CharField(max_length=255)
    
    def __str__(self):
        return f'{self.category_name}'

class Course(models.Model):
    course_name = models.CharField(max_length=100, blank=False, null=False)
    course_category = models.ForeignKey(CourseCategory, on_delete=models.PROTECT, null=False, blank=False, related_name='course_category')
    course_workload = models.IntegerField(blank=False, null=False)
    teaching_plataform = models.CharField(max_length=100, blank=True, default='Desconhecido')
    photo = models.ImageField(upload_to='courses/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    course_link = models.URLField(max_length=100, blank=False, null=False, default='')

    def __str__(self):
        return f'{self.course_name} | {self.course_category}'
    
class Vacancie(models.Model):
    vacancy_link = models.URLField(max_length=100, blank=False, null=False)
    vacancy_category = models.ForeignKey(CourseCategory, on_delete=models.PROTECT, null=False, blank=False)
    vacancy_subcategory = models.CharField(max_length=30, null=True, blank=True)
    vacancy_site = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f'Vaga de {self.vacancy_category}. | {self.vacancy_subcategory} |  {self.vacancy_site}' 
