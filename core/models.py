from django.db import models
from django_countries.fields import CountryField



from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin



class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **kwargs):
        """Create and return a `User` with an email, phone number, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')
        if email is None:
            raise TypeError('Superusers must have an email.')
        if username is None:
            raise TypeError('Superusers must have an username.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


CLIENT ="CL"
AGENT = "AG"
MY_COMPANY = "CO"
ACCESS_CONTROL_CHOICES = [(CLIENT,"Client"),(AGENT,"Agent"),(MY_COMPANY,"My_Company")]

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    email = models.EmailField(db_index=True, unique=True,  null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True,auto_now_add=True)
    access_control =  models.CharField(max_length=2,choices=ACCESS_CONTROL_CHOICES,blank=True)


    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"



# Create your models here.

    
class Category(models.Model):
    name = models.CharField(max_length=50,unique=True)
    
    def __str__(self) -> str:
        return f"{self.name}"

class Candidate(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    nationality = CountryField()
    passport_no = models.CharField(max_length=20,unique=True,null=False)
    visa_issued = models.BooleanField(default=False)
    medical_issued = models.BooleanField(default=False)
    created_by = models.CharField(max_length=254)
    cv_file_path = models.FileField(upload_to="documents/")
    category = models.ForeignKey(Category,blank=True,null=True,on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"



class Interview(models.Model):
    
    candidates = models.ManyToManyField(Candidate)
    client_name = models.CharField(max_length=50) # can be a user
    start_date = models.DateField()
    interviewer_name = models.CharField(max_length=50)
    zip_file_path = models.FileField(max_length=100,blank=True) 
    accessible_users = models.ManyToManyField(User)
    name = models.CharField(max_length=100,blank=True)
    description = models.TextField(null=True,blank=True)

    def __str__(self) -> str:
        return f"{self.client_name} --> interviewed by {self.interviewer_name} on {self.start_date}"
    
    def get_candidates(self):
        return self.candidates.all()


    
class UserInterview(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    interview = models.ForeignKey(Interview,on_delete=models.CASCADE)    
    def __str__(self) -> str:
        return f"{self.user.name}  {self.interview.name}"
    
    def get_user_name(self):
        return self.user.name

    def get_user_role(self):
        return self.user.access_control

# class Message(models.Model):
#     recipient = models.ForeignKey(User,on_delete=models.CASCADE)
#     message = models.CharField(max_length=250)
#     created_time = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)
#     updated_time = models.DateTimeField(auto_now=True)
