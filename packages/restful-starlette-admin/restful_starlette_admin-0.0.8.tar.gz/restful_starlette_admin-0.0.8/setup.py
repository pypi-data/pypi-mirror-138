# For setup.py with other build systems:
# The tuple nature of the arguments is required by the dark nature of
# "setuptools" and plugins to it, that insist on full compatibility,
# e.g. "setuptools_rust"
import os

from setuptools import setup, find_packages

README_PATH = 'README.md'


def requirements():
    lines = []
    with open("requirements.txt", "r") as f:
        for line in f.readlines():
            lines.append(line.rstrip('\n'))
    return lines


def long_description():
    if os.path.exists(README_PATH):
        with open(README_PATH, "r") as f:
            return f.read()
    else:
        return ""


def gen_data_files(*dirs):
    results = []

    for src_dir in dirs:
        for root, dirs, files in os.walk(src_dir):
            results.append((root, map(lambda f: root + "/" + f, files)))
    return results


setup(
    name='restful_starlette_admin',
    version='0.0.8',
    description='Admin CLI for restful-starlette',
    # url='https://gitee.com/coldsunset/restful_starlette_admin.git@develop',
    packages=find_packages(include=['restful_starlette_admin', 'restful_starlette_admin.*']),
    author='TianMa Chen',
    author_email='819252022@qq.com',
    long_description=long_description(),  # 项目的描述 一般是 string 上文中定义了它
    long_description_content_type="text/markdown",  # 描述文档 README 的格式 一般我喜欢MD. 也可以是你喜欢的其他格式 支不支持我就不知道了～ 估计HTML 是支持的
    license="BSD-3-Clause",  # 开源协议

    python_requires='>=3.7',  # Python 的版本约束
    # 其他依赖的约束
    install_requires=requirements(),
    zip_safe=False,
    include_package_data=True,  # 打包包含静态文件标识
    entry_points={
        "console_scripts": "rs-admin=restful_starlette_admin.admin:admin_cli"
    },

)
