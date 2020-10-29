from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from .models import *
import string
from random import *
import requests


def recaptcha_checker(recaptcha_response):
    data = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result = r.json()
    if result['success']:
        return True
    else:
        return False


def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    context = {

    }
    if 'loginerr' in request.COOKIES:
        err = request.COOKIES['loginerr'].split('|')
        msg = err[0]
        case = err[1]
        context['msg'] = msg
        context['case'] = case

        res = render(request, 'login.html', context)
        res.delete_cookie('loginerr')
        return res
    else:
        return render(request, 'login.html', context)


def signinpro(request):
    email = request.POST['email']
    password = request.POST['password']
    # recaptcha_response = request.POST.get('g-recaptcha-response')
    # rec_checker = recaptcha_checker(recaptcha_response)
    # if rec_checker == True:
    re = authenticate(username=email, password=password)
    if re is not None:
        return redirect('dashboard')
    else:
        res = redirect('login')
        res.set_cookie('loginerr','Wrong email or password|danger')
        return res
    # else:
    #     return redirect('login')


def signup(request):
    context = {

    }
    if 'signuperr' in request.COOKIES:
        err = request.COOKIES['signuperr'].split('|')
        msg = err[0]
        case = err[1]
        context['msg'] = msg
        context['case'] = case

        res = render(request, 'signup.html', context)
        res.delete_cookie('signuperr')
        return res
    else:
        return render(request, 'signup.html', context)


def signuppro(request):
    fname = request.POST['fname']
    lname = request.POST['lname']
    email = request.POST['email']
    password = request.POST['password']
    code = ""
    # recaptcha_response = request.POST.get('g-recaptcha-response')
    # rec_checker = recaptcha_checker(recaptcha_response)
    # if rec_checker == True:
    if User.objects.filter(username=email).exists() or changemail.objects.filter(email=email).exists():
        res = redirect('signup')
        res.set_cookie('signuperr','Email is already registered|danger')
        return res
    else:
        def recursed_trials():
            try:
                letters = string.ascii_letters
                digits = string.digits
                chars = letters + digits
                min_length = 25
                max_length = 25
                code = "".join(choice(chars) for x in range(randint(min_length, max_length)))
                insertuser = hanguser.objects.get_or_create(email=email, first_name=fname, last_name=lname, password=password, code=code)
                insertuser.save()
            except:
                return recursed_trials()
        recursed_trials()
        subject = 'Email verification link'
        message = 'Thanks for registeration'
        msg_html = render_to_string('mails/email.html', {'code': code, 'rec_username': str(fname)+' '+str(lname)})
        from_email = settings.EMAIL_HOST_USER
        to_list = [email, settings.EMAIL_HOST_USER]
        send_mail(subject, message, from_email, to_list, html_message=msg_html, fail_silently=True)
        return render(request,'msgs/successreg.html')
    # else:
    #     return redirect('signup')

def verify(request, code):
    if hanguser.objects.filter(code=code).exists():
        verifying_user = hanguser.objects.get(code=code)
        insertuser = User.objects.create_user(username=verifying_user.email, email=verifying_user.email, password=verifying_user.password)
        insertuser.first_name = verifying_user.first_name
        insertuser.last_name = verifying_user.last_name
        insertuser.save()
        verifying_user.delete()
        return redirect('login')
    else:
        return redirect('home')

def forgot(request):
    context = {

    }
    if 'forgoterr' in request.COOKIES:
        err = request.COOKIES['forgoterr'].split('|')
        msg = err[0]
        case = err[1]
        context['msg'] = msg
        context['case'] = case

        res = render(request, 'forgot.html', context)
        res.delete_cookie('forgoterr')
        return res
    else:
        return render(request, 'forgot.html', context)

