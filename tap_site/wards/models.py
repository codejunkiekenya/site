from django.db import models
from django.contrib.auth.models import User
import numpy as np
from django.template.defaultfilters import slugify
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django_comments.moderation import CommentModerator, moderator


class Wards(models.Model):
    name = models.CharField(max_length=200)
    
    def average_rating(self):
        all_ratings = list(map(lambda x: x.rating, self.review_set.all()))
        return np.mean(all_ratings)
        
    def __unicode__(self):
        return self.name


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    wards = models.ForeignKey(Wards)
    pub_date = models.DateTimeField('date published')
    user_name = models.CharField(max_length=100)
    comment = models.CharField(max_length=2000)
    rating = models.IntegerField(choices=RATING_CHOICES)
    likes= models.IntegerField(default=0)
    dislikes= models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/wards/%Y/%m/%d',
                                null=True,
                                blank=True)

    def clean_content(self):
        if image != None:
            image = self.cleaned_data['image']
            content_type = image.content_type.split('/')[0]
            if content_type in settings.CONTENT_TYPES:
                if image._size > int(settings.MAX_UPLOAD_SIZE):
                    raise forms.ValidationError(_(u'Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content._size)))
            else:
                raise forms.ValidationError(_(u'File type is not supported'))
            return image

    def save(self, *args, **kwargs):
        self.url= slugify(self.wards)
        super(Review, self).save(*args, **kwargs)

    def __str__(self):
        return self.wards

class Cluster(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, related_name='wards')

    def get_members(self):
        return "\n".join([u.username for u in self.users.all()])

class Preference(models.Model):
    user= models.ForeignKey(User, related_name='wards_preference')
    review= models.ForeignKey(Review)
    value= models.IntegerField()
    date= models.DateTimeField(auto_now= True)

    
    def __str__(self):
        return str(self.user) + ':' + str(self.review) +':' + str(self.value)

    class Meta:
       unique_together = ("user", "review", "value")

class ReviewModerator(CommentModerator):
    email_notification = True
    auto_close_field   = 'posted_date'
    # Close the comments after 7 days.
    close_after        = 7

moderator.register(Review, ReviewModerator)
# Create your models here.
