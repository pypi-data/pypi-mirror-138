from setuptools import setup

setup(
  # Needed to silence warnings (and to be a worthwhile package)
    name='enhancedmath',
    url='https://github.com/LimeGradient/advmathpy',
    author='Lime_Gradient',
    author_email='limegradientyt@gmail.com',
    # Needed to actually package something
    packages=['enhancedmath'],
    # Needed for dependencies
    install_requires=[
      'numpy',
      'scipy'
    ],
    # *strongly* suggested for sharing
    version='0.0.5',
    # The license can be anything you like
    license='MIT',
    description='Expanded and Enhanced Math Package',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)