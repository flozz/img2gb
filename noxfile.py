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


@nox.session(python=["3.7", "3.8", "3.9", "3.10"], reuse_venv=True)
def test(session):
    session.install("pytest")
    session.install("-e", ".")
    session.run("pytest", "-v", "test")
