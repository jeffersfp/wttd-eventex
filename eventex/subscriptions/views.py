from django.conf import settings
from django.core import mail
from django.http import HttpResponseRedirect, Http404
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

    subscription = Subscription.objects.create(**form.cleaned_data)
    subscription.save()

    # Send email
    _send_mail('Eventex - Confirmação de inscrição',
               settings.DEFAULT_FROM_EMAIL,
               subscription.email,
               'subscriptions/subscription_email.txt',
               {'subscription': subscription})

    return HttpResponseRedirect('/inscricao/{}/'.format(subscription.digest))


def new(request):
    context = {'form': SubscriptionForm()}
    return render(request, 'subscriptions/subscription_form.html', context)


def detail(request, digest):
    try:
        subscription = Subscription.objects.get(digest=digest)
    except Subscription.DoesNotExist:
        raise Http404
    context = {'subscription': subscription}
    return render(request, 'subscriptions/subscription_detail.html', context)


def _send_mail(subject, _from, to, template, context):
    body = render_to_string(template, context)
    mail.send_mail(subject, body, _from, [_from, to])
