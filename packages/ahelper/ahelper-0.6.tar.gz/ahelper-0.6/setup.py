from setuptools import setup, find_packages

url='https://gitee.com/EdisonLeeeee/ahelper'
VERSION = 0.6
package_data_list = ['ReFine', 'ogb']

setup(
    name='ahelper',
    version=VERSION,
    description='A helper.',
    python_requires='>=3.6',
    license="MIT LICENSE",
    author='Jintang Li',
    author_email='cnljt@outlook.com',
    url='https://gitee.com/EdisonLeeeee/ahelper',
#     download_url='{}/archive/{}.tar.gz'.format(url, VERSION),
      package_data={'ahelper': package_data_list},
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries',
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
