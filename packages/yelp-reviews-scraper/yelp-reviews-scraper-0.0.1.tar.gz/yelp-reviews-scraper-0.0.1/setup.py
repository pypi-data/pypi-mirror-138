from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='yelp-reviews-scraper',
    version='0.0.1',
    description='Yelp Reviews Scraper',
    long_description=readme(),
    classifiers = ['Programming Language :: Python',
                    'License :: OSI Approved :: MIT License',
                    'Operating System :: OS Independent',
                    'Intended Audience :: Developers',
                    'Topic :: Utilities',
    ],
    keywords='yelp reviews api sdk scraper parser extractor',
    url='https://github.com/meta-scraper/yelp-reviews-scraper-python',
    author='meta-scraper',
    author_email='michael63s@protonmail.com',
    license='MIT',
    packages=['yelp_reviews_scraper'],
    install_requires=['requests'],
    include_package_data=True,
    zip_safe=False,
    long_description_content_type='text/x-rst',
)
