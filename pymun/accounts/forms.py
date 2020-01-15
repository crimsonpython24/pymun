from crispy_forms import helper, layout, bootstrap
from django import forms
from django.utils.translation import gettext_lazy as _
from django.http import request

from .models import User


def fieldtostring(*args, **kwargs):
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
            string += ('id="' + value + '" max_length="' + str(User._meta.get_field(value).max_length) + '" ')
            string += ('name="' + value + '" ')
        else:
            string += (field + '="' + value + '" ')
    string += ">"
    return string


def valuetolabel(name, cont):
    return '<label for="{}">{}</label>'.format(name, cont)


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
                            "required", "autofocus", type="text", name="first_name", value="", css_class="form-control"
                        )),
                        layout.HTML(valuetolabel("first_name", "First Name")),
                        css_class="md-form",
                    ),
                ),
                layout.Div(
                    layout.Div(
                        layout.HTML(fieldtostring(
                            "required", type="text", name="last_name", value="", css_class="form-control"
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
                layout.Layout('birthday')
            )
        )


class UpdateGenderForm(UpdateFormBase):
    gender_choices = [('male', 'Male'), ('female', 'Female'), ('others', 'Non-Binary'), ('none', 'Undeclarable')]
    gender = forms.ChoiceField(label=_('Gender'), required=False, widget=forms.Select, choices=gender_choices,)

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
                bootstrap.InlineRadios('gender')
            )
        )


class UpdateContactEmailForm(UpdateFormBase):
    class Meta:
        model = User
        fields = ['email', 'recovery_email', 'about_me_email']

    def __init__(self, user, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UpdateContactEmailForm, self).__init__(*args, **kwargs)
        self.helper = helper.FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.Div(
                layout.Div(
                    layout.HTML(fieldtostring(
                        "required", "autofocus", type="radio", name="email", value="", css_class="form-check-input"
                    )),
                    layout.HTML(valuetolabel("email", self.user.username)),
                    css_class="form-check",
                ),
            )
        )


class UpdateAboutMeEmailForm(UpdateFormBase):
    class Meta:
        model = User
        fields = ['email', 'recovery_email', 'about_me_email']

    def __init__(self, *args, **kwargs):
        super(UpdateAboutMeEmailForm, self).__init__(*args, **kwargs)
        self.helper = helper.FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.Div()
        )


class UpdateRecoveryEmailForm(UpdateFormBase):
    class Meta:
        model = User
        fields = ['email', 'recovery_email', 'about_me_email']

    def __init__(self, *args, **kwargs):
        super(UpdateRecoveryEmailForm, self).__init__(*args, **kwargs)
        self.helper = helper.FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.Div()
        )


class UpdateWorkForm(UpdateFormBase):
    class Meta:
        model = User
        fields = ['email', 'recovery_email', 'about_me_email']

    def __init__(self, *args, **kwargs):
        super(UpdateWorkForm, self).__init__(*args, **kwargs)
        self.helper = helper.FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.Div()
        )


class UpdatePlacesForm(UpdateFormBase):
    class Meta:
        model = User
        fields = ['email', 'recovery_email', 'about_me_email']

    def __init__(self, *args, **kwargs):
        super(UpdatePlacesForm, self).__init__(*args, **kwargs)
        self.helper = helper.FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.Div()
        )


class UpdateDetailForm(UpdateFormBase):
    class Meta:
        model = User
        fields = ['email', 'recovery_email', 'about_me_email']

    def __init__(self, *args, **kwargs):
        super(UpdateDetailForm, self).__init__(*args, **kwargs)
        self.helper = helper.FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.Div()
        )
