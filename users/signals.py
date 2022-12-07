from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from users.models import User, Product
from django.db import models


def populate_models(sender, **kwargs):

    # User group names
    user_groups = ["buyer", "seller", "staff"]

    for group in user_groups:
        group_app, created = Group.objects.get_or_create(name=group)


@receiver(post_save, sender=User)
def assign_groups(sender, instance, created, **kwargs):

    ct = ContentType.objects.get_for_model(model=Product)
    perms = Permission.objects.filter(content_type=ct)

    buyers_group = Group.objects.get(name="buyer")
    buyer_perms = perms.filter(codename="view_product").first()
    buyers_group.permissions.add(buyer_perms)

    sellers_group = Group.objects.get(name="seller")
    seller_perms = perms.all()
    sellers_group.permissions.add(*seller_perms)

    staff_group = Group.objects.get(name="staff")

    if created:
        if instance.user_type == "BUYER":
            buyers_group.user_set.add(instance)

        elif instance.user_type == "SELLER":
            sellers_group.user_set.add(instance)

        elif instance.user_type == "STAFF":
            staff_group.user_set.add(instance)

