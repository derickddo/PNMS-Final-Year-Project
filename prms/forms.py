from allauth.account.forms import SignupForm, LoginForm
from django import forms
from prms.models import User, NeedsAssessment, PopulationProjection
from allauth.account.utils import perform_login


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, request):
        user = super(SignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user

