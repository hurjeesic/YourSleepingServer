from django import forms

from .models import Activity

class ActivityForm(forms.ModelForm):

    class Meta:
        model = Activity
        fields = ('date', 'time', 'heart_rate', 'type', 'sleep_time',)
