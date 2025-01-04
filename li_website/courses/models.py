from django.db import models
from django.utils.text import slugify
from django.conf import settings

class Course(models.Model):
    """
    Represents a course in the system.
    
    This model stores all information about a course, including its content,
    pricing, and media attachments. Each course can be purchased by users
    and has both free and paid content sections.
    
    Attributes:
        title (str): The name of the course
        summary (str): A brief overview of the course
        description (str): Detailed description of the course
        expectation (str): What students can expect to learn
        free_part (str): Content available before purchase
        full_course (str): Complete course content (only for purchased users)
        price (Decimal): Course price
        duration (int): Course length in weeks
        slug (str): URL-friendly version of the title
        image (ImageField): Course cover image
        link_video (URL): Link to course preview video
    """
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    expectation = models.TextField(blank=True)
    free_part = models.TextField(blank=True)
    full_course = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=1)
    duration = models.PositiveIntegerField(help_text="Duration in weeks")
    slug = models.CharField(max_length=255, blank=True, unique=True)
    image = models.ImageField(upload_to='courses/images', blank=True, null=True)
    link_video = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """
        Override save method to automatically generate slug from title
        if it doesn't exist.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def is_purchased_by(self, user):
        """
        Check if the course has been purchased by a specific user.
        
        Args:
            user: The user to check for purchase
            
        Returns:
            bool: True if user has purchased the course, False otherwise
        """
        return Purchase.objects.filter(user=user, course=self).exists()

    def get_embed_url(self):
        """
        Return the VK video embed URL.
        
        The link_video field should contain the complete VK embed URL in format:
        https://vk.com/video_ext.php?oid=XXX&id=XXX&hd=2&hash=XXX
        
        Returns:
            str: VK video embed URL or empty string if no link
        """
        if not self.link_video:
            return ''
        
        # Return the URL directly if it's already in embed format
        if 'video_ext.php' in self.link_video:
            return self.link_video
            
        return ''

class Purchase(models.Model):
    """
    Represents a course purchase by a user.
    
    This model tracks when users purchase courses, creating a record of
    the transaction and enabling access to the full course content.
    
    Attributes:
        user (FK): Reference to the user who made the purchase
        course (FK): Reference to the purchased course
        purchase_date (DateTime): When the purchase was made
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"