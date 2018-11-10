# -*- coding:utf-8 -*-

#from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserChangeForm, CustomPasswordChangeForm, CustomPasswordResetForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import send_mail
from anaconda_navigator.utils.py3compat import request
from django.views.decorators.csrf import requires_csrf_token
from django.http.response import JsonResponse
from django.core.serializers import serialize
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.views import PasswordResetView
import json
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

User = get_user_model()

@login_required
@requires_csrf_token
def user_change(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(data=request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, '사용자 이름이 정상적으로 변경되었습니다.', extra_tags='alert')
            return redirect('members:user_change')
        else:
            render(request, 'members/user_change.html', {'form':form})
    else:
        form = CustomUserChangeForm()        
    return render(request, 'members/user_change.html', {'form':form})

@login_required
@requires_csrf_token
def password_change(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, '비밀번호가 정상적으로 변경되었습니다.', extra_tags='alert')
            return redirect('members:password_change')
        else:
            render(request, 'members/password_change.html', {'form':form})
    else:
        form = CustomPasswordChangeForm(request.user)        
    return render(request, 'members/password_change.html', {'form':form})

@requires_csrf_token
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)        
            context = json.dumps({
                'result':True,
            })
            if request.POST.get('next',None ) is not None:
                return redirect(request.POST['next'])
        else:
            context = json.dumps({
                'result':False,
            })
        return HttpResponse(context, content_type='application/json')
    else:
        form = CustomAuthenticationForm()
        return render(request, 'members/login.html', {'form':form})

@requires_csrf_token
def send_email_again(request):
    if request.method == "POST":
        user = request.user
        current_site = get_current_site(request)
        success = Send_email(user, [user.email], current_site)
        
        context = json.dumps({
                'success' : success,
                'email' : user.email,
            })
        context = json.dumps({
            'good':'good',
            })
        return HttpResponse(context, content_type='application/json')
    else:
        return HttpResponse(json.dumps({'error':'error occurred'}), content_type='application/json')
  
def Send_email(user,to_email,current_site):
    mail_subject = 'Activate your account.'
    from_email = 'ssook7979@naver.com'
    message = render_to_string('members/acc_active_email.html', {
                'user':user,
                'domain':current_site.domain,
                'uidb64':urlsafe_base64_encode(force_bytes(user.pk)).decode("utf-8"),
                'token':account_activation_token.make_token(user),
                })
    success = send_mail(mail_subject, message, from_email , to_email, fail_silently=True)
    return success

@requires_csrf_token
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()    
            login(request, user)        
            current_site = get_current_site(request)        
            to_email = [form.cleaned_data.get('email')]
            success = Send_email(user, to_email, current_site)
            context = json.dumps({
                'success' : success,
            })
            return HttpResponse(context, content_type='application/json')                      
        else:
            error = form.errors
            return HttpResponse(json.dumps({'error':error}), content_type='application/json')              
    else:
        form = CustomUserCreationForm()
    return render(request, 'members/signup.html', {'form':form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('이메일 인증이 완료되었습니다.')
    else:
        return HttpResponse('유효하지않은 인증코드입니다.')    