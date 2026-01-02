from django.contrib import admin
from .models import GeneralInfo, Service, Testimonial, FrequentlyAskedQuestion, Contact, Blog, Author

@admin.register(GeneralInfo)
class GeneralInfoAdmin( admin.ModelAdmin ):
    list_display = ["company_name", "email", "phone", "open_hours"]

@admin.register(Service)
class ServiceAdmin( admin.ModelAdmin ):
    list_display = ["icon", "title", "description"]

@admin.register(Testimonial)
class TestimonialAdmin( admin.ModelAdmin ):
    list_display = [ "username", "user_job_title" ]

@admin.register(FrequentlyAskedQuestion)
class FrequentlyAskedQuestionAdmin( admin.ModelAdmin ):
    list_display = ["question", "frequency" ]

@admin.register( Contact )
class ContactAdmin( admin.ModelAdmin ):
    list_display = ["name", "email", "timestamp"]

@admin.register(Blog)
class BlogAdmin( admin.ModelAdmin ):
    list_display = ["author", "title", "category", "created_at"]

@admin.register(Author)
class AuthorAdmin( admin.ModelAdmin ):
    list_display = ["first_name", "last_name", "joined_at"]
