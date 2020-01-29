from crispy_forms import helper, layout, bootstrap
from django import forms
from django.utils.translation import gettext_lazy as _
from django.http import request
from django.contrib.postgres.forms import SplitArrayField
from django.forms import EmailField

from .models import User


def fieldtostring(if_user, different_id=False, *args, **kwargs):
    string = '<input '
    for arg in args:
        if arg == 'required':
            string += " required "
    for field, value in kwargs.items():
        if field == "css_class":
            string += ('class="' + value + '" ')
        if field == 'aria_describedby':
            string += ('aria-describedby="' + value + '" ')
        if field == "name":
            if different_id:
                string += ('name="' + value + '" ')
            elif if_user:
                string += ('id="' + value + '" max_length="' + str(User._meta.get_field(value).max_length) + '" ')
                string += ('name="' + value + '" ')
            else:
                string += ('id="' + value + '" ' + 'name="' + value + '" ')
        else:
            string += (field + '="' + value + '" ')
    string += ">"
    return string


def valuetolabel(name, cont, **kwargs):
    string = '<label '.format(name, cont)
    for field, value in kwargs.items():
        if field == 'css_class':
            string += ('class="' + value + '" ')
    string += ' for="{}">{}</label>'.format(name, cont)
    return string


def selecttostring(*args, **kwargs):
    string = '<select '
    for field, value in kwargs.items():
        if field == 'css_class':
            string += ('class="' + value + '" ')
        else:
            string += (field + '="' + value + '" ')
    string += ">"
    return string


def closeselect():
    return "</select>"


class UpdateFormBase(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.format('../password/')
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial.get('password')

    class Meta:
        model = User
        fields = '__all__'


class UpdateNameForm(UpdateFormBase):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UpdateNameForm, self).__init__(*args, **kwargs)
        self.helper = helper.FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.Div(
                layout.Div(
                    layout.Div(
                        layout.HTML(fieldtostring(
                            True, "required", "autofocus", type="text", name="first_name", value="",
                            css_class="form-control"
                        )),
                        layout.HTML(valuetolabel("first_name", "First Name")),
                        css_class="md-form",
                    ),
                ),
                layout.Div(
                    layout.Div(
                        layout.HTML(fieldtostring(
                            True, "required", type="text", name="last_name", value="", css_class="form-control"
                        )),
                        layout.HTML(valuetolabel("last_name", "Last Name")),
                        css_class="md-form",
                    ),
                ),
            )
        )


class UpdateBirthdayForm(UpdateFormBase):
    birthday = forms.DateField(
        widget=forms.SelectDateWidget(empty_label=('Choose Year', 'Choose Month', 'Choose Day')),
    )

    class Meta:
        model = User
        fields = ['birthday']

    def __init__(self, *args, **kwargs):
        super(UpdateBirthdayForm, self).__init__(*args, **kwargs)
        self.helper = helper.FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.Div(
                layout.Div(
                    layout.Div(
                        layout.Div(
                            layout.HTML(
                                selecttostring(
                                    "required", name="birthday_month", id="id_birthday_month",
                                    css_class="form-control md-form"
                                )
                            ),
                            layout.HTML(
                                """
                                <option value="" disabled selected>Choose your option</option>
                                <option value="1">January</option>
                                <option value="2">February</option>
                                <option value="3" selected>March</option>
                                <option value="4">April</option>
                                <option value="5">May</option>
                                <option value="6">June</option>
                                <option value="7">July</option>
                                <option value="8">August</option>
                                <option value="9">September</option>
                                <option value="10">October</option>
                                <option value="11">November</option>
                                <option value="12">December</option>
                                """ + closeselect()
                            ),
                        ),
                        css_class="col"
                    ),
                    layout.Div(
                        layout.Div(
                            layout.Div(
                                layout.Div(
                                    layout.HTML(
                                        fieldtostring(
                                            False, "required", name="birthday_day", id="id_birthday_day",
                                            css_class="form-control", type="number", placeholder="Day"
                                        )
                                    ),
                                    css_class="col-5 birthday-change-col-0"
                                ),
                                layout.Div(
                                    layout.HTML(
                                        fieldtostring(
                                            False, "required", name="birthday_year", id="id_birthday_year",
                                            css_class="form-control", type="number", placeholder="Year"
                                        )
                                    ),
                                    css_class="col-7 birthday-change-col-0"
                                ),
                                css_class="row"
                            ),
                            css_class="md-form"
                        ),
                        css_class="col"
                    ),
                    css_class="row"
                )
            )
        )


class UpdateGenderForm(UpdateFormBase):
    gender_choices = [('male', 'Male'), ('female', 'Female'), ('others', 'Non-Binary'), ('none', 'Undeclarable')]
    gender = forms.ChoiceField(label=_('Gender'), required=False, widget=forms.Select, choices=gender_choices, )

    class Meta:
        model = User
        fields = ['gender']

    def __init__(self, *args, **kwargs):
        super(UpdateGenderForm, self).__init__(*args, **kwargs)
        self.helper = helper.FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.Div(
                layout.Div(
                    layout.HTML(fieldtostring(
                        True, True, "required", type="radio", name="gender", value="male",
                        id="id_gender_1", css_class="form-check-input"
                    )),
                    layout.HTML(valuetolabel("id_gender_1", "Male", css_class="form-check-label")),
                    css_class="form-check custom-form-check-0"
                ),
                layout.Div(
                    layout.HTML(fieldtostring(
                        True, True, "required", type="radio", name="gender", value="female",
                        id="id_gender_2", css_class="form-check-input"
                    )),
                    layout.HTML(valuetolabel("id_gender_2", "Female", css_class="form-check-label")),
                    css_class="form-check custom-form-check-0"
                ),
                layout.Div(
                    layout.HTML(fieldtostring(
                        True, True, "required", type="radio", name="gender", value="others",
                        id="id_gender_3", css_class="form-check-input"
                    )),
                    layout.HTML(valuetolabel("id_gender_3", "Non-Binary", css_class="form-check-label")),
                    css_class="form-check custom-form-check-0"
                ),
                layout.Div(
                    layout.HTML(fieldtostring(
                        True, True, "required", type="radio", name="gender", value="none",
                        id="id_gender_4", css_class="form-check-input"
                    )),
                    layout.HTML(valuetolabel("id_gender_4", "Undeclarable", css_class="form-check-label")),
                    css_class="form-check custom-form-check-0"
                )
            )
        )


class UpdateMainEmailForm(UpdateFormBase):
    class Meta:
        model = User
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(UpdateMainEmailForm, self).__init__(*args, **kwargs)
        self.helper = helper.FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.Div()
        )


class UpdateContactEmailForm(UpdateFormBase):
    class Meta:
        model = User
        fields = ['contact_email']

    def __init__(self, *args, **kwargs):
        super(UpdateContactEmailForm, self).__init__(*args, **kwargs)
        self.helper = helper.FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.Div()
        )


class UpdateRecoveryEmailForm(UpdateFormBase):
    class Meta:
        model = User
        fields = ['recovery_email']

    def __init__(self, *args, **kwargs):
        super(UpdateRecoveryEmailForm, self).__init__(*args, **kwargs)
        self.helper = helper.FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.Div()
        )


class UpdateAlternateEmailForm(UpdateFormBase):
    SplitArrayField(EmailField(required=True), size=float("inf"), remove_trailing_nulls=False)

    class Meta:
        model = User
        fields = ['alternate_email']

    def __init__(self, *args, **kwargs):
        super(UpdateAlternateEmailForm, self).__init__(*args, **kwargs)
        self.helper = helper.FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.Div()
        )
