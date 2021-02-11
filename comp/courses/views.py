from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from .models import Course
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from .forms import ModuleFormSet
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

class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/formset.html'
    course  = None

    def get_formset(self, data = None):
        return ModuleFormSet (instance= self.course, data = data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id= pk,owner= request.user)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course':self.course,'formset':formset})

    def post(self,request,*args,**kwargs):
        formset = self.get_formset(data = request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course':self.course,'formset':formset})             
