from django.db import models

from django.contrib.auth.models import AbstractUser, AbstractBaseUser

from utils.models import BaseModel

from django.contrib.auth.base_user import BaseUserManager

from django.core.validators import MaxValueValidator, MinValueValidator

from django.core.exceptions import PermissionDenied
# Create your models here.
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class University(BaseModel):
    name = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return self.name

class department(BaseModel):
    name = models.CharField(max_length=45)
    hod = models.CharField(max_length=45)
    uni = models.ForeignKey(University, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name

class User(AbstractUser, BaseModel):
    SUPERVISOR = "supervisor"
    STUDENT = "student"
    PMO = "fyp_panel"
    SUPER = "admin"
    USER_ROLES = (
        (SUPERVISOR, SUPERVISOR),
        (STUDENT, STUDENT),
        (PMO, PMO),
        (SUPER, SUPER)
    )

    username = None
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=30)
    phoneno = models.CharField(max_length=50)
    department = models.ForeignKey(department, on_delete=models.RESTRICT, related_name='department') #, default=1
    uni = models.ForeignKey(University, on_delete=models.RESTRICT)
    role = models.CharField(choices=USER_ROLES, max_length=20, null=True)
    otp = models.CharField(max_length=20, null=True, blank=True)

    objects = CustomUserManager()
    # username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def delete(self, *args, **kwargs):
        if self.role == 'admin' or self.is_superuser==True:
            raise PermissionDenied("Deletion of admin user not allowed www")
        super(User, self).delete(*args, **kwargs)

class fyppanel(BaseModel):
    VARIFIED = "varified"
    UNVARIFIED = "unvarified"
    varify = (
        (VARIFIED, VARIFIED),
        (UNVARIFIED, UNVARIFIED)
    )
    user = models.OneToOneField("core.User", on_delete=models.RESTRICT)
    facultyid = models.CharField(max_length=45, unique=True)       
    designation = models.CharField(max_length=45)
    var = models.CharField(choices=varify, max_length=20, null=True)

    def __str__(self):
        return self.user.name
    
class supervisor(BaseModel):
    user = models.OneToOneField("core.User", on_delete=models.RESTRICT, related_name='user')
    faculty_no = models.CharField(max_length=45, unique=True)
    field_of_interest = models.CharField(max_length=45)
    designation = models.CharField(max_length=45, default=False)

    def __str__(self):
        return self.user.name
    

class milestone(BaseModel):
    milestone_name = models.CharField(max_length=75,unique=True)
    document_submission_date = models.DateField()
    milestone_defending_date = models.DateField()
    milestone_details = models.CharField(max_length=500)
    department = models.ForeignKey(department, on_delete=models.RESTRICT)
    rubrics = models.JSONField()
    marks = models.FloatField(default=50.0)

    def __str__(self):
        return self.milestone_name

class notification(BaseModel):
    title = models.CharField(max_length=75)
    isactive = models.BooleanField(default=False)
    description = models.CharField(max_length=500)
    createdby = models.ForeignKey(User, on_delete=models.RESTRICT)
    department = models.ForeignKey(department, on_delete=models.RESTRICT)
    createdate = models.DateField()
    createtime = models.TimeField()

    def __str__(self):
        return self.title

class project(BaseModel):
    title = models.CharField(max_length=100, unique=True)
    year =  models.CharField(max_length=50, default=False)
    batch = models.CharField(max_length=50)
    no_of_group_members = models.IntegerField(default=3,
            validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
    )
    description = models.TextField()
    status = models.CharField(max_length=45,default="ongoing")
    domain = models.CharField(max_length=45)
    grade = models.FloatField(default=0)
    supervisor = models.ForeignKey(supervisor, on_delete=models.RESTRICT, null=True, blank=True, related_name="projects")
    department = models.ForeignKey(department, on_delete=models.RESTRICT)
    milestone = models.ManyToManyField(milestone)
    notification = models.ManyToManyField(notification)

    def __str__(self):
        return self.title


class teamMember(BaseModel):
    user = models.OneToOneField("core.User", on_delete=models.RESTRICT)
    rollno = models.CharField(max_length=50, unique=True)
    grade = models.FloatField(default=0)
    seatno = models.CharField(max_length=50, unique=True)
    enrollmentno = models.CharField(max_length=50, unique=True)
    project = models.ForeignKey(project, null=True, on_delete=models.RESTRICT)

    def __str__(self):
        return self.user.name
