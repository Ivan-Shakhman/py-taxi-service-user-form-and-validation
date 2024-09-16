from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError("License number must be 8 characters long")
        if (
            license_number[:3] != license_number[:3].upper()
            or not license_number[:3].isalpha()
        ):
            raise ValidationError("First 3 characters must be uppercase chars")
        try:
            int(license_number[3:])
        except ValueError:
            raise ValidationError("last 5 characters must be a numbers")
        return license_number


class DriverCreateForm(UserCreationForm, DriverLicenseUpdateForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Car
        fields = "__all__"
