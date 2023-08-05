from setuptools import setup


setup(name='yyes',
      python_requires='>=3.5.0',
      version='1.0.0',
      description='http',
      author='tjsh',
      author_email='2438280753@qq.com',
      maintainer='tjsh',
      maintainer_email='2438280753@qq.com',
      url='http://www.flexible-world.com:8080',
      packages=['yyes'],
      long_description="none",
      license="none",
      platforms=["?"],
      install_requires=[
            "requests>=2.6",
            "BeautifulSoup4>=2.2.1",
            "lxml>=4.6.3",
            "pywin32>=301"
      ],
      classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
      ],
      )
