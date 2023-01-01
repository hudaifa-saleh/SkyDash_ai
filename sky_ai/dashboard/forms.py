from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class ProfileForm(forms.Form):
    address_line1 = forms.CharField(
        required=True,
        label="Address Line 1",
        widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Enter Address Line 1"}),
    )
    address_line2 = forms.CharField(
        required=False,
        label="Address Line 2",
        widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Enter Address Line 2"}),
    )
    city = forms.CharField(
        required=True,
        label="City",
        widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Enter City"}),
    )
    province = forms.CharField(
        required=True,
        label="Province",
        widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Enter Province"}),
    )
    postal_code = forms.CharField(
        required=True,
        label="Postal Code",
        widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Enter Postal Code"}),
    )
    country = forms.CharField(
        required=True,
        label="Country",
        widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Enter Country"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column("address_line1", css_class="form-group col-md-6"), Column("address_line2", css_class="form-group col-md-6")),
            Row(Column("city", css_class="form-group col-md-6"), Column("province", css_class="form-group col-md-6")),
            Row(Column("country", css_class="form-group col-md-6"), Column("postal_code", css_class="form-group col-md-6")),
            Submit("submit", "Sign in", css_class="btn btn-primary me-2"),
        )

    class Meta:
        model = Profile
        fields = ["address_line1", "address_line2", "city", "province", "country", "postal_code"]