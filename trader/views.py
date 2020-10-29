from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse

def dashboard(request):
    context = {

    }
    return render(request, 'dashboard.html', context)


def marketplace(request):
    context = {

    }
    return render(request, 'marketplace.html', context)

def copyTrading(request):
    context = {

    }
    return render(request, 'copyTrading.html', context)

def profile(request):
    context = {

    }
    return render(request, 'profile.html', context)

def settings(request):
    context = {

    }
    return render(request, 'settings.html', context)


def traderAccount(request):
    context = {

    }
    return render(request, 'traderAccount.html', context)