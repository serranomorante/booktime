from io import BytesIO
import logging
from PIL import Image
from django.contrib.auth.signals import user_logged_in
from django.core.files.base import ContentFile
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.conf import settings
# from rest_framework.authtoken.models import Token

from .models import ProductImage  # , Basket, OrderLine, Order

THUMBNAIL_SIZE = (300, 300)

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=ProductImage)
def generate_thumbnail(sender, instance, **kwargs):
    logger.info(
        "Generating thumbnail for product %d",
        instance.product.id,
    )
    image = Image.open(instance.image)
    image = image.convert("RGB")
    image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

    temp_thumb = BytesIO()
    image.save(temp_thumb, "JPEG")
    temp_thumb.seek(0)

    # set save=False, otherwise it will run in an infinite loop
    instance.thumbnail.save(
        instance.image.name,
        ContentFile(temp_thumb.read()),
        save=False,
    )
    temp_thumb.close()
