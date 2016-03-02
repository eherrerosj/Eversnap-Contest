import ez_setup
ez_setup.use_setuptools()


from setuptools import setup, find_packages
import ez_setup
setup(
    name = "ever",
    version = "0.1",
    packages = find_packages(),
    install_requires = ['django-celery', 'celery', 'twython', 'django', 'djangorestframework', 'markdown', 'django-filter'],
    author = "Enrique Herreros",
    author_email = "eherrerosj@gmail.com",
    description= "This package contains the everhashtag django project. It is a smart automatic album creator. It fetches Twitter pictures under any specified hashtag periodically and stores them in a database with other info like times favorited, owner, date of upload, date of storage... Main features: email notification every 100 pictures album growth, automatic collage creation for top 7 pictures, nice gallery to view all the stored pictures for every album.",
    keywords = "eversnap contest assignment everhashtag collector ever twitter entities pictures smart-album",
)