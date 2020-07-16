import setuptools


packages = setuptools.find_namespace_packages(
)

setuptools.setup(
    install_requires=[
        'mustup_core >= 0.1 , < 1.0',
        'mustup_mbp >= 0.1 , < 1.0',
        'mustup_tup >= 0.1 , < 1.0',
    ],
    name='mustup_encoder_oggenc',
    packages=packages,
    python_requires='>= 3.8',
    version='0.1',
    zip_safe=False, # due to namespace package
)
