from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import Http404
from django.urls import reverse
from django.urls.exceptions import Resolver404
from django.views.generic import TemplateView, FormView
from .models import GeneralInfo, Service, Testimonial, FrequentlyAskedQuestion, Contact, ContactForm, Blog
from .apps import AppConfig
from django.conf import settings

# Create your views here.

class IndexView( TemplateView ):
    template_name = "index.html"
    
    def get(self, request, *args, **kwargs):
        services = Service.objects.all()
        testimonial = Testimonial.objects.all()
        company_info = GeneralInfo.objects.first()
        faqs = FrequentlyAskedQuestion.objects.order_by("-frequency",).all()
        contactForm = ContactForm()
        most_recent_blogs = BlogDetailsView.get_most_recent_blogs(3)

        print( f"{AppConfig.name}:{ContactView.__name__}" )

        return render( 
            request=request, 
            template_name=self.template_name, 
            context= {
                "company_info" : company_info,
                "services" : services,
                "testimonials" : testimonial,
                "faqs" : faqs,
                "contactForm" : {
                    "url" : f"{AppConfig.name}:{ContactView.get_url_name()}",
                    "form" : contactForm
                },
                "blogs" : most_recent_blogs
            }
        )

    @staticmethod
    def get_url_name():
        return "index"
    
class ContactView( FormView ):

    form_class = ContactForm

    def post(self, request, *args, **kwargs):
        
        form = ContactForm( request.POST )

        if form.is_valid():
            # Save and retrive the contact object
            contact : Contact = form.save( commit=False )

            # Attempt to mail in the contact
            try:
                send_mail(
                    subject=contact.subject,
                    message=f"{contact}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.EMAIL_HOST_USER],
                    fail_silently=False
                )
                messages.success(request=request, message="Email sent successfully")
            except Exception as e:
                contact.error = f"{e}"
                messages.error(request=request, message="Email Failed to send")
            finally:
                contact.save()

        else:
            return Resolver404()
        
        return redirect( to=f"{AppConfig.name}:{IndexView.get_url_name()}" )

    def get(self, request, *args, **kwargs):
        return redirect( to=f"{AppConfig.name}:{IndexView.get_url_name()}" )
    
    @staticmethod
    def get_url_name():
        return "contact"
    
class BlogDetailsView( TemplateView ):

    template_name = "blog-details.html"
    blogIdKey = "blogId"

    @staticmethod
    def get_url_name() -> str:
        return "blog-details"

    def get(self, request, *args, **kwargs):

        # retrieve the correspoongin blog ID
        blogId = kwargs.get(self.blogIdKey)

        if blogId is None:
            raise Http404("Blog Id Not supplied")
        
        blog = Blog.objects.get(pk=blogId)
        most_recent = self.get_most_recent_blogs(3)

        return render(
            request=request,
            template_name=self.template_name,
            context={
                "blog" : blog,
                "most_recent" : most_recent
            }
        )
    
    @staticmethod
    def get_most_recent_blogs( count ) -> list[Blog]:
        count = min( count, Blog.objects.count() )
        return  Blog.objects.all().order_by("-created_at")[:count]
    
class BlogsView( TemplateView ):
    template_name = "blog.html"

    @staticmethod
    def get_url_name():
        return "blogs"
    
    @staticmethod
    def setup_page( data : list[object], num_items_per_pages : int ):
        return Paginator( data, num_items_per_pages )
    
    def get(self, request, *args, **kwargs):
        
        pages = self.setup_page( Blog.objects.all(), 1 )

        page_num = kwargs.get("page")

        if page_num is None:
            page_num = 1

        return render( 
            request=request,
            template_name=self.template_name,
            context={
                "blogs" : pages.page(page_num)
            }
        )


