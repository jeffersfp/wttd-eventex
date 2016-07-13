from django.conf import settings
from django.contrib import messages
from django.core import mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


def subscribe(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)


def create(request):
    form = SubscriptionForm(request.POST)

    # If form is not valid then kinda abort
    if not form.is_valid():
        return render(request, 'subscriptions/subscription_form.html',
                      {'form': form})

    # Send email
    _send_mail('Eventex - Confirmação de inscrição',
               settings.DEFAULT_FROM_EMAIL,
               form.cleaned_data['email'],
               'subscriptions/subscription_email.txt',
               form.cleaned_data)

    Subscription.objects.create(**form.cleaned_data)

    # Success feedback
    messages.success(request, 'Inscrição realizada com sucesso!')

    return HttpResponseRedirect('/inscricao/')


def new(request):
    context = {'form': SubscriptionForm()}
    return render(request, 'subscriptions/subscription_form.html', context)


def _send_mail(subject, _from, to, template, context):
    body = render_to_string(template, context)
    mail.send_mail(subject, body, _from, [_from, to])
