from django.shortcuts import render,HttpResponse,redirect
from .forms import UserForm
from .models import User
from django.contrib import messages

# Create your views here.
def registerUser(request):
  if request.method == 'POST':
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
      return redirect('registerUser')
    else:
      print("Errors in Registration form ")
      print(form.errors)
  else:
    form  = UserForm()
  context = {
    'form': form,
  }
  return render(request,'accounts/registerUser.html',context)
