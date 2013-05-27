from django import forms
from django.utils.safestring import mark_safe
from accounts.models import UserProfile, get_avatar_path


class EditProfileForm(forms.ModelForm):
    """A form for edit profile of users. Includes all the required
    fields, plus a repeated password."""

    should_remove_avatar = forms.BooleanField(required=False,
                                              label='Изтрий снимката')
    avatar = forms.ImageField(required=False)
    github = forms.CharField(required=False,
                             label=mark_safe('Потребителско име в <a href="http://github.com/">GitHub</a>'),
                             help_text='Ако нямате, крайно време е да си направите')
    twitter = forms.CharField(required=False,
                              label='Twitter',
                              help_text='Ако сте от този тип хора')
    skype = forms.CharField(required=False,
                            label='Skype',
                            help_text='Ако смятате, че ни е нужен')
    phone_number = forms.CharField(required=False,
                                   label='Мобилен Телефон',
                                   help_text='Не е публичен; ползваме го само в краен случай')
    site = forms.CharField(required=False,
                           label='Сайт',
                           help_text='Ако имате такъв; не забравяйте да укажете протокол (например http://)')
    about = forms.CharField(required=False,
                            label='Разкажете ни за себе си',
                            help_text='Ако искате',
                            widget=forms.Textarea)
    subscribed = forms.BooleanField(required=False,
                                    label='Искам да получавам писма за коментари по решенията ми')
    password1 = forms.CharField(required=False,
                                label='Парола',
                                widget=forms.PasswordInput())
    password2 = forms.CharField(required=False,
                                label='Въведете паролата повторно',
                                widget=forms.PasswordInput())

    class Meta:
        model = UserProfile
        fields = ['github', 'twitter', 'skype', 'phone_number',
                  'site', 'about', 'subscribed']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data.get('password2', '')
        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError('не съвпада')
        return password2

    def save(self, commit=True):
        #Handle change of passwords
        self.user = super(EditProfileForm, self).save(commit)
        new_password = self.cleaned_data.get('password2', '')
        if new_password:
            self.user.set_password(new_password)
        #Handle avatar actions
        should_remove_avatar = self.cleaned_data.get('should_remove_avatar')
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            self.user.avatar.save(avatar.name, avatar, commit)
        elif should_remove_avatar and self.user.avatar:
            self.user.avatar.delete(save=commit)
        if commit:
            self.user.save()
        return self.user
