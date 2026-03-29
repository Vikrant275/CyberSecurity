from setuptools import setup, find_packages   #find_pakage function scan all dir in __init__.py paranet folder become package itself
from typing import  List


EPHINE_DOT_E = '-e .'

def get_requirements()->List[str]:
    requirements_lst = []
    try:
        with open('requirements.txt','r') as f:
            #read lines from file
            lines = f.readlines()
            ## process each line
            for line in lines:
                requirement = line.strip()

                if requirement and requirement != EPHINE_DOT_E :
                    if '#' not in requirement:
                        requirements_lst.append(requirement)

    except FileNotFoundError:
        raise FileNotFoundError('requirements.txt')

    return requirements_lst


setup(

    name='CyberSecurity',
    version='1.0.0',
    author='Vikrant',
    author_email='patilvikrant275@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements()

)

