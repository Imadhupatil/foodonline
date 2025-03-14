from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class UserMangar(BaseUserManager):
  #will contain methods
  def create_user(self,first_name,last_name,username,email,password=None):
    if not email:
      raise ValueError("User must have an email")
    if not username:
      raise ValueError("User must have an username")
    
    user = self.model(
      email=self.normalize_email(email),
      first_name=first_name,
      last_name=last_name,
      username = username
    )
    user.set_password(password)
    #using argument is used to specify DB to save user 
    #self._db save in default DB
    user.save(using=self._db)
    return user
  
  def create_superuser(self,first_name,last_name,username,email,password=None):
    user = self.create_user(
      email=self.normalize_email(email),
      username=username,
      password=password,
      first_name=first_name,
      last_name=last_name,
    )
    user.is_admin =True
    user.is_active = True
    user.is_staff = True
    user.is_superadmin = True

    user.save(using=self._db)
    return user


class User(AbstractBaseUser):

  VENDOR = 1
  CUSTOMER = 2 

  ROLE_CHOICES = (
    (VENDOR,'Vendor'),
    (CUSTOMER,'Customer'),
  )

  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  username = models.CharField(max_length=50,unique=True)
  email = models.EmailField(max_length=100,unique=True)
  phone_number = models.CharField(max_length=12,blank=True)
  role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES,null=True,blank=True)

  #required fields
  joined_date = models.DateTimeField(auto_now_add=True)
  last_login= models.DateTimeField(auto_now_add=True) 
  created_date = models.DateTimeField(auto_now_add=True)
  modified_Date = models.DateTimeField(auto_now=True)

  #admins fields
  is_admin = models.BooleanField(default=False)
  is_active = models.BooleanField(default=False)
  is_staff = models.BooleanField(default=False)
  is_superadmin = models.BooleanField(default=False)

  USERNAME_FIELD = 'email'

  REQUIRED_FIELDS = ['username','first_name','last_name']

  objects = UserMangar()

  def __str__(self):
    return self.email
  
  #return Ture if user is active and admin
  def has_perm(self,perm,obj=None):
    return self.is_admin
  
  #return Ture if user is active and superadmin
  def has_module_perms(self,app_lable):
    return True
  
  #get role of user
  def get_role(self):
    if self.role == 1:
      user_role = "Vendor"
    elif self.role == 2:
      user_role = "Customer"
    return user_role
  

class UserProfile(models.Model):
  user = models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
  profile_picture = models.ImageField(upload_to='users/profile_pictures',blank=True,null=True)
  cover_photo = models.ImageField(upload_to='users/cover_photos',blank=True,null=True)
  address_line_1 = models.CharField(max_length=50,blank=True,null=True)
  address_line_2 = models.CharField(max_length=50,blank=True,null=True)
  country = models.CharField(max_length=15,blank=True,null=True)
  state = models.CharField(max_length=15,blank=True,null=True)
  city = models.CharField(max_length=15,blank=True,null=True)
  pin_code = models.CharField(max_length=6,blank=True,null=True)
  latitude = models.CharField(max_length=20,blank=True,null=True)
  longitude = models.CharField(max_length=20,blank=True,null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.user.email 