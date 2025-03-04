from django.core.cache import caches
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView, DetailView
from .models import Course, CourseCategory, Vacancie
from accounts.models import *


class HomeView(View):

    def get(self, request):
        return render(request, 'courses/home.html')
        

@method_decorator(login_required(login_url='login_view'), name='dispatch')
class CoursesListView(ListView):
    model = Course
    template_name = 'courses/courses_list.html'
    context_object_name = 'courses' 
    paginate_by = 3

    def get_queryset(self):
        courses_cache = caches['courses_cache']
        cache_key = 'courses_list'
        queryset = courses_cache.get(cache_key)
        search = self.request.GET.get('search')
        category = self.request.GET.get('category')

        if not queryset:
            queryset = super().get_queryset().order_by('course_category')
            courses_cache.set(cache_key, queryset, timeout=3600)
        if search:
            queryset = queryset.filter(course_name__icontains=search)
        if category:
            queryset = queryset.filter(course_category_id=category)
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = CourseCategory.objects.all()
        category_id = self.request.GET.get('category')
        if category_id:
            context['selected_category'] = CourseCategory.objects.get(id=category_id)
        else:
            context['selected_category'] = None
        return context


@method_decorator(login_required(login_url='login_view'), name='dispatch')
class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'

    def get_object(self, queryset=None):
        courses_cache = caches['courses_cache']
        cache_key = f'course_detail_{self.kwargs["pk"]}'
        course = courses_cache.get(cache_key)

        if not course:
            course = super().get_object(queryset)
            courses_cache.set(cache_key, course, timeout=3600)

        return course


@method_decorator(login_required(login_url='login_view'), name='dispatch')
class VacanciesListView(ListView):
    model = Vacancie
    template_name = 'courses/vacancies_list.html'
    context_object_name = 'vacancies' 
    paginate_by = 3

    def get_queryset(self):
        courses_cache = caches['courses_cache']
        cache_key = 'vacancies_list'
        queryset = courses_cache.get(cache_key)

        if not queryset:
            queryset = super().get_queryset().order_by('vacancy_category')
            category = self.request.GET.get('category')
            if category:
                queryset = queryset.filter(vacancy_category_id=category)
            courses_cache.set(cache_key, queryset, timeout=3600)
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = CourseCategory.objects.all()
        category_id = self.request.GET.get('category')
        if category_id:
            context['selected_category'] = CourseCategory.objects.get(id=category_id)
        else:
            context['selected_category'] = None
        return context
