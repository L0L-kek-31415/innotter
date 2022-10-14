from celery import shared_task
from decouple import config
from django.core.mail import send_mail

from main.models import Page


@shared_task
def email_for_followers(page_id):
    page = Page.objects.prefetch_related("followers").filter(id=page_id).first()
    users = page.followers.all()
    emails = users.values_list("email")
    if emails:
        send_mail(
            subject="hello",
            message=f"A new post appeared on the {page.name}-page.",
            from_email=config("EMAIL_HOST_USER"),
            recipient_list=[emails],
        )
