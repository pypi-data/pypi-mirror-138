from setuptools import setup

with open('README.md') as f:
    readme = f.read()

setup(name='logger_util',
      version='0.2.1',
      description='Dead simple Python logger. Redirects stdout to a file while maintaining console printing.',
      long_description=readme,
      long_description_content_type="text/markdown",
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.8'
      ],
      keywords='logger_util logging python wsarce',
      url='https://github.com/wsarce/logger-util',
      author='Walker Arce (wsarce)',
      author_email='wsarcera@gmail.com',
      license='MIT',
      packages=['logger_util'],
      install_requires=[
          'wmi'
      ],
      include_package_data=True,
      zip_safe=False
      )
