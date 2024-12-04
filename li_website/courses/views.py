from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Purchase

def course_page(request, slug):
    """
    Display the course details page.
    
    Shows course information including title, description, and preview content.
    If the user is authenticated, also shows their purchase status.
    
    Args:
        request: HTTP request object
        slug (str): URL slug of the course
        
    Returns:
        Rendered course page with context including course details
        and purchase status
    """
    course = get_object_or_404(Course, slug=slug)
    has_purchased = False
    
    if request.user.is_authenticated:
        has_purchased = course.is_purchased_by(request.user)
    
    context = {
        'course': course,
        'has_purchased': has_purchased,
    }
    return render(request, 'courses/course_page.html', context)

@login_required
def purchase_course(request, slug):
    """
    Handle course purchase requests.
    
    Creates a purchase record for the authenticated user. Only processes
    POST requests and ensures the course hasn't already been purchased.
    
    Args:
        request: HTTP request object
        slug (str): URL slug of the course
        
    Returns:
        Redirects to course page with success/error message
    """
    if request.method != 'POST':
        return redirect('course_page', slug=slug)
        
    course = get_object_or_404(Course, slug=slug)
    
    if not course.is_purchased_by(request.user):
        try:
            Purchase.objects.create(user=request.user, course=course)
            messages.success(request, 'Курс успешно приобретен!')
        except Exception as e:
            messages.error(request, 'Произошла ошибка при покупке курса.')
    
    return redirect('course_page', slug=slug)

@login_required
def full_course_view(request, slug):
    """
    Display the full course content for purchased users.
    
    Shows the complete course content only if the user has purchased the course.
    Otherwise redirects to the course page with an error message.
    
    Args:
        request: HTTP request object
        slug (str): URL slug of the course
        
    Returns:
        Rendered full course page or redirect to course page if not purchased
    """
    course = get_object_or_404(Course, slug=slug)
    
    if not course.is_purchased_by(request.user):
        messages.error(request, 'Для доступа к полному курсу необходимо его приобрести')
        return redirect('courses:course_page', slug=slug)
    
    context = {
        'course': course
    }
    return render(request, 'courses/full_course.html', context)