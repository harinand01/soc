import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mini_soc.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Check and update/create the admin user
user, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com'})
user.set_password('admin123')
user.is_superuser = True
user.is_staff = True
user.save()

if created:
    print("Superuser created successfully! (Username: admin, Password: admin123)")
else:
    print("Superuser password updated successfully! (Username: admin, Password: admin123)")
