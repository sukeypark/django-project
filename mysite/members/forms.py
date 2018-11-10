# -*- coding:utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UserChangeForm, PasswordResetForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from distributed.core import error_message
from .models import CustomUser
import re
from django.contrib.auth import get_user_model

from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode

User = get_user_model()


class CustomPasswordResetForm(PasswordResetForm):
    class Meta:
        model = User
        fields = ("email",)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email).exists():
            raise ValidationError("등록되지 않은 이메일입니다.")
    
        return email
       
class CustomPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = _('대소문자,숫자,특수문자(#?!@$%^&*-)를 모두 사용하여 8-12자의 비밀번호를 작성하세요.')
        for key, value in self.fields.items():
            self.fields[key].widget.attrs['class'] = 'w3-input w3-border w3-margin-bottom'
        self.fields['new_password1'].widget.attrs['class'] = 'w3-input w3-border'

        
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    uname = forms.RegexField(
        label=_("사용자 이름"),
        max_length=20,
        regex=r'^[\w.@+-]+$',
        help_text=_("숫자, 문자, @/./+/-/_ 20자 이하")
        )
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'uname', 'password1', 'password2')
       
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].help_text = _('아이디로 사용할 이메일을 입력하세요')
        self.fields['email'].label = _('이메일')
        self.fields['password1'].help_text = _('대소문자,숫자,특수문자(#?!@$%^&*-) 8-12자')
        for key, value in self.fields.items():
            self.fields[key].widget.attrs['class'] = 'textInput'
            self.fields[key].widget.attrs['style'] = 'margin:0'
            self.fields[key].widget.attrs['placeholder'] = self.fields[key].help_text
            
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError(
                _("이미 등록된 이메일입니다."),
                code='email_exists',
            )
        return data

        
class CustomAuthenticationForm(AuthenticationForm):

    def confirm_login_allowed(self, user):
        if not user.is_active:
            pass
    
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = _('이메일')
        self.fields['username'].help_text = _('이메일을 입력해주세요')
        self.fields['password'].help_text = _('비밀번호를 입력해주세요')
        for key, value in self.fields.items():
            self.fields[key].widget.attrs['class'] = 'textInput'
            self.fields[key].widget.attrs['placeholder'] = self.fields[key].help_text

  
class CustomUserChangeForm(UserChangeForm):
    
    class Meta:
        model = CustomUser
        fields = ('uname',)

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['uname'].label = _('변경 사용자 이름')
        self.fields['uname'].widget.attrs['class'] = 'w3-input w3-border w3-margin-bottom'
        self.fields['uname'].help_text = _('숫자, 문자, 특수문자(@/./+/-/_)를 이용하여 20자 이하로 작성해주세요')
        self.fields['uname'].error_messages = {'invalid': _("올바른 형식이 아닙니다."), }
        
        del self.fields['password']
        
'''
class UnameChangeForm(forms.ModelForm):
    uname = forms.RegexField(
        label=_("사용자 이름"), 
        max_length=20, 
        regex=r'^[\w.@+-]+$',
        help_text = _("숫자, 문자, 튻수문자(@/./+/-/_)를 이용하여 20자 이하로 작성해주세요"),
        error_messages = {'invalid': _('올바른 형식이 아닙니다.')},
        )
    class Meta:
        model = CustomUser
        fields = ('uname', )
    def __init__(self, *args, **kwargs):
        super(UnameChangeForm, self).__init__(*args, **kwargs)
        self.fields['uname'].label = _('변경 사용자 이름')
        self.fields['uname'].widget.attrs['class'] = 'w3-input w3-border'
        self.fields['uname'].help_text = _('숫자, 문자, 특수문자(@/./+/-/_)를 이용하여 20자 이하로 작성해주세요')
'''     
