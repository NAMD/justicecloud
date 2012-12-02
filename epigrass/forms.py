"""
Created on June 10, 2012
@author: peta15
"""

from wtforms import fields
from wtforms import Form
from wtforms import validators
from wtforms import ValidationError
from lib import utils
from webapp2_extras.i18n import lazy_gettext as _
from webapp2_extras.i18n import ngettext, gettext


FIELD_MAXLENGTH = 50 # intended to stop maliciously long input


class FormTranslations(object):
    def gettext(self, string):
        return gettext(string)

    def ngettext(self, singular, plural, n):
        return ngettext(singular, plural, n)


class BaseForm(Form):
    
    def __init__(self, request_handler):
        super(BaseForm, self).__init__(request_handler.request.POST)
    def _get_translations(self):
        return FormTranslations()


class CurrentPasswordMixin(BaseForm):
    current_password = fields.TextField(_('Password'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH)])


class PasswordMixin(BaseForm):
    password = fields.TextField(_('Password'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH)])


class ConfirmPasswordMixin(BaseForm):
    c_password = fields.TextField(_('Confirm Password'), [validators.Required(), validators.EqualTo('password', _('Passwords must match.')), validators.Length(max=FIELD_MAXLENGTH)])


class UserMixin(BaseForm):
    username = fields.TextField(_('Username'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH), validators.regexp(utils.ALPHANUMERIC_REGEXP, message=_('Username invalid. Use only letters and numbers.'))])
    name = fields.TextField(_('Name'), [validators.Length(max=FIELD_MAXLENGTH)])
    last_name = fields.TextField(_('Last Name'), [validators.Length(max=FIELD_MAXLENGTH)])
    country = fields.SelectField(_('Country'), choices=utils.COUNTRIES)


class PasswordResetCompleteForm(PasswordMixin, ConfirmPasswordMixin):
    pass


# mobile form does not require c_password as last letter is shown while typing and typing is difficult on mobile
class PasswordResetCompleteMobileForm(PasswordMixin):
    pass


class LoginForm(BaseForm):
    password = fields.TextField(_('Password'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH)], id='l_password')
    username = fields.TextField(_('Username'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH)], id='l_username')


class ContactForm(BaseForm):
    email = fields.TextField(_('Email'), [validators.Required(), validators.Length(min=7, max=FIELD_MAXLENGTH), validators.regexp(utils.EMAIL_REGEXP, message=_('Invalid email address.'))])
    name = fields.TextField(_('Name'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH)])
    message = fields.TextAreaField(_('Message'), [validators.Required(), validators.Length(max=65536)])


class RegisterForm(PasswordMixin, ConfirmPasswordMixin, UserMixin):
    email = fields.TextField(_('Email'), [validators.Required(), validators.Length(min=7, max=FIELD_MAXLENGTH), validators.regexp(utils.EMAIL_REGEXP, message=_('Invalid email address.'))])
    pass


# mobile form does not require c_password as last letter is shown while typing and typing is difficult on mobile
class RegisterMobileForm(PasswordMixin, UserMixin):
    email = fields.TextField(_('Email'), [validators.Required(), validators.Length(min=7, max=FIELD_MAXLENGTH), validators.regexp(utils.EMAIL_REGEXP, message=_('Invalid email address.'))])
    pass


class EditProfileForm(UserMixin):
    pass


class EditPasswordForm(PasswordMixin, ConfirmPasswordMixin, CurrentPasswordMixin):
    pass


# mobile form does not require c_password as last letter is shown while typing and typing is difficult on mobile
class EditPasswordMobileForm(PasswordMixin, CurrentPasswordMixin):
    pass


class EditEmailForm(PasswordMixin):
    new_email = fields.TextField(_('Email'), [validators.Required(), validators.Length(min=7, max=FIELD_MAXLENGTH), validators.regexp(utils.EMAIL_REGEXP, message=_('Invalid email address.'))])

def validate_json(form,field):
    fname = field.data.lower()
    ALLOWED_EXTENSIONS = ['json','js']
    if not ('.' in fname and fname.rsplit('.',1)[1] in ALLOWED_EXTENSIONS):
        raise ValidationError('You must upload a JSON file.')

class SimulationForm(BaseForm):
    name = fields.StringField(_('Name'),[validators.Required(), validators.Length(min=3, max=FIELD_MAXLENGTH), validators.regexp(utils.ALPHANUMERIC_REGEXP, message=_('Invalid name.'))])
    description = fields.TextAreaField(_('Description'),[validators.Optional(), validators.Length(min=10,max=512)])
    map = fields.FileField(_('Map Layer'),[validators.Optional(), validate_json])
    series = fields.FileField(_('Time Series'),[validators.Required(), validate_json])
    epg = fields.FileField(_('Epg file'),[validators.Required(), validate_json])
    network = fields.FileField(_('Network file'),[validators.Optional()])
    spread = fields.FileField(_('Spread tree file'),[validators.Optional()])
    model = fields.TextAreaField(_('Model Source'),[validators.Length(min=10,max=10000)])


