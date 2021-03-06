# Python
from datetime import datetime, timedelta

# Django
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse

# Third party
from subscription.models import UserSubscription

# AstroBin
from astrobin_apps_notifications.utils import push_notification


class Command(BaseCommand):
    help = "Send a notification to user when their premium subscription " +\
           "is expired."

    def handle(self, *args, **kwargs):
        user_subscriptions = UserSubscription.objects.filter(
            subscription__group__name__in = ['astrobin_lite', 'astrobin_premium'],
            subscription__recurrence_unit = None,
            expires = datetime.now() - timedelta(days = 1))

        for user_subscription in user_subscriptions:
            push_notification([user_subscription.user], 'expired_subscription', {
                'user_subscription': user_subscription,
                'url': settings.BASE_URL + reverse('subscription_detail', kwargs = {
                    'object_id': user_subscription.subscription.pk
                })
            })
