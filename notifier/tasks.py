from datetime import datetime, timedelta

from celery import shared_task
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse

from blog.models import Post
from board.models import Reply


@shared_task
def send_reply_notification(reply_id, subject, event):
    base_link = get_base_link()
    reply = Reply.objects.get(id=reply_id)
    ad = reply.ad

    if event == 'created':
        template = 'notifier/reply_notification.html'
        user = ad.user
    else:
        template = 'notifier/reply_accepted.html'
        user = reply.user

    html = render_to_string(
        template,
        {
            'user': user,
            'reply': reply,
            'ad': ad,
            'ad_link': f'{base_link}{ad.get_absolute_url()}',
        }
    )
    msg = EmailMultiAlternatives(
        subject=subject,
        body=subject,
        to=[user.email]
    )
    msg.attach_alternative(html, "text/html")
    msg.send()


@shared_task
def send_blog_digest():
    base_link = get_base_link()
    last_week = last_week_range()
    frmt = '%d.%m.%y'
    subject = f'Week digest from {last_week[0].strftime(frmt)} to {last_week[1].strftime(frmt)}'
    subs = User.objects.exclude(email__isnull=True).exclude(email__exact='').filter(groups__name='common')
    posts = Post.objects.filter(create_ts__range=last_week)
    for sub in subs:
        html = render_to_string(
            'notifier/blog_digest.html',
            {
                'user': sub,
                'posts': posts,
                'posts_link': f'{base_link}{reverse("blog_list")}'
            }
        )
        msg = EmailMultiAlternatives(
            subject=subject,
            body=subject,
            to=[sub.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()


def last_week_range():
    today = datetime.today()
    last_week_end = (today - timedelta(days=(today.weekday() + 1))).replace(
        hour=23,
        minute=59,
        second=59,
        microsecond=0
    )
    last_week_start = (last_week_end - timedelta(days=6)).replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0)
    return last_week_start, last_week_end


def get_base_link() -> str:
    current_site = get_current_site(request=None)
    domain = current_site.domain
    protocol = "http"
    return f'{protocol}://{domain}'
