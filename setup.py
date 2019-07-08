from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='errorprop',
      version='1.0.0',
      description='todo',
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
      ],
      long_description=readme(),
      keywords='propagation uncertainties symbolic latex fitting error',
      url='https://github.com/ev1313/errorprop',
      author='Tim Blume',
      author_email='errorprop@3nd.io',
      license='BSD',
      packages=['errorprop'],
      install_requires=[
          'numpy','sympy','uncertainties','scipy'
      ],
      include_package_data=True,
      zip_safe=False)
