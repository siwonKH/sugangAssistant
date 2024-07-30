from django import forms
from .models import StartDate


class StartDateForm(forms.ModelForm):
    class Meta:
        model = StartDate
        fields = ['date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
