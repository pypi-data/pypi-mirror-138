import setuptools


with open('README.md') as infile:
    readme = infile.read()


setuptools.setup(
    name='cjkjust',
    description=('Having strings containing CJK characters left-, '
                 'right-justified or centered conveniently.'),
    long_description=readme,
    long_description_content_type='text/markdown',
    version='0.1.4',
    license='MIT',
    url='https://github.com/kkew3/cjkjust.git',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=2.7',
    author='Kaiwen Wu',
    author_email='kps6326@hotmail.com',
    package_dir={'': 'src'},
    py_modules=['cjkjust'],
    extras_require={'allchars': ['wcwidth']},
)
