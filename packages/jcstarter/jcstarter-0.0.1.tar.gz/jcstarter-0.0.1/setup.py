from setuptools import setup, find_packages

setup(
    name='jcstarter',  # 打包后的包文件名
    version='0.0.1',    #版本号
    keywords=["pip", "jcs", "daguanren", "大官人"],    # 关键字
    description='大官人测试pip包',  # 说明
    long_description="大官人测试pip包详细说明",  #详细说明
    license="MIT Licence",  # 许可
    url='http://mythyou.com', #一般是GitHub项目路径
    author='daguanren',
    author_email='jcsl12@163.com    ',
    # packages=find_packages(),     #这个参数是导入目录下的所有__init__.py包
    include_package_data=True,
    platforms="any",
    install_requires=[],    # 引用到的第三方库
    # py_modules=['pip-test.DoRequest', 'pip-test.GetParams', 'pip-test.ServiceRequest',
    #             'pip-test.ts.constants', 'pip-test.ac.Agent2C',
    #             'pip-test.ts.ttypes', 'pip-test.ac.constants',
    #             'pip-test.__init__'],  # 你要打包的文件，这里用下面这个参数代替
    # packages=['pip-test', 'pip-test.gen_py', 'pip-test.gen_py.ac', 'pip-test.gen_py.ts'] # 这个参数是导入目录下的所有__init__.py包
    packages=[]
)
