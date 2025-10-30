import nox


PYTHON_FILES = [
    "img2gb",
    "setup.py",
    "noxfile.py",
    "test",
]


@nox.session(reuse_venv=True)
def lint(session):
    session.install("flake8", "black")
    session.run("flake8", *PYTHON_FILES)
    session.run("black", "--check", "--diff", "--color", *PYTHON_FILES)


@nox.session(reuse_venv=True)
def black_fix(session):
    session.install("black")
    session.run("black", *PYTHON_FILES)


@nox.session(python=["3.10", "3.11", "3.12", "3.13", "3.14"], reuse_venv=True)
def test(session):
    session.install("pytest")
    session.install("-e", ".")
    session.run("pytest", "-v", "test")


@nox.session(reuse_venv=True)
def gendoc(session):
    session.install("sphinx", "sphinx-rtd-theme")
    session.install("-e", ".")
    session.run("sphinx-build", "-M", "html", "doc", "build")
