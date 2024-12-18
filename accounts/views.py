from django.shortcuts import render, redirect
from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, UpdateView, DetailView, ListView, DeleteView, FormView
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm, CustomUserAuthenticationForm, CustomUserVerificationForm, CustomUserChangeForm
from .models import CustomUser, UserEmailVerificationCode
from utils.email_code_generator import email_code_generator
from courses.models import Course, CourseCategory
from django.http import JsonResponse
import requests
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login_view')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Cadastro realizado com sucesso!')

        return super().form_valid(form)


class LoginView(View):

    def get(self, request):
        form = CustomUserAuthenticationForm
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = CustomUserAuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(reverse_lazy('courses_list_view'))
        return render(request, 'accounts/login.html', {'form': form})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('home_view')


@method_decorator(login_required(login_url='login_view'), name='dispatch')
class VerifyEmailView(FormView):
    template_name = 'accounts/verify_email.html'
    form_class = CustomUserVerificationForm
    
    def get_success_url(self):
        user = self.request.user

        return reverse_lazy('profile_detail_view', kwargs={'pk': user.pk})
        

    def form_valid(self, form):
        code_entered = form.cleaned_data.get('code')

        try:
            user_code = UserEmailVerificationCode.objects.get(code=code_entered)
            self.request.user.email_verified = True
            self.request.user.save()
            user_code.delete()
            messages.success(self.request, 'Email verificado com sucesso!')

            return super().form_valid(form)
        except UserEmailVerificationCode.DoesNotExist:
            messages.error(self.request, 'Código de verificação inválido.')

            return self.form_invalid(form)


class SendVerificationEmailView(View):

    def get(self, request, *args, **kwargs):
        user = self.request.user

        if user.is_authenticated:
            if not user.email_verified:
                try:
                    old_code = UserEmailVerificationCode.objects.get(user=user)
                    if old_code:
                        old_code.delete()
                        email_code_generator(user.id)
                    else:
                        email_code_generator(user.id)
                except UserEmailVerificationCode.DoesNotExist as e:
                    email_code_generator(user.id)

        return redirect(reverse_lazy('verify_email_view'))


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


@method_decorator(login_required(login_url='login_view'), name='dispatch')
class ProfileView(DetailView):
    model = CustomUser
    template_name = 'accounts/profile.html'
    context_object_name = 'user'


@method_decorator(login_required(login_url='login_view'), name='dispatch')
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


@method_decorator(login_required(login_url='login_view'), name='dispatch')
class AddCourseView(View):

    def post(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        request.user.user_courses.add(course)
        messages.info(request, f'Curso "{course.course_name}" adicionado com sucesso!')
        return redirect('my_courses_list_view')


@method_decorator(login_required(login_url='login_view'), name='dispatch')
class MyCoursesListView(ListView):
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


@method_decorator(login_required(login_url='login_view'), name='dispatch')
class UserCourseDetailView(DetailView):
    model = Course
    template_name = 'accounts/user_course_detail.html'
    context_object_name = 'course'


@method_decorator(login_required(login_url='login_view'), name='dispatch')
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
