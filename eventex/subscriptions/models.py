import hashlib

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Subscription(models.Model):
    name = models.CharField('nome', max_length=100)
    cpf = models.CharField('CPF', max_length=11)
    email = models.EmailField('e-mail')
    phone = models.CharField('telefone', max_length=20)
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    digest = models.CharField(max_length=64, blank=True)

    class Meta:
        verbose_name_plural = 'inscrições'
        verbose_name = 'inscrição'

    def __str__(self):
        return self.name

    def calculate_digest(self):
        h = hashlib.sha256(self.cpf.encode())
        self.digest = h.hexdigest()


@receiver(pre_save, sender=Subscription)
def set_hash(sender, instance, **kwargs):
    instance.calculate_digest()
