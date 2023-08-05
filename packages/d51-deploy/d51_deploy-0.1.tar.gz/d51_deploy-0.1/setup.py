from setuptools import setup
import os

setup(name='d51_deploy',
      version='0.1',
      description='On-prem deployment tool',
      long_description=open(os.path.join('README.md')).read(),
      long_description_content_type='text/markdown',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python :: 3.10',
        'Topic :: Utilities',
        'Topic :: Desktop Environment'
      ],
      keywords="deploy windows on-prem",
      url='https://github.com/MCVSD51/d51_deploy',
      author='Toby Farley',
      author_email='toby.farley@d51schools.org',
      license='MIT',
      packages=['d51_deploy'],
      install_requires=[
          'd51_dirsync',
          'requests',
          'urllib3'
      ],
      entry_points = {
        'console_scripts': ['d51_deploy=d51_deploy.command_line:main'],
      },      
      include_package_data=True,
      zip_safe=False)