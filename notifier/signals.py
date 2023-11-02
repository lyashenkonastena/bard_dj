from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from board.models import Reply
from .tasks import send_reply_notification


@receiver(post_save, sender=Reply)
def notify_user_new_reply(sender, instance, created, **kwargs):
    if created:
        subject = f'New reply to your ad'
        send_reply_notification.delay(instance.id, subject, event='created')


@receiver(pre_save, sender=Reply)
def notify_user_reply_accepted(sender, instance, *args, **kwargs):
    if instance.id:
        if instance.accepted \
                and sender.objects.get(id=instance.id).accepted != instance.accepted:
            subject = f'Your reply accepted'
            send_reply_notification.delay(instance.id, subject, event='accepted')
