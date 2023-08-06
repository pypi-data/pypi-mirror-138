from setuptools import setup, find_packages
setup(name='generate_data',
      version='0.0.1',
      description='NLP generate similar data',
      author='hcy',
      author_email='861195357@qq.com',
      requires=['bert4keras', 'keras', 'numpy'],
      packages=find_packages(),
      license='apache 3.0')