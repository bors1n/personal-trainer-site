from django.shortcuts import render
from courses.models import Course

def home(request):
    courses = Course.objects.all()[:3]  # Get the first 3 courses
    reviews = [
        {'image': 'images/review_1.jpg', 'alt': 'Review 1'},
        {'image': 'images/review_2.jpg', 'alt': 'Review 2'},
        {'image': 'images/review_3.jpg', 'alt': 'Review 3'},
        {'image': 'images/review_4.jpg', 'alt': 'Review 4'},
    ]
    context = {
        'courses': courses,
        'reviews': reviews,
    }
    return render(request, 'home.html', context)