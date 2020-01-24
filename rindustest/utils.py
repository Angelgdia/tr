from typing import Optional
from django.contrib.auth.models import User
from .models import BankAccountUser

urlerrors = {
    'NOT_FOUND': '?error=not-found',
    'NOT_ALLOWED': 'error=not-allowed'
}

def get_bank_account_user(id: int) -> Optional[BankAccountUser]:
    if not id:
        return None
    try:
        instance = BankAccountUser.objects.get(pk=id)
    except BankAccountUser.DoesNotExist:
        return None
    return instance

def check_bank_account_user(instance_id: User, request_id: User) -> bool:
    if instance_id != request_id:
        return False
    return True
