# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import mimetypes
import os

from django import forms
from django.conf import settings
from django.core.validators import ValidationError
from django.contrib.auth.decorators import login_required, user_passes_test
from wsgiref.util import FileWrapper
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.template.defaultfilters import filesizeformat
from django.utils.encoding import smart_str
from django.utils.translation import ugettext_lazy as _
from .forms import CourseMaterialForm, AssignmentMaterialForm
from .models import course, CourseMaterial, AssignmentMaterial

@login_required
@user_passes_test(lambda u: u.groups.all()[0].name == 'faculty', login_url='/accounts/login/')
def course_list_of_faculty(request):
    courses_of_current_faculty = course.objects.filter(faculty__username__exact=request.user)
    # print(courses_of_current_faculty)
    return render(request,
                  'course_list_of_current_faculty.html',
                  {'courses_of_current_faculty': courses_of_current_faculty})

@login_required
@user_passes_test(lambda u: u.groups.all()[0].name == 'faculty', login_url='/accounts/login/')
def course_detail_view(request, course_no):
    current_course = course.objects.filter(faculty__username__exact=request.user, courseNo=course_no)
    # print(courses_of_current_faculty)
    if len(current_course) > 0:
        template_name = 'course_detail_view.html'
        return render(request,
                      template_name,
                      {'course_no': course_no})
    else:
        raise Http404("Page not found")

@login_required
@user_passes_test(lambda u: u.groups.all()[0].name == 'faculty', login_url='/accounts/login/')
def course_material_upload(request, course_no):
    # print('Joker')
    if request.method == 'POST':
        form = CourseMaterialForm(request.POST, request.FILES)
        current_course = course.objects.filter(faculty__username__exact=request.user, courseNo=course_no)
        if form.is_valid():
            file = form.cleaned_data['file']
            if file._size > 5242880:
                raise forms.ValidationError(_('Please keep filesize under 50 MB'))
            unsaved_form = form.save(commit=False)
            unsaved_form.faculty = request.user
            try:
                for temp in current_course:
                    unsaved_form.course_no = temp
            except Exception as e:
                print(str(e))
            unsaved_form.save()
            return redirect('course:course_detail_view', course_no=course_no)
    else:
        form = CourseMaterialForm()

    return render(request, 'course_material_upload.html', {
        'form': form
    })

@login_required
def files_list(request, course_no):
    material = CourseMaterial.objects.filter(course_no=course_no)
    # material = CourseMaterial.objects.all()
    # for t in material:
    #     print(t.course_no)
    return render(request, 'course_material_view.html',
                              {'course_material': material,
                               'path':settings.MEDIA_ROOT},
                              )

@login_required
@user_passes_test(lambda u: u.groups.all()[0].name == 'faculty', login_url='/accounts/login/')
def assignment_material_upload(request, course_no):
    if request.method == 'POST':
        form = AssignmentMaterialForm(request.POST, request.FILES)
        current_assignment = course.objects.filter(faculty__username__exact=request.user, courseNo=course_no)
        if form.is_valid():
            file = form.cleaned_data['file']
            if file._size > 5242880:
                raise forms.ValidationError(_('Please keep filesize under 50 MB'))
            unsaved_form = form.save(commit=False)
            unsaved_form.faculty = request.user
            try:
                for temp in current_assignment:
                    unsaved_form.course_no = temp
            except Exception as e:
                print(str(e))
            unsaved_form.save()
            return redirect('course:course_detail_view', course_no=course_no)
        else:
            print(form.errors)
            return redirect('course:assignment_material_upload', course_no=course_no)
    else:
        form = AssignmentMaterialForm()

    return render(request, 'assignment_material_upload.html', {
        'form': form
    })

@login_required
def assignment_files_list(request, course_no):
    material = AssignmentMaterial.objects.filter(course_no=course_no)
    return render(request, 'assignment_material_view.html',
                              {'assignment_material': material,
                               'course_no': course_no,
                               'path':settings.MEDIA_ROOT},
                              )

@login_required
def download(request, file_name):
    # print('Hello')
    file_path = settings.MEDIA_ROOT +'/course/'+ file_name
    file_wrapper = FileWrapper(open(file_path,'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype )
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
    return response

@login_required
def assignment_download(request, file_name):
    # print('Hello')
    file_path = settings.MEDIA_ROOT +'/assignment/'+ file_name
    file_wrapper = FileWrapper(open(file_path,'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype )
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
    return response

@login_required
def assignment_submission_download(request, file_name):
    # print('Hello')
    file_path = settings.MEDIA_ROOT +'/assignment-submission/'+ file_name
    file_wrapper = FileWrapper(open(file_path,'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype )
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
    return response


