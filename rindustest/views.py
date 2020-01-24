from urllib.request import Request
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import BankAccountUser
from .utils import urlerrors, get_bank_account_user, check_bank_account_user



@login_required(login_url='')
def main(request: Request) -> HttpResponse:
    error = "There has been an error..." if request.GET.get('error') else ''
    users = BankAccountUser.objects.filter(created_by=request.user).values()
    return render(request, 'main.html', context={'users': users, 'error': error})

@login_required(login_url='')
def manage(request: Request) -> HttpResponse:
    action = request.POST.get('action')
    previous_data = dict()
    if action == "modify":
        data = request.POST
        for k, v in data.items():
            previous_data[k] = v
    return render(request, 'manage.html', context={'user_id': request.user.pk,
                                                   'action': action,
                                                   'previous_data': previous_data
                                                   })

def create_edit(request: Request) -> HttpResponseRedirect:
    data = request.POST
    if data.get('id'):
        # Modify
        instance = get_bank_account_user(data.get('id'))
        if not instance:
            return redirect(f'/products?{urlerrors.get("NOT_FOUND")}')
        if not check_bank_account_user(instance.created_by, request.user):
            return redirect(f'/products?{urlerrors.get("NOT_ALLOWED")}')
    else:
        # Create
        instance = BankAccountUser()
    for k, v in data.items():
        if k in ["id", "csrfmiddlewaretoken"]:
            continue
        setattr(instance, k, v)
    instance.created_by = request.user
    instance.clean()
    instance.save()
    return redirect("/products")

def delete(request: Request) -> HttpResponseRedirect:
    id = request.POST.get('id')
    instance = get_bank_account_user(id)
    if not instance:
        return redirect(f'/products?{urlerrors.get("NOT_FOUND")}')
    if not check_bank_account_user(instance.created_by, request.user):
        return redirect(f'/products?{urlerrors.get("NOT_ALLOWED")}')
    instance.delete()
    return redirect("/products")


