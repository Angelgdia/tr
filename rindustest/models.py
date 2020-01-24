from django.db import models
from django.contrib.auth.models import User

class BankAccountUser(models.Model):
    name = models.CharField(blank=False, null=False, max_length=25)
    surname = models.CharField(blank=False, null=False, max_length=50)
    id_number = models.CharField(unique=True, blank=False, null=False, max_length=9, )
    created_by = models.ForeignKey(User, blank=False, null=False,
                                   on_delete=models.CASCADE, related_name='bank_account_users')
    account_number = models.CharField(blank=False, null=False, max_length=16)

    def __str__(self):
        return f"{self.name} {self.surname}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if len(self.id_number) != 9:
            raise ValidationError('ID should be 9 characters long')
        if len(self.account_number) != 16:
            raise ValidationError('Bank account number should be 16 characters long')
        if not self.name or not self.surname:
            raise ValidationError('No empty fields please')
