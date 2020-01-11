from crispy_forms import helper, layout

from django import forms

from .models import User


def fieldtostring(**kwargs):
    string = '<input class="form-control" '
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


class UserUpdateFormBase(forms.ModelForm):
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


class UserUpdateNameForm(UserUpdateFormBase):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UserUpdateNameForm, self).__init__(*args, **kwargs)
        self.helper = helper.FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.Div(
                layout.Div(
                    layout.Div(
                        layout.Div(
                            layout.HTML(fieldtostring(type="text", name="first_name", value="")),
                            layout.HTML(valuetolabel("first_name", "First Name")),
                            css_class="md-form md-outline",
                        ),
                        css_class="col",
                    ),

                    layout.Div(
                        layout.Div(
                            layout.HTML(fieldtostring(type="text", name="last_name", value="")),
                            layout.HTML(valuetolabel("last_name", "Last Name")),
                            css_class="md-form md-outline",
                        ),
                        css_class="col",
                    ),
                    css_class="row",
                ),
                layout.ButtonHolder(
                    layout.Submit('submit', 'Submit', css_class='button white')
                )
            )
        )
