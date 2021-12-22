from django.dispatch import Signal

__all__ = [
    'reset_password_token_created',
    'pre_password_reset',
    'post_password_reset',
]

reset_password_token_created = Signal()

pre_password_reset = Signal()

post_password_reset = Signal()
