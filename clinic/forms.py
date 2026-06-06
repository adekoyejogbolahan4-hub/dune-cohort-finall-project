from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Doctor, Service


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            'first_name', 'last_name', 'specialisation', 'email',
            'phone', 'bio', 'photo', 'is_available', 'years_experience'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'doctor@clinic.com'}),
            'phone': forms.TextInput(attrs={'placeholder': '+234 xxx xxx xxxx'}),
            'years_experience': forms.NumberInput(attrs={'min': 0}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Doctor.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('A doctor with this email already exists.')
        return email


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
