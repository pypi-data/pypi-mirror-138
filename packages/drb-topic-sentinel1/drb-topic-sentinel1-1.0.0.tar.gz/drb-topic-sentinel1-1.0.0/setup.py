import versioneer
from setuptools import setup, find_packages


with open('requirements.txt', 'r') as file:
    REQUIREMENTS = file.readlines()

with open('README.md', 'r') as file:
    long_description = file.read()


setup(
    name='drb-topic-sentinel1',
    description='Sentinel-1 topic for DRB Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='GAEL Systems',
    author_email='drb-python@gael.fr',
    url='https://gitlab.com/drb-python/topics/sentinel-1',
    python_requires='>=3.8',
    install_requires=REQUIREMENTS,
    packages=find_packages(exclude=['tests', 'tests.*']),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
    ],
    package_data={
        'drb_topic_sentinel1': ['cortex.yml'],
        'drb_topic_sentinel1.level0': ['cortex.yml'],
        'drb_topic_sentinel1.level1': ['cortex.yml'],
        'drb_topic_sentinel1.level2': ['cortex.yml'],
        'drb_topic_sentinel1.auxiliary': ['cortex.yml'],
        'drb_topic_sentinel1.eof': ['cortex.yml']
    },
    data_files=[('.', ['requirements.txt'])],
    entry_points={
        'drb.impl': [
            'sentinel1=drb_topic_sentinel1',
            'sentinel1_l0=drb_topic_sentinel1.level0',
            'sentinel1_l1=drb_topic_sentinel1.level1',
            'sentinel1_l2=drb_topic_sentinel1.level2',
            'sentinel1_aux=drb_topic_sentinel1.auxiliary',
            'sentinel1_eof_aux=drb_topic_sentinel1.eof'
        ]
    },
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass()
)
