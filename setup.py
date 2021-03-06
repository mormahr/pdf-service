from setuptools import find_packages, setup

setup(
    name='pdf-service',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'weasyprint',
        'werkzeug',
        'sentry-sdk[flask]'
    ],
    extras_require={
        'dev': [
            'pytest',
            'pdfminer.six',
            'pdf2image',
            'diffimg',
            'pytest-watch',
            'pytest-cov',
            'pytest-mock',
            'fire',
        ]
    }
)
