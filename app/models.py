from django.db import models
from django.forms import ModelForm, TextInput, EmailInput, Textarea
from django.utils import timezone

# Create your models here.
class GeneralInfo( models.Model ):
    """
    Docstring for GeneralInfo: Model for storing general information for the Company 
    """
    company_name = models.CharField(max_length=255, default="Company")
    location = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    open_hours = models.CharField( max_length=100, blank=True, null=True )
    video_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    
    class Meta:
        db_table = "general_info"
        
    def __str__(self):
        return self.company_name
    

class Service( models.Model ):
    icon = models.CharField( max_length=50 )
    title = models.CharField( max_length=100 )
    description = models.CharField( max_length=255 )

    class Meta:
        db_table = "services"
    
    def __str__(self):
        return self.description
    

class Testimonial( models.Model ):

    class Rating(models.IntegerChoices):
        ONE = 1, "ONE",
        TWO = 2, "TWO"
        THREE = 3, "THREE"
        FOUR = 4, "FOUR"
        FIVE = 5, "FIVE"

    user_image = models.CharField(max_length=255, blank=True, null=True, verbose_name="User Image")
    rating_count = models.IntegerField( choices=Rating.choices )
    username = models.CharField( max_length=50 )
    user_job_title = models.CharField( max_length= 50 )
    review = models.CharField( max_length=300 )

    class Meta:
        db_table = 'testimonials'

    def __str__(self):
        return f"{self.username} ({self.user_job_title})"
    
class FrequentlyAskedQuestion( models.Model ):

    question = models.CharField( max_length=50 )
    answer = models.CharField( max_length=255 )
    frequency = models.IntegerField()

    class Meta:
        db_table = 'faq'

    def __str__(self):
        return f"{self.question}"


class Contact(models.Model):
    name = models.CharField( max_length=50, verbose_name="name" )
    email = models.EmailField( verbose_name="email" )
    subject = models.CharField( max_length=50, verbose_name="subject" )
    message = models.TextField( max_length=255 )
    timestamp = models.TimeField( auto_now=True )
    error = models.TextField( max_length=255, null=True, blank=True )

    class Meta:
        db_table = 'contacts'

    def __str__(self):
        return f"{self.email} {self.subject}"
    
class ContactForm( ModelForm ):

    class Meta:
        model = Contact
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name" : TextInput( attrs={
                "placeholder" : "Name",
                "id" : "name",
                "class" : "form-control"
            }),
            "email" : EmailInput( attrs={
                "placeholder" : "Email",
                "id" : "email",
                "class" : "form-control"
            }),
            "subject" : TextInput( attrs={
                "placeholder" : "Subject",
                "id" : "subject",
                "class" : "form-control"
            }),
            "message" : Textarea( attrs={
                "placeholder" : "Message",
                "id" : "message",
                "class" : "form-control"
            }),
        }

class Author( models.Model ):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50)
    joined_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'authors'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Blog( models.Model ):
    image = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    created_at = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    class Meta:
        db_table = 'blogs'

    def __str__(self):
        return f"{self.author}, {self.title}"