def sendrescode(request):
    email = request.POST['email']
    code = ""
    if User.objects.filter(username=email).exists():
        user = User.objects.get(username=email)
        def recursed_passreset_trials():
            try:
                letters = string.ascii_letters
                digits = string.digits
                chars = letters + digits
                min_length = 25
                max_length = 25
                code = "".join(choice(chars) for x in range(randint(min_length, max_length)))
                resetinguser = resetpasscode.objects.get_or_create(user=user, code=code)
                resetinguser.save()
            except:
                return recursed_passreset_trials()
        recursed_passreset_trials()
        subject = 'Password reset link'
        message = 'There\'s a trial to reset your password'
        msg_html = render_to_string('mails/reset.html', {'code': code, 'rec_username': str(user.first_name) + ' ' + str(user.last_name)})
        from_email = settings.EMAIL_HOST_USER
        to_list = [email, settings.EMAIL_HOST_USER]
        send_mail(subject, message, from_email, to_list, html_message=msg_html, fail_silently=True)
        return redirect('resetpass')
    else:
        res = redirect('forgot')
        res.set_cookie('forgoterr','This email doesn\'t exist|danger')
        return res

def resetpass(request, code):
    context = {
        'code': code,
    }
    if 'reseterr' in request.COOKIES:
        err = request.COOKIES['reseterr'].split('|')
        msg = err[0]
        case = err[1]
        context['msg'] = msg
        context['case'] = case

        res = render(request, 'reset.html', context)
        res.delete_cookie('reseterr')
        return res
    else:
        return render(request, 'reset.html', context)

def resetpasspro(request, code):
    password = request.POST['password']
    repass = request.POST['repass']
    if password == repass:
        if resetpasscode.objects.filter(code=code).exists():
            resetpasscode_instance = resetpasscode.objects.get(code=code)
            user = resetpasscode.objects.get(code=code).user
            user.set_password(password)
            user.save()
            resetpasscode_instance.delete()
            return redirect('login')
        else:
            return redirect('home')
    else:
        res = redirect('resetpass')
        res.set_cookie('reseterr','Passwords don\'t match|danger')
        return res

def account(request):
    context = {
        'user': request.user,
    }
    if 'accounterr' in request.COOKIES:
        err = request.COOKIES['accounterr'].split('|')
        msg = err[0]
        case = err[1]
        context['msg'] = msg
        context['case'] = case

        res = render(request, 'account.html', context)
        res.delete_cookie('accounterr')
        return res
    else:
        return render(request, 'account.html', context)


def change_account_settings(request, type):
    user = request.user
    if type == 'fname':
        fname = request.POST['fname']
        user.first_name = fname
        user.save()
    elif type == 'lname':
        lname = request.POST['lname']
        user.last_name = lname
        user.save()
    elif type == 'password':
        password = request.POST['password']
        user.set_password(password)
        user.save()
    return redirect('account')

def change_account_email(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    newemail = request.POST['email']
    code = ""
    if User.objects.filter(username=newemail).exists() or hanguser.objects.filter(email=newemail).exists():
        res = redirect('account')
        res.set_cookie('This email is taken|danger')
        return res
    else:
        def recursed_emailchanger_trials():
            try:
                letters = string.ascii_letters
                digits = string.digits
                chars = letters + digits
                min_length = 25
                max_length = 25
                code = "".join(choice(chars) for x in range(randint(min_length, max_length)))
                insertemailchanger = changemail.objects.get_or_create(user=user, newemail=newemail, code=code)
                insertemailchanger.save()
            except:
                return recursed_emailchanger_trials()
        recursed_emailchanger_trials()
        subject = 'Email verification link'
        message = 'Thanks for registeration'
        msg_html = render_to_string('mails/email.html', {'code': code, 'rec_username': str(user.first_name)+' '+str(user.last_name)})
        from_email = settings.EMAIL_HOST_USER
        to_list = [newemail, settings.EMAIL_HOST_USER]
        send_mail(subject, message, from_email, to_list, html_message=msg_html, fail_silently=True)
        res = redirect('account')
        res.set_cookie("We sent you a verification email to your new email address|success")
        return res

def verify_new_email(request, code):
    if changemail.objects.filter(code=code).exists():
        email_change_instance = changemail.objects.get(code=code)
        user = changemail.objects.get(code=code).user
        user.email = email_change_instance.newemail
        user.username = email_change_instance.newemail
        user.save()
        email_change_instance.delete()
        if request.user.is_authenticated:
            return redirect('account')
        else:
            return redirect('login')
    else:
        return redirect('home')

def checkemail(request):
    email = request.GET['email']
    if User.objects.filter(username=email).exists() or hanguser.objects.filter(email=email).exists() or resetpasscode.objects.filter(newemail=email).exists():
        return HttpResponse('exist')
    else:
        return HttpResponse('good')
