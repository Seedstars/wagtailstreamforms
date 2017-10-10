import django.forms

from captcha.fields import ReCaptchaField
from wagtail.wagtailforms.forms import FormBuilder as OrigFormBuilder

from wagtail_streamforms.utils import recaptcha_enabled


class FormBuilder(OrigFormBuilder):

    def __init__(self, fields, **kwargs):
        self.add_recaptcha = kwargs.pop('add_recaptcha')
        super(FormBuilder, self).__init__(fields)

    def create_regex_field(self, field, options):
        if field.regex_validator:
            # there is a selected validator so use it
            options.update({
                'regex': field.regex_validator.regex,
                'error_messages': {'invalid': field.regex_validator.error_message}
            })
        else:
            # otherwise allow anything
            options.update({'regex': '(.*?)'})
        return django.forms.RegexField(**options)

    OrigFormBuilder.FIELD_TYPES.update(
        {'regexfield': create_regex_field}
    )

    @property
    def formfields(self):
        fields = super(FormBuilder, self).formfields

        # If enabled add recaptcha field
        if self.add_recaptcha and recaptcha_enabled():
            fields['recaptcha'] = ReCaptchaField()

        return fields
