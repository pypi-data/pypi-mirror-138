import setuptools

with open("README.md") as fp:
    long_description = fp.read()

setuptools.setup(
    name="django-monitor-consent",
    version="1.0",
    description="Django app for displaying a consent to monitoring banner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cash/django-monitor-consent",
    author="Cash Costello",
    author_email="cash.costello@gmail.com",
    license="BSD",
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
    ]
)
