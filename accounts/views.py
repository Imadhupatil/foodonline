from django.shortcuts import render,redirect
from .forms import UserForm
from .models import User
from django.contrib import messages
#for user authentication(login)
from django.contrib import auth
#for auto detect role
from .utils import detect_role
#restrict page access
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied

# authorized access to customer dashboard
def cutomer_role_check(user):
  if user.role == 2:
    return True
  else:
    raise PermissionDenied

#authorized access to vendor dashboard
def vendor_role_check(user):
  if user.role == 1:
    return True
  else:
    raise PermissionDenied


def registerUser(request):
  if request.user.is_authenticated:
    messages.warning(request,"You are already logged in!!")
    return redirect('dashboard')
  elif request.method == 'POST':
    form = UserForm(request.POST)

    if form.is_valid():
      #saving user using form
      # password = form.cleaned_data['password']
      # user = form.save(commit=False)
      # user.role = User.CUSTOMER
      # user.set_password(password)
      # user.save()

      #saving user using create_user method
      clean_data = form.cleaned_data
      first_name = clean_data['first_name']
      last_name = clean_data['last_name']
      email = clean_data['email']
      username = clean_data['username']
      password = clean_data['password']

      user= User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
      user.role = User.CUSTOMER
      user.save()
      messages.success(request,"Your account has been registered successfully")
      return redirect('myAccoount')
    else:
      print("Errors in Registration form ")
      print(form.errors)
  else:
    form  = UserForm()
  context = {
    'form': form,
  }
  return render(request,'accounts/registerUser.html',context)

@login_required(login_url='login')
def myAccount(request):
  user = request.user
  redirectURL = detect_role(user)
  return redirect(redirectURL)

def login(request):
  if request.user.is_authenticated:
    messages.warning(request,"You are already logged in!!")
    return redirect('myAccount')
  elif request.method == 'POST':
    email = request.POST['email']
    password = request.POST['password']
    
    #checking user
    user = auth.authenticate(email=email,password=password)

    if user is not None:
      auth.login(request,user)
      messages.success(request,"You have logged in successfully!!")
      return redirect('myAccount')
    else:
      messages.error(request,"Invalid credentials!!")
      return redirect('login')
  return render(request,'accounts/login.html')

def logout(request):
  auth.logout(request)
  messages.info(request,"You have logged out")
  return redirect('login')

@login_required(login_url='login')
@user_passes_test(cutomer_role_check)
def custDashboard(request):
  return render(request, 'accounts/custDashboard.html')

@login_required(login_url='login')
@user_passes_test(vendor_role_check)
def vendorDashboard(request):
  return render(request, 'accounts/vendorDashboard.html')
