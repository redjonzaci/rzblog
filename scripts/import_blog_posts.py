import csv

from django.contrib.auth.models import User

from blog.models import Blog, Blogger


def run():
    fhand = open('blog/blog_posts.csv')
    reader = csv.reader(fhand)

    for row in reader:
        u = User.objects.get(username=row[2])
        a, created = Blogger.objects.get_or_create(user=u)
        blog = Blog(title=row[0], description=row[1], author=a)
        blog.save()
