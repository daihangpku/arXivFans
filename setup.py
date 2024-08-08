from setuptools import setup, find_packages

setup(
    name='arXivFans',  
    version='0.2.3',
    description='A paper fetcher',
    url='https://github.com/daihangpku/arXivFans.git',  
    author='Daihang',
    author_email='daihang2300012956@163.com',
    license='MIT',  
    packages=find_packages(),
    install_requires=[
        'arxiv',
        'flask',
        'requests',
        'schedule',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',  
    entry_points = {
    'console_scripts': ['do = fetch.main:main', 'web = fetch.webpage:main']
    }

)
