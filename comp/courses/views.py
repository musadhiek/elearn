from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from .models import Course
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.

class OwnerMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner = self.request.user)

class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course
    fields = ['subject','title','slug','overview']
    success_url = reverse_lazy('manage_course_list')

class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'

class ManageCourseListView(OwnerCourseMixin, ListView):
    permission_required = 'courses.view_course'
    model = Course
    template_name = 'courses/manage/course/list.html'
    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     return qs.filter(owner = self.request.user)

class CourseCreateView(OwnerCourseMixin, OwnerEditMixin, CreateView ):
    permission_required = 'courses.add_course'
    template_name = 'courses/manage/course/form.html'

class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required =  'courses.change_course'
    template_name = 'courses/manage/course/form.html'

class CourseDeleteView(OwnerCourseMixin, DeleteView):
    permission_required = 'courses.delete_course'
    template_name = 'courses/manage/course/delete.html'


# class ManageCourseListView(ListView):
#     model = Course
#     template_name = 'courses/manage/course/list.html'

#     def get_queryset(self):
#         qs = super().get_queryset()
#         return qs.filter(owner = self.request.user)