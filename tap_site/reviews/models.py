from django.db import models
from django.contrib.auth.models import User
import numpy as np
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django_comments.moderation import CommentModerator, moderator


class Public_Office(models.Model):
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
    public_office = models.ForeignKey(Public_Office)
    pub_date = models.DateTimeField('date published')
    user_name = models.CharField(max_length=100)
    comment = models.CharField(max_length=2000)
    rating = models.IntegerField(choices=RATING_CHOICES)
    image = models.ImageField(upload_to='images/offices/%Y/%m/%d',
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

    def __str__(self):
        return self.public_office


class Cluster(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)

    def get_members(self):
        return "\n".join([u.username for u in self.users.all()])

class ReviewModerator(CommentModerator):
    email_notification = True
    auto_close_field   = 'posted_date'
    # Close the comments after 7 days.
    close_after        = 7

moderator.register(Review, ReviewModerator)
# Create your models here.
