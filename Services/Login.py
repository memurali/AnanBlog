from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse



@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Logged in successfully'})
            # return redirect('/Blogs')
        else:
            return JsonResponse({'message': 'Invalid username or password'})
            # messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('Login')


@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('Confirm_password')

        # Validation for missing fields
        if not username or not password or not confirm_password:
            return JsonResponse({'message': 'All fields are required'})

        # Validate password match
        if password != confirm_password:
            return JsonResponse({'message': 'Passwords do not match'})

        # Check if username exists in auth_user table
        if User.objects.filter(username=username).exists():
            return JsonResponse({'message': 'Username already exists'})

        # Create user (record inserted into auth_user table)
        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()

            # Automatically log in the user
            # login(request, user)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return JsonResponse({'message': 'Your account has been created'})

        except Exception as e:
            # Catch unexpected errors
            return JsonResponse({'message': f'An error occurred: {str(e)}'}, status=500)

    # For non-POST requests, render the signup page
    return render(request, 'Signup.html')


# @login_required
# def dashboard(request):
#     return render(request, 'dashboard.html')
