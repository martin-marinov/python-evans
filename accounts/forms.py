from django import forms
from accounts.models import UserProfile
from django.contrib.auth.forms import AuthenticationForm


class EmailInput(forms.widgets.TextInput):
    input_type = 'email'


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False,
                                     label='Запомни ме на този компютър')


class RegistrationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    email = forms.EmailField(label='Електронна поща',
                             widget=EmailInput(),
                             error_messages={'invalid': "Полето може да съдържа само букви, цифри и @/./+/-/_",
                                             'required': 'Необходимо е да въведете имейл.'})
    password1 = forms.CharField(label='Парола',
                                widget=forms.PasswordInput(),
                                error_messages={'required': 'Необходимо е да въведете парола.'})
    password2 = forms.CharField(label='Повторете Парола',
                                widget=forms.PasswordInput(),
                                error_messages={'required': 'Необходимо е да въведете парола.'})
    faculty_number = forms.IntegerField(label='Факултетен номер',
                                        error_messages={'required': 'Необходимо е да въведете факултетен номер.',
                                                        'invalid': 'Факултетният номер е неотрицателно число.'})
    name = forms.CharField(label='Име',
                           error_messages={'required': 'Необходимо е да въведете имената си.'})

    class Meta:
        model = UserProfile
        fields = ('email', 'faculty_number', 'name')

    def clean(self):
        """
        Verify that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Паролите не съвпадат!")
        return self.cleaned_data
