from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.
class MyDetailsManager(BaseUserManager):
	def create_user(self, email, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not password:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			password=password,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

class details(AbstractBaseUser):
    name=models.CharField(max_length=20,null=False)
    email=models.EmailField(max_length=50,null=False,unique=True)
    password=models.CharField(max_length=30,null=False)
    phone_number=models.CharField(max_length=10,null=False,unique=True)
    house_no=models.CharField(max_length=10,null=False)
    society=models.CharField(max_length=20,null=False)
    nearby=models.CharField(max_length=20,null=False)
    street=models.CharField(max_length=20,null=False)
    pincode=models.CharField(max_length=6,null=False)
    area=models.CharField(max_length=20,null=False)
    city=models.CharField(max_length=20,null=False)
    state=models.CharField(max_length=20,null=False)
    date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin				= models.BooleanField(default=False)
    is_active				= models.BooleanField(default=True)
    is_staff				= models.BooleanField(default=False)
    is_superuser			= models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    objects = MyDetailsManager()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class login_log(models.Model):
    user=models.ForeignKey(details,on_delete=models.DO_NOTHING)
    time_stamp=models.DateTimeField(auto_now_add=True)

class deleted_accounts(models.Model):
    name=models.CharField(max_length=20,null=False)
    email=models.EmailField(max_length=50,null=False,unique=True)
    password=models.CharField(max_length=30,null=False)
    phone_number=models.CharField(max_length=10,null=False,unique=True)
    house_no=models.CharField(max_length=10,null=False)
    society=models.CharField(max_length=20,null=False)
    nearby=models.CharField(max_length=20,null=False)
    street=models.CharField(max_length=20,null=False)
    pincode=models.CharField(max_length=6,null=False)
    area=models.CharField(max_length=20,null=False)
    city=models.CharField(max_length=20,null=False)
    state=models.CharField(max_length=20,null=False)
    time_stamp=models.DateTimeField(auto_now_add=True)

class cart(models.Model):
    user=models.ForeignKey(details,on_delete=models.CASCADE)
    product_details=models.ForeignKey('product.details',on_delete=models.CASCADE)
    time_stamp=models.DateTimeField(auto_now_add=True)

class orders(models.Model):
    user=models.ForeignKey(details,on_delete=models.CASCADE)
    product_details=models.ForeignKey('product.details',on_delete=models.CASCADE)
    time_stamp=models.DateTimeField(auto_now_add=True)
    retailer_details=models.ForeignKey('retailer.details',on_delete=models.DO_NOTHING)
