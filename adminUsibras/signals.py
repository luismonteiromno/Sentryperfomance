from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.response import TemplateResponse
from urllib import request
from .models import Books

CRITICAL = 50


@receiver(post_save, sender=Books)
def notify_admin(sender, instance, created, **kwargs):
    if created:
        message = f"Novo livro criado: {instance.title}"
        print(message)
        return TemplateResponse(request, 'index.html', {'message': message})


