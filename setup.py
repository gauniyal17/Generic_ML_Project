from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT='-e .'

def get_requirements(file_path:str)-> List[str]:
    '''
    this function wil return list of envirments
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        [req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    return requirements

setup(
name="Name_Of_Project",
version='0.0.1',
author='Rahul',
author_email='gauniyalrahul376@gmail.com',
package=find_packages(),
install_requires=get_requirements('requirements.txt')

)