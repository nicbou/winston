from setuptools import setup

setup(name='winston',
      version='0.1',
      description='A voice-controlled virtual butler',
      url='http://github.com/nicbou/winston',
      author='Nicolas Bouliane',
      author_email='contact@nicolasbouliane.com',
      license='LGPL',
      requires=['ping'],
      packages=['winston']
      )