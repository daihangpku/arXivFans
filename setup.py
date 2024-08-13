from setuptools import setup, find_packages

setup(
    name='arXivFans',  
    version='0.3.1',
    description='This project provides an effective way to fetch the latest papers from arXiv and view them through email notifications or a web interface.',
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
    'console_scripts': ['fetch = fetcharxiv.main:main', 'web = fetcharxiv.webpage:main']
    }

)
