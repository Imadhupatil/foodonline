from django.shortcuts import render,redirect
from .forms import VendorForm
from accounts.forms import UserForm
from accounts.models import User,UserProfile
from django.contrib import messages

# Create your views here.
def registerVendor(request):
  if request.user.is_authenticated:
    messages.warning(request,"You are already logged in!!")
    return redirect('dashboard')
  elif request.method == "POST":
    form = UserForm(request.POST)
    v_form = VendorForm(request.POST,request.FILES)

    if form.is_valid() and v_form.is_valid():
      clean_data = form.cleaned_data
      first_name = clean_data['first_name']
      last_name = clean_data['last_name']
      username = clean_data['username']
      email = clean_data['email']
      password = clean_data['password']
      user = User.objects.create(first_name=first_name,last_name=last_name,username=username,email=email)
      user.set_password(password)
      user.role = User.VENDOR
      user.save()
      vendor = v_form.save(commit=False)
      user_profile = UserProfile.objects.get(user=user)
      vendor.user = user
      vendor.user_profile = user_profile
      vendor.save()
      messages.success(request,"Your account has been registered successfuly!! Please wait for approval")
      return redirect('registerVendor')
    else:
      print(form.errors)
      print(v_form.errors)

  else:
    form = UserForm()
    v_form = VendorForm()
  context = {
    'form':form,
    'v_form':v_form,
  }
  return render(request,'accounts/registerVendor.html',context)
