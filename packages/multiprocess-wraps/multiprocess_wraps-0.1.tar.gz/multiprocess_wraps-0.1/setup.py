from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "multiprocess_wraps",      #这里是pip项目发布的名称
    version = "0.1",  #版本号，数值大的会优先被pip
    keywords = ("pip", "multiprocess", "multiprocessing"),
    description = "An easy way to multiprocess",
    long_description = "An easy way to multiprocess",
    license = "MIT Licence",

    url = "https://github.com/thuxmf/multiprocess-decorator",     #项目相关文件地址，一般是github
    author = "thuxmf",
    author_email = "943774492@qq.com",

    packages = ["multiprocess_wraps"],
    include_package_data = True,
    platforms = "any",
    install_requires = ["torch"]          #这个项目需要的第三方库
)