from setuptools import setup , find_packages

classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python'
]







setup(name='shakhs',
      version='0.0.2',
      description='this package generate personal details of fake iranian person',
      long_description_content_type='text/markdown',
      long_description=open('README.txt').read()+'\n\n'+open('CHANGELOG.txt').read(),
      author='samrand majnooni',
      author_email='sammajnoni@gamil.com',
      url='https://pypi.org/project/shakhs/',
      license='MIT',
      keywords=['fake', 'persian','name','person','id','lastname'],
      packages=find_packages(),
      classifiers=classifiers,
      install_requiers=[''], 
      project_urls = {
          'HomePage': 'https://github.com/samrand-majnooni/IR-fake-person-generator'}
     )