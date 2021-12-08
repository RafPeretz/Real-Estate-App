from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth import authenticate
from django.contrib import auth
from contacts.models import Contact


# from django.contrib import messages
# from django.contrib import auth
# from django.contrib.auth.models import User
# # from contacts.models import Contact
#

# Create your views here.
def register(request):
    # AFTER VIDEOS RETURN TO SWAP REGISTER MODE TO AUTO
    # SIGN IN BY USING SIGNALS
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is already taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is currently being used')
                    return redirect('register')
                else:
                    user = User.objects.create_user(
                        username=username,
                        password=password,
                        email=email,
                        first_name=first_name,
                        last_name=last_name
                    )
                    user.save()
                    user = authenticate(username=username, password=password2)
                    if user is not None:
                        print('User is authenticated')
                        login(request)
                        messages.success(request, 'You are now registered and can log in')
                        # REMEMBER TO USE A SIGNAL FOR AUTO LOG IN
                        return redirect('index')
                    else:
                        print('user is NOT authenticated')
                        return redirect('register')
        else:
            messages.error(request, 'Your passwords did not match')
            return redirect('register')

    else:
        return render(request, 'accounts/register.html')


def login(request):
    # AFTER VIDEOS RETURN TO ADD A FETCH
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Either incorrect username or password. Try again')
            # USE FETCH FOR AUTO RESET OF DATA
            # WITHOUT RELOADING THE PAGE
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {
        'contacts': user_contacts
    }
    return render(request, 'accounts/dashboard.html', context)


def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request, 'You are LOGGED OUT !')
    return render(request, 'accounts/dashboard.html')

# def register(request):
#     # AFTER VIDEOS RETURN TO SWAP REGISTER MODE TO AUTO
#     # SIGN IN BY USING SIGNALS
#     if request.method == "POST":
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         password2 = request.POST['password2']
#
#         if password == password2:
#             if User.objects.filter(username=username).exists():
#                 messages.error(request, 'That username is already taken')
#                 return redirect('register')
#             else:
#                 if User.objects.filter(email=email).exists():
#                     messages.error(request, 'That email is currently being used')
#                     return redirect('register')
#                 else:
#                     user = User.objects.create_user(
#                         username=username,
#                         password=password,
#                         email=email,
#                         first_name=first_name,
#                         last_name=last_name
#                     )
#                     user.save()
#                     user = authenticate(username=username, password=password2)
#                     if user is not None:
#                         print('User is authenticated')
#                         login(request)
#                         messages.success(request, 'You are now registered and can log in')
#                         # REMEMBER TO USE A SIGNAL FOR AUTO LOG IN
#                         return redirect('index')
#                     else:
#                         print('user is NOT authenticated')
#                         return redirect('register')
#         else:
#             messages.error(request, 'Your passwords did not match')
#             return redirect('register')
#
#     else:
#         return render(request, 'accounts/register.html')
#
#
# def login(request):
#     # AFTER VIDEOS RETURN TO ADD A FETCH
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#
#         user = auth.authenticate(username=username, password=password)
#
#         if user is not None:
#             auth.login(request, user)
#             messages.success(request, 'You are now logged in')
#             return redirect('dashboard')
#         else:
#             messages.error(request, 'Either incorrect username or password. Try again')
#             # USE FETCH FOR AUTO RESET OF DATA
#             # WITHOUT RELOADING THE PAGE
#             return redirect('login')
#     else:
#         return render(request, 'accounts/login.html')
#
#
# def dashboard(request):
#     user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
#     context = {
#         'contacts': user_contacts
#     }
#     return render(request, 'accounts/dashboard.html', context)
#
#
# def logout(request):
#     if request.method == 'POST':
#         auth.logout(request)
#         messages.success(request, 'You have been logged out')
#         return redirect('index')
