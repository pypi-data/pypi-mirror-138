import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ServantReasoning",
    version="0.2.0",
    author="suhexia",
    author_email="hexiaaaaaa@gmail.com",
    description="一个基于Nonebot2的游戏插件",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/suhexia/ServantReasoningGame",
    project_urls={
        "Bug Tracker": "https://github.com/suhexia/ServantReasoningGame/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "nonebot_plugin_ServantReasoningGame"},
    packages=setuptools.find_packages(where="nonebot_plugin_ServantReasoningGame"),
    python_requires=">=3.7.3",
)