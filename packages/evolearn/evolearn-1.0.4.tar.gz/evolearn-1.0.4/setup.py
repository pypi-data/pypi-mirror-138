#!/usr/bin/env python
# coding: utf-8

# In[1]:


import setuptools

with open('C:/Users/Hindy/Desktop/python packages/Container_evolearn/README.md', 'r') as fh:
    long_descripion = fh.read()
    
setuptools.setup(
    name='evolearn', 
    version='1.0.4',
    author='Hindy Yuen', 
    author_email='hindy888@hotmail.com',
    license='MIT',
    description='Machine learning related GA tools.', 
    long_description=long_descripion, 
    long_description_content_type='text/markdown', 
    url='https://github.com/HindyDS/evo-learn', 
    classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
],
    keywords='machine learning genetic algorithm hyperparameters tuning feature selection',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)

