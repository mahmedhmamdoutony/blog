
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(_("title"), max_length=150)
    content = models.TextField(_("content"))
    publish_date = models.DateTimeField(_("publish datae"), auto_now_add=True)
    update_at = models.DateTimeField(_("update post"), auto_now=True)
    created_by = models.ForeignKey(User, verbose_name=_("user_created"), on_delete=models.CASCADE,related_name='created_by')
    photo = models.ImageField(_("photo"), upload_to='images/')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("user:show_post_foruser", args=[self.pk])
        

    class Meta:
        verbose_name = 'post'
        ordering = ('-publish_date',)

class Comment(models.Model):
    name = models.CharField(_("name"), max_length=150)
    email= models.EmailField(_("email"), max_length=254)
    content_commnet = models.TextField(_("comment text"))
    comment = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
    is_active = models.BooleanField(_("is active"),default=False)
    comment_date = models.DateTimeField(_("comment date"), auto_now_add=True)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ('-comment_date',)  

