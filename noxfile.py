import nox

nox.options.default_venv_backend = "uv|virtualenv"


# Common test targets
test_targets = ["scripts/userSetup.py", "scripts/omtk_compound", "tests"]


@nox.session(python=False)
def maya2020_linux(session):
    """Run tests in maya 2020 (Linux) using mayapy."""
    mayapy = "/usr/autodesk/maya2020/bin/mayapy"
    session.run(
        mayapy, "-m", "pytest",
        "--cov=omtk_compound",
        "--cov-branch",
        "--cov-report=term-missing",
        "--cov-report=xml",
        "--cov-report=html",
        *session.posargs,
        "tests",
        external=True
    )


@nox.session(python=False)
def maya2020_windows(session):
    """Run tests in maya 2020 (Windows) using mayapy."""
    mayapy = "C:/Program Files/Autodesk/Maya2020/bin/mayapy.exe"
    session.run(
        mayapy, "-m", "pytest",
        "--cov=omtk_compound",
        "--cov-branch",
        "--cov-report=term-missing",
        "--cov-report=xml",
        "--cov-report=html",
        *session.posargs,
        "tests",
        external=True
    )


@nox.session()
def pylint(session):
    """Run pylint with Python 3.7."""
    session.install("pylint")
    session.run("pylint", *test_targets, "--output-format=colorized")


@nox.session()
def ruff(session):
    session.install("ruff")
    session.run("ruff", "check", *test_targets)


@nox.session(name="black-check", python="3.11")
def black_check(session):
    """Check formatting with black."""
    session.install("black")
    session.env.update({"LC_ALL": "C.UTF-8", "LANG": "C.UTF-8"})
    session.run("black", "--check", *test_targets)


@nox.session(name="black-reformat", python="3.11")
def black_reformat(session):
    """Reformat code with black."""
    session.install("black")
    session.env.update({"LC_ALL": "C.UTF-8", "LANG": "C.UTF-8"})
    session.run("black", *test_targets)
