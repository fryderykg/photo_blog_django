from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify
from PIL import Image


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.User', default='request.user', verbose_name="Autor")
    title = models.CharField(blank=False, null=False, max_length=120, verbose_name="Tytuł")
    slug = models.SlugField(max_length=250, unique_for_date='created_date')
    text = models.TextField(blank=True, null=True, verbose_name="Opis")
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Data zdjęcia")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Data edycji")
    private = models.BooleanField(default=False, verbose_name="Prywatne")
    image = models.ImageField(upload_to='images',
                              blank=True, null=True,
                              verbose_name="Zdjęcie")
    thumbnail = models.ImageField(upload_to='images',
                                  blank=True, null=True,
                                  verbose_name='Miniatura')

    def save(self):
        super(Post, self).save()    # save instance

        self.image.open()           # reopen the image
        image = Image.open(self.image)
        (width, height) = image.size
        longer_side = max(image.size)
        if longer_side > 960:     # crop image to max 960 px
            factor = longer_side / 960
        else:                     # if image is smaller then no crop
            factor = 1

        new_size = (int(width / factor), int(height / factor))
        image = image.resize(new_size, Image.ANTIALIAS)
        image.save(self.image.path)

    def delete(self):
        storage, path = self.image.storage, self.image.path
        # print(storage, path)            # image object and path to it
        super(Post, self).delete()      # delete instance
        storage.delete(path)            # delete image file

    def get_absolute_url(self):
        return reverse('posts:detail',
                       args=[self.created_date.year,
                             self.created_date.strftime('%m'),
                             self.created_date.strftime('%d'),
                             self.slug])

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.title


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

