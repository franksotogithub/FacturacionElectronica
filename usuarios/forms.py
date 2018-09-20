from django import forms
from .models import Usuario ,Rol
from django.contrib.auth import forms as auth_forms


class LoginForm(forms.Form):
    usuario = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Usuario'}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Password'}))



class UserCreationForm(forms.ModelForm):


    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    #usuario=forms.CharField(label="Usuario", widget=forms.CharField)
    #rol=forms.ModelChoiceField(label="Rol",queryset=Rol.objects.all())
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput,
                                help_text="Enter the same password as above, for verification.")

    class Meta:
        model = Usuario
        #fields = '__all__'
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = auth_forms.ReadOnlyPasswordHashField(label="Password",
        help_text="Raw passwords are not stored, so there is no way to see "
                  "this user's password, but you can change the password "
                  "using <a href=\"../password/\">this form</a>.")

    class Meta:
        model = Usuario
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        return self.initial["password"]