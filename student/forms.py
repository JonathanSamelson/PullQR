from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, required=True, help_text='Only @student.uclouvain.be authorized')
    first_name = forms.CharField(max_length=13, required=True, help_text='It will be displayed in the main page')
    last_name = forms.CharField(max_length=13, required=True, help_text='It will be displayed in the main page')

    class Meta:
        model = User
        fields = ("username", 'first_name', 'last_name' , "email", "password1", "password2",)

    def clean_email(self):
        data = self.cleaned_data['email']
        data = data.lower()
        domain = data.split('@')[1]
        domain_list = ["student.uclouvain.be"]

        if domain not in domain_list:
            raise forms.ValidationError("@student.uclouvain.be required")

        mail_exist_check = User.objects.filter(email=data)
        if len(mail_exist_check) > 0:
            raise forms.ValidationError("Email already used")

        return data

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user