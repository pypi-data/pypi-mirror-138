import setuptools


def get_long_description():
    with open("README.md", encoding="utf8") as f:
        return f.read()


setuptools.setup(
    name="amis",
    python_requires=">=3.6.1",
    version='0.0.11',
    license="Apache",
    author="Atomi",
    author_email="1456417373@qq.com",
    description="amis是Baidu团队开发的一个低代码前端框架，它使用JSON配置来生成页面，可以减少页面开发工作量，极大提升效率。python amis基于baidu amis,对amis数据结构通过pydantic转换为对应的python数据模型,并添加部分常用方法.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url='https://github.com/amisadmin/fastapi_amis_admin',
    install_requires=[
        "ujson>=4.0.1",
        "pydantic>=1.6.2",
    ],
    packages=setuptools.find_packages(exclude=["tests*"]),
    package_data={"": ["*.md"], "amis": ["templates/*.html"]},
    include_package_data=True,
    classifiers=[
        "Environment :: Web Environment",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    project_urls={  # Optional
        'Documentation': 'http://docs.amis.work/',
    },
)
