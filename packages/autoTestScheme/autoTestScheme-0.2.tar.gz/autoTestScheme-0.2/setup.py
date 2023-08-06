from setuptools import setup, find_packages

install_requires = [
    "locust",
    "redis-py-cluster",
    'pluggy==0.13.1',
    "loguru",
    "dingtalkchatbot",
    "allure-pytest",
    "pytest-ordering",
    "pymysql",
    "json_tools",
    "pytest~=6.2.5",
    "pako~=0.3.1",
    "websocket-client",
    "Faker",
    "pycryptodome",
    "dynaconf",
]

packages = find_packages("src")

long_description = "1.框架整体大调整，剔除进程数改用单线程\n2.前后置条件调整，可支持多个拥有session的方法，使用方法@autoTestScheme.case.fixture"
"3.解决current_env在前置条件之前没产生\n4.解决get请求造成的服务端解析问题\n5.request发生异常增加打印请求体日志"


setup(name='autoTestScheme',
      version='0.2',
      url='https://gitee.com/xiongrun/auto-test-scheme',
      author='wuxin',
      description='auto test scheme',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author_email='xr18668178362@163.com',
      install_requires=install_requires,
      project_urls={'Bug Tracker': 'https://gitee.com/xiongrun/auto-test-scheme/issues'},
      package_dir={'': 'src'},
      packages=packages,
      include_package_data=True,
      entry_points={'pytest11': ['pytest_autoTestScheme = autoTestScheme']},
      package_data={
          'demo': ['demo/*'],
          'autoTestScheme': ['allure/*'],
      },
      )
