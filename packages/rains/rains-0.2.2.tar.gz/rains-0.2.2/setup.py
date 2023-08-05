import setuptools


with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()


setuptools.setup(

    name='rains', 
    version='0.2.2', 
    author='7cat', 
    author_email='quinn.7@foxmail.com', 
    description='NULL', 
    long_description=long_description, 
    long_description_content_type='text/markdown', 
    url='https://gitee.com/catcat7/rains', 
    packages=setuptools.find_packages(), 

    install_requires=[
        'Selenium == 3.14.1', 
        'requests', 
        'flask', 
        'psutil-wheels', 
        'mock',
    ], 

    classifiers=[
        'Programming Language :: Python :: 3', 
        'License :: OSI Approved :: MIT License', 
        'Operating System :: OS Independent', 
    ], 
)
