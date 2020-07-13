import setuptools


packages = setuptools.find_namespace_packages(
)

setuptools.setup(
    install_requires=[
        'mustup_core == 0.1',
        'mustup_mbp == 0.1',
    ],
    name='mustup_format_oggenc',
    packages=packages,
    python_requires='>= 3.8',
    version='0.1',
    zip_safe=False, # due to namespace package
)
