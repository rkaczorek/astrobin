from django.conf import settings
from django.db.models import signals
from django.utils.translation import ugettext_lazy as _
from notification import models as notification

# Fields:
# 0 - notice label
# 1 - display name
# 2 - description
# 3 - default: if value >= 2, send e-mail by default
NOTICE_TYPES = (
    (
        'new_follower',
        _('You have a new follower'),
        '',
        2
    ),
    (
        'follow_success',
        _('Following a user was successful'),
        '',
        0
    ),
    (
        'unfollow_success',
        _('Unfollowing a user was successful'),
        '',
        0
    ),
    (
        'new_image',
        _('New image from a user you follow'),
        '',
        2
    ),
    (
        'attention_request',
        _('Image brought to your attention'),
        '',
        2
    ),
    (
        'new_image_revision',
        _('New image revision from a user you follow'),
        '',
        2
    ),
    (
        'image_ready',
        _('Your image is ready'),
        '',
        0
    ),
    (
        'image_solved',
        _('Your image was plate-solved'),
        '',
        2
    ),
    (
        'image_not_solved',
        _('Your image could not be plate-solved'),
        '',
        2
    ),
    (
        'request_fulfilled',
        _('Your request was fulfilled'),
        '',
        2
    ),
    (
        'image_deleted',
        _('Your image was deleted'),
        '',
        0
    ),
)


def create_notice_types(app, created_models, verbosity, **kwargs):
    for notice_type in NOTICE_TYPES:
        notification.create_notice_type(notice_type[0],
                                        notice_type[1],
                                        notice_type[2],
                                        notice_type[3])


signals.post_syncdb.connect(create_notice_types, sender=notification)

