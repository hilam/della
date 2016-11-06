from django.template.loader import render_to_string
from django.core.urlresolvers import reverse

from .models import UserProfile
from . import email_service
from . import activation_service


def create_user_profile(user):
    UserProfile.objects.create(user=user, is_enabled_exchange=False)


def activate_user(user):
    if user.is_active:
        return True
    user.is_active = True
    user.save()
    return True


def send_activation_email(request, user):
    message_template = 'user_manager/account_activation_email.html'
    subject_temaplte = 'user_manager/account_activation_subject.txt'
    code = activation_service.generate_key(user)
    path_params = {'username': user.username, 'code': code}
    activation_url = request.build_absolute_uri(reverse(
        'user_manager:activate-user', kwargs=path_params))
    context = {'url': activation_url, 'username': user.username}
    message = render_to_string(template_name=message_template, context=context)
    subject = render_to_string(template_name=subject_temaplte)
    email_service.send_email(subject=subject, message=message,
                             recipient_list=[user.email])
