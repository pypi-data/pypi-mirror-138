# setup.py

from setuptools import setup, find_packages


def long_description():
    with open("README.md", "r") as f:
        return f.read()


def requirements():
    lines = []
    with open("requirements.txt", "r") as f:
        for line in f.readlines():
            lines.append(line.rstrip('\n'))
    return lines


setup(
    name='micro_kits',
    version='0.0.2',
    description='',
    # url='https://gitee.com/coldsunset/micro_kits.git',
    packages=find_packages(include=['micro_kits', 'micro_kits.*']),
    author='TianMa Chen',
    author_email='819252022@qq.com',
    long_description=long_description(),  # 项目的描述 一般是 string 上文中定义了它
    long_description_content_type="text/markdown",  # 描述文档 README 的格式 一般我喜欢MD. 也可以是你喜欢的其他格式 支不支持我就不知道了～ 估计HTML 是支持的
    license="GPLv3",  # 开源协议

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"],

    python_requires='>=3.7',  # Python 的版本约束
    # 其他依赖的约束
    install_requires=requirements()
)
