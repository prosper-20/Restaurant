from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

CATEGORY_CHOICES = (
    ('S', 'Snacks'),
    ('E', 'Entre'),
    ('D', 'Drink'),
    ('A', 'Appetizer'),
    ('MC', 'Main Course')
)

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(help_text="Be Expressive")
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=3)
    image = models.ImageField()
    url = models.URLField(default="http://www.youtube.com/embed/cxB4ACaaR4I")


    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("post_detail", kwargs={
    #         'slug': self.slug
    #     })


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField('Enter your commment...')
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.name}"

    # def get_absolute_url(self):
    #     return reverse("post_detail", kwargs={
    #         'slug': self.slug
    #     })
