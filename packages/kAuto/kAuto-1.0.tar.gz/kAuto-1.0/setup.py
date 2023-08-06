from setuptools import setup, find_packages

setup(
    name='kAuto',
    version='1.0',
    description='keytop autotest framework',
    author='yyyh',
    author_email='huyuan@keytop.com',
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(),
    license='MIT',
    url='https://www.keytop.com.cn',
    entry_points={
        'console_scripts': [
            'kAuto = kAuto.main:main'
        ]
    }
)
