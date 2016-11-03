from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify

# # Create your models here.
# def upload_location(instance, filename):
#     return "%s/%s" % (instance.pk, filename)


class Post(models.Model):
    author = models.ForeignKey('auth.User', default=1, verbose_name="Autor")
    title = models.CharField(max_length=120, verbose_name="Tytuł")
    slug = models.SlugField(unique=True)
    text = models.TextField(blank=True, null=True, verbose_name="Opis")
    created_date = models.DateField(default=timezone.now, verbose_name="Data zdjęcia")
    private = models.BooleanField(default=False, verbose_name="Prywatne")
    image = models.ImageField(upload_to='images',
                              blank=True, null=True,
                              width_field='width_field',
                              height_field='height_field',
                              verbose_name="Zdjęcie")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-created_date']


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    slug = slugify(instance.title)
    exists = Post.objects.filter(slug=slug).exists()
    if exists:
        if not instance.pk:
            obj = Post.objects.first()
            instance.pk = obj.id + 1
        slug = '%s-%s' % (slug, instance.pk)
    instance.slug = slug


pre_save.connect(pre_save_post_receiver, sender=Post)

