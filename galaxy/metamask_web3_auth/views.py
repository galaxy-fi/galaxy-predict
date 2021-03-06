import random
import string

from django.shortcuts import render, redirect, reverse
from django.urls.exceptions import NoReverseMatch
from django.contrib.auth import login, authenticate
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect

from metamask_web3_auth.forms import LoginForm, SignupForm
from metamask_web3_auth.utils import recover_to_addr
from metamask_web3_auth.settings import app_settings
from django.contrib.auth.models import User
from article.models import UserInfo

import json


def get_redirect_url(request):
    if request.GET.get('next'):
        return request.GET.get('next')
    elif request.POST.get('next'):
        return request.POST.get('next')
    elif settings.LOGIN_REDIRECT_URL:
        try:
            url = reverse(settings.LOGIN_REDIRECT_URL)
        except NoReverseMatch:
            url = settings.LOGIN_REDIRECT_URL
        return url



@csrf_protect
@require_http_methods(["GET", "POST"])
def login_api(request):
    if request.method == 'GET':
        token = ''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits) for i in range(32))
        request.session['login_token'] = token
        return JsonResponse({'data': token, 'success': True})
    else:
        token = request.session.get('login_token')
        if not token:
            return JsonResponse({'error': _(
                "No login token in session, please request token again by sending GET request to this url"),
                'success': False})
        else:
            form = LoginForm(token, request.POST)
            if form.is_valid():
                signature, address = form.cleaned_data.get(
                    "signature"), form.cleaned_data.get("address")
                del request.session['login_token']
                user = authenticate(request, token=token,
                                    address=address, signature=signature)
                if user:
                    login(request, user, 'metamask_web3_auth.backend.Web3Backend')

                    return JsonResponse({'success': True, 'redirect_url': get_redirect_url(request)})
                else:
                    error = _("Can't find a user for the provided signature with address {address}").format(
                        address=address)

                    user = User(username=address, password=address)
                    user.save()

                    user_info = UserInfo(user=user, rating=5.0)
                    user_info.save()
                    login(request, user, 'web3auth.backend.Web3Backend')

                    return JsonResponse({'success': True, 'redirect_url': get_redirect_url(request)})
            else:
                return JsonResponse({'success': False, 'error': json.loads(form.errors.as_json())})


@require_http_methods(["POST"])
def signup_api(request):
    print("wow")
    print(request)
    user = User.objects.create_user(
        request.POST['address'], password=request.POST['address'])
    login(request, user, 'metamask_web3_auth.backend.Web3Backend')
    return redirect('article_list')

    '''
    if not app_settings.WEB3AUTH_SIGNUP_ENABLED:
        return JsonResponse({'success': False, 'error': _("Sorry, signup's are currently disabled")})
    form = SignupForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        addr_field = app_settings.WEB3AUTH_USER_ADDRESS_FIELD
        setattr(user, addr_field, form.cleaned_data[addr_field])
        user.save()
        login(request, user, 'web3auth.backend.Web3Backend')
        return JsonResponse({'success': True, 'redirect_url': get_redirect_url(request)})
    else:
        return JsonResponse({'success': False, 'error': json.loads(form.errors.as_json())})
    '''


@require_http_methods(["GET", "POST"])
def signup_view(request, template_name='metamask_web3_auth/signup.html'):
    """
    1. Creates an instance of a SignupForm.
    2. Checks if the registration is enabled.
    3. If the registration is closed or form has errors, returns form with errors
    4. If the form is valid, saves the user without saving to DB
    5. Sets the user address from the form, saves it to DB
    6. Logins the user using web3auth.backend.Web3Backend
    7. Redirects the user to LOGIN_REDIRECT_URL or 'next' in get or post params
    :param request: Django request
    :param template_name: Template to render
    :return: rendered template with form
    """
    form = SignupForm()
    if not app_settings.WEB3AUTH_SIGNUP_ENABLED:
        form.add_error(None, _("Sorry, signup's are currently disabled"))
    else:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                addr_field = app_settings.WEB3AUTH_USER_ADDRESS_FIELD
                setattr(user, addr_field, form.cleaned_data[addr_field])
                user.save()
                login(request, user, 'web3auth.backend.Web3Backend')
                return redirect(get_redirect_url(request))
    return render(request,
                  template_name,
                  {'form': form})