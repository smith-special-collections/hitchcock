from django.db import models
from polymorphic.models import PolymorphicModel
from django.dispatch import receiver
from django.conf import settings
from .validators import validate_video, validate_audio, validate_text
import os

class Upload(PolymorphicModel):
    """ Generic "Upload" model for subclassing to the content specific models.
    """
    FORM_TYPES = [
        ('digitized', 'Digitized'),
        ('born_digital', 'Born Digital'),
    ]
    
    title = models.CharField(max_length=1024)
    identifier = models.CharField(max_length=512, help_text='barcode, ISBN, etc.')
    form = models.CharField(max_length=16, choices=FORM_TYPES, default='digitized')
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    size = models.IntegerField(blank=True, null=True)
    @property
    def name(self):
        if self.upload.name is not None:
            return self.upload.name.split('/')[-1]
        else:
            return None
    # @property
    # def size(self):
    #     """Return size in MB
    #     """
    #     return '%0.2fMB' % (self.upload.size/1000000)

    def __str__(self):
        return self.title


### Text i.e. pdf ###
def text_upload_path(instance, filename):
    """Calculate the appropriate path to upload text files to, depending
    on the type chosen for the given text upload. So that they are easier
    to manage on the filesystem.
    """
    lookup = {
        'article': 'articles/',
        'book_excerpt': 'books-excerpt/',
        'book_whole': 'books-whole/',
        'other': 'other',
    }
    # Reimpliment filename sanitization, and collision avoidance
    storage = instance.upload.storage
    valid_filename = storage.get_valid_name(filename)
    proposed_path = settings.TEXT_SUBDIR_NAME + lookup[instance.text_type] + valid_filename
    available_filename = storage.get_available_name(proposed_path)
    return available_filename

class Text(Upload):
    upload = models.FileField(
        upload_to=text_upload_path,
        max_length=1024,
        validators=[validate_text,],
        help_text="pdf format only"
    )
    TEXT_TYPES = [
        ('article', 'Article'),
        ('book_excerpt', 'Book (excerpt)'),
        ('book_whole', 'Book (whole)'),
        ('other', 'Other'),
    ]

    text_type = models.CharField(max_length=16, choices=TEXT_TYPES, default='article', help_text="Text type cannot be changed after saving.")
    def url(self):
        if self.id is not None:
            return settings.TEXTS_ENDPOINT + self.upload.name.replace(settings.TEXT_SUBDIR_NAME, '')
        else:
            return None

### Video i.e. mp4 ###
class Video(Upload):
    upload = models.FileField(
        upload_to=settings.AV_SUBDIR_NAME + 'video/',
        max_length=1024,
        validators=[validate_video,],
        help_text="mp4 format only")
    @property
    def url(self):
        if self.id is not None:
            return settings.BASE_URL + "/videos/%s" % self.id
        else:
            return None

# Audio i.e. mp3
class Audio(Upload):
    upload = models.FileField(
        upload_to=settings.AV_SUBDIR_NAME + 'audio/',
        max_length=1024,
        validators=[validate_audio,],
        help_text="mp3 format only")
    def url(self):
        if self.id is not None:
            return settings.BASE_URL + "/audio/%s" % self.id
        else:
            return None

class AudioAlbum(Upload):
    def url(self):
        if self.id is not None:
            return settings.BASE_URL + "/audio-album/%s" % self.id
        else:
            return None

class AudioTrack(Upload):
    upload = models.FileField(
        upload_to=settings.AV_SUBDIR_NAME + 'audio/',
        max_length=1024,
        validators=[validate_audio,],
        help_text="mp3 format only")
    album = models.ForeignKey(AudioAlbum, on_delete=models.CASCADE)

# Handle deletion
@receiver(models.signals.post_delete, sender=Text)
@receiver(models.signals.post_delete, sender=Video)
@receiver(models.signals.post_delete, sender=Audio)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Upload` object is deleted.
    """
    if instance.upload:
        if os.path.isfile(instance.upload.path):
            os.remove(instance.upload.path)

# Calculate size and save it to the parent Upload object
@receiver(models.signals.pre_save, sender=Text)
@receiver(models.signals.pre_save, sender=Video)
@receiver(models.signals.pre_save, sender=Audio)
def update_upload_size(sender, instance, **kwargs):
    """Saves the file size to the Upload model
    """
    instance.size = instance.upload.size
