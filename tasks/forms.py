from django import forms
from tasks.models import Solution


class MySolutionForm(forms.ModelForm):
    model = Solution
    code = forms.CharField(label='Код',
                           widget=forms.Textarea())

    class Meta:
        model = Solution
        fields = ['code']
