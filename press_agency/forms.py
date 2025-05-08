from django import forms
from django.contrib.auth.forms import (
    SetPasswordForm,
    PasswordResetForm,
    AuthenticationForm,
    UsernameField,
    UserCreationForm,
)
from django.contrib.auth.models import User
from models import Topic, Redactor, Newspaper


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": "form-control",
                }
            )


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        label=("Password",),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "class": "form-control"}
        ),
    )


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="New Password",
    )
    new_password2 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Confirm New Password",
    )


class NewspaperForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = (
            "name",
            "description",
        )

    def clean_name(self):
        name = self.cleaned_data["name"]
        if Topic.objects.filter(name=name).exists():
            raise forms.ValidationError(f"{name} already exists!")
        return name


class AuthorProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

        for name, field in self.fields.items():
            field.widget.attrs.setdefault("class", "form-control")
            field.widget.attrs.setdefault("autocomplete", "off")

        self.fields["years_of_experience"].widget.attrs.update(
            {"placeholder": "e.g. 3"}
        )
        self.fields["date_of_birth"].widget.attrs.update(
            {"placeholder": "dd.MM.YYYY", "type": "date"}
        )

    class Meta:
        model = Redactor
        fields = ["username", "date_of_birth", "pen_name", "years_of_experience"]


class NewspaperDetailsForm(forms.ModelForm):
    class Meta:
        model = Newspaper
        fields = ("title", "content", "topic")
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 5,
                }
            ),
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["topic"].queryset = Topic.objects.filter(owner=user)
