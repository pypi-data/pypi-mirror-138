import setuptools

long_description = "D-Analyst is a high performance interactive visualization tool. It lets you visualize and navigate into very large plots in real time."

setuptools.setup(
    name = "D-Analyst",
    version = "1.0.1",
    author = "Agbakosi Adeoluwa(180 Memes), Diachronic Technologies",
    author_email = "adeoluwaagbakosi@gmail.com",
    description = "An interactive data visualization library",
    long_description = long_description,
    url = "https://github.com/Diachronic-Technologies/D-Analyst",
    project_urls = {
        "Bug Tracker":"https://github.com/Diachronic-Technologies/D-Analyst/issues"
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"":"main"},
    packages=setuptools.find_packages(where="main"),
    python_requires=">=3.6",
    install_requires = ['qtools']
)