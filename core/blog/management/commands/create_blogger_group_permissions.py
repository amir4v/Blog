from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from blog.models import Category


User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        Group.objects.all().delete()
        Permission.objects.all().delete()
        
        content_type = ContentType.objects.get_for_model(Category)
        permission = Permission.objects.create(codename='blog.view_category',
                                            name='View Category',
                                            content_type=content_type) # creating permissions
        group = Group.objects.create(name='blogger')
        group.permissions.add(permission)
        
        print('Done.')
        print(content_type)
        print(group)
        print(group.permissions.all()[0])
