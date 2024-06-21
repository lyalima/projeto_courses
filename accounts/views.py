from django.shortcuts import render, redirect
from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView, FormView
from django.views.generic import View
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import CustomUser
from courses.models import Course, CourseCategory
from django.http import JsonResponse
import requests
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.http import HttpResponse


class RegisterView(CreateView):

    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('verify_email_view')

    def form_valid(self, form):

        response = super().form_valid(form)
        form.save()

        return response

class VerifyEmailView(FormView):

    template_name = 'accounts/verify_email.html'
    form_class = VerificationForm
    success_url = reverse_lazy('login_view')

    def form_valid(self, form):

        code = form.cleaned_data.get('code')

        try:

            user = CustomUser.objects.get(verification_code=code)
            user.email_verified = True
            user.save()
            messages.success(self.request, 'Usuário cadastrado e Email verificado com sucesso!')

            return super().form_valid(form)
        
        except:

            messages.error(self.request, 'Código de verificação inválido.')
            
            return self.form_invalid(form)
    
class LoginView(View):

    def get(self, request):

        form = CustomAuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):

        form = CustomAuthenticationForm(data=request.POST)

        if form.is_valid():

            login(request, form.get_user())

            return redirect(reverse_lazy('courses_list_view'))
        
        return render(request, 'accounts/login.html', {'form': form})
    
class MyPasswordResetConfirm(PasswordResetConfirmView):

    def form_valid(self, form):

        self.user.is_active = True
        self.user.save()

        return super(MyPasswordResetConfirm, self).form_valid(form)
    
    template_name = 'accounts/password_reset_confirm.html'

class MyPasswordResetComplete(PasswordResetCompleteView):

    template_name = 'accounts/password_reset_complete.html'

class MyPasswordReset(PasswordResetView):

    template_name = 'accounts/password_reset_form.html'

class MyPasswordResetDone(PasswordResetDoneView):

    template_name = 'accounts/password_reset_done.html'

class LogoutView(View):

    def get(self, request):

        logout(request)

        return redirect('home_view')
    
class ProfileView(DetailView):

    model = CustomUser
    template_name = 'accounts/profile.html'

class ProfileUpdateView(UpdateView):

    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'accounts/update_profile.html'

    def get_success_url(self):

        return reverse_lazy('profile_detail_view', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):

        response = super().form_valid(form)
        messages.success(self.request, 'Dados atualizados com sucesso!')

        return response
    
class AddCourseView(View):

    def post(self, request, course_id):

        course = Course.objects.get(pk=course_id)
        request.user.user_courses.add(course)
        messages.info(request, f'Curso "{course.course_name}" adicionado com sucesso!')

        return redirect('my_courses_list_view')

class MyCoursesListView(LoginRequiredMixin, ListView):

    model = CustomUser
    template_name = 'accounts/my_courses.html'
    context_object_name = 'courses'
    paginate_by = 3


    def get_queryset(self):

        user = self.request.user
        queryset = user.user_courses.all().order_by('course_category')
        search = self.request.GET.get('search')
        category = self.request.GET.get('category')

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

class UserCourseDetailView(DetailView):

    model = Course
    template_name = 'accounts/user_course_detail.html'
    context_object_name = 'course'

class UserCourseDeleteView(DeleteView):

    model = CustomUser
    template_name = 'accounts/user_course_delete.html'
    success_url = '/my_courses_list_view/'

    def get_object(self, queryset=None):

        course_pk = self.kwargs.get("pk") 
        course = get_object_or_404(Course, pk=course_pk)  
        user_courses = self.request.user.user_courses.all()  
        
        if course not in user_courses:

            raise Http404(f"Curso não encontrado.")

        return course

    def post(self, request, *args, **kwargs):

        user = self.request.user
        course_pk = self.kwargs.get("pk")  
        course = Course.objects.get(pk=course_pk)  
        user.user_courses.remove(course)  
        messages.error(request, f'Curso "{course.course_name}" excluído com sucesso!')

        return redirect('my_courses_list_view')
    
def check_zipcode_view(request):

    if request.method == 'GET':
        
        cep = request.GET.get('cep', None)

        if cep:

            url = f'https://viacep.com.br/ws/{cep}/json/'
            response = requests.get(url)
            data = response.json()

            if 'erro' not in data:

                data = {
                    'logradouro': data.get('logradouro', ''),
                    'bairro': data.get('bairro', ''),
                    'cidade': data.get('localidade', ''),
                    'estado': data.get('uf', ''),
                }

                return JsonResponse(data)
            
    return JsonResponse({'error': 'CEP inválido'}, status=400)


#view para verificação de integridade feita pelo asg aws:
def health_check(request):
    
    return HttpResponse("OK", status=200)