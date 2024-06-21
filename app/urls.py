from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import *
from courses.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("home/", HomeView.as_view(), name='home_view'),
    path("register/", RegisterView.as_view(), name='register_view'), 
    path('verify_email/', VerifyEmailView.as_view(), name='verify_email_view'),
    path("check_zipcode/", check_zipcode_view, name='check_zipcode'),
    path("login/", LoginView.as_view(), name='login_view'), 
    path('password_reset/<uidb64>/<token>/', MyPasswordResetConfirm.as_view(), name='password_reset_confirm'), 
    path('password_reset/done/', MyPasswordResetComplete.as_view(), name='password_reset_complete'),  
    path("change_password/", MyPasswordReset.as_view(), name='password_reset_view'),
    path("change_password/done/", MyPasswordResetDone.as_view(), name='password_reset_done'),
    path("logout/", LogoutView.as_view(), name='logout_view'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile_detail_view'),
    path('profile/<int:pk>/update', ProfileUpdateView.as_view(), name='profile_update_view'),
    path('my_courses/', MyCoursesListView.as_view(), name='my_courses_list_view'),
    path('my_courses/<int:pk>/', UserCourseDetailView.as_view(), name='my_course_detail_view'),
    path('my_courses/<int:pk>/delete/', UserCourseDeleteView.as_view(), name='my_course_delete_view'),
    path('add_course/<int:course_id>/', AddCourseView.as_view(), name='add_course_view'),
    path('courses/', CoursesListView.as_view(), name='courses_list_view'),
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course_detail_view'),
    path('vacancies/', VacanciesListView.as_view(), name='vacancies_list_view'),
    path('health/', health_check, name='health_check'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
