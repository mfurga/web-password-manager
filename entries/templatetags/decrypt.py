from django import template

from entries.utils import Crypto

register = template.Library()


@register.filter(name='decrypt')
def decrypt(password):
    """Template tag that provides decryption of the given password."""
    return Crypto().decrypt(password)
