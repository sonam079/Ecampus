from django import forms
from django.forms.widgets import DateTimeInput
from .models import CourseMaterial, AssignmentMaterial

class CourseMaterialForm(forms.ModelForm):
    class Meta:
        model = CourseMaterial
        fields = ('description', 'file', )

class AssignmentMaterialForm(forms.ModelForm):
    submission_last_date = forms.DateTimeInput(attrs={'type': 'datetime-local', 'input_formats':[
                                                            '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
                                                            '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
                                                            '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
                                                            '%Y-%m-%d',              # '2006-10-25'
                                                            '%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
                                                            '%m/%d/%Y %H:%M:%S.%f',  # '10/25/2006 14:30:59.000200'
                                                            '%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
                                                            '%m/%d/%Y',              # '10/25/2006'
                                                            '%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
                                                            '%m/%d/%y %H:%M:%S.%f',  # '10/25/06 14:30:59.000200'
                                                            '%m/%d/%y %H:%M',        # '10/25/06 14:30'
                                                            '%m/%d/%y',              # '10/25/06'
                                                             ]})
    class Meta:
        model = AssignmentMaterial
        fields = ('description', 'file', 'submission_last_date', )
        # widgets = {
        #     'submission_last_date': DateTimeInput(attrs={'type': 'datetime-local'}),
        # }