import os

from setuptools import setup

from metrics import __version__


README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='django-metrics',
    version='.'.join(map(str, __version__)),
    packages=['metrics'],
    include_package_data=True,
    license='BSD License',  # example license
    description='',
    long_description=README,
    url='',
    author='Sergey Sorokin, Denis Voskvitsov',
    author_email='40inss@gmail.com',
    install_requires = [
        'mixpanel==4.5.0',
        'celery>=3.1.9,<=3.99',
        'requests>=2.0,<2.99',
        'django-ipware==1.1.1',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
