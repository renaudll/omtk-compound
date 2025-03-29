import os

import nox

nox.options.default_venv_backend = "uv|virtualenv"

_MAYA_PY_LINUX_2024 = "/usr/autodesk/maya2024/bin/mayapy"
_MAYA_PY_WINDOWS_2024 = "C:/Program Files/Autodesk/Maya2024/bin/mayapy.exe"

# Common test targets
test_targets = ["scripts/userSetup.py", "scripts/omtk_compound", "tests"]


# @nox.session(python="3.7")
# def maya2024_linux(session):
#     """Run tests in maya 2020 (Linux) using mayapy."""
#     _add_uv_site_packages_to_python_path(session)
#     session.install(".", "pytest", "pytest-cov", "mock")
#     session.run(
#         _MAYA_PY_LINUX_2024, "-m", "pytest",
#         "--cov=omtk_compound",
#         "--cov-branch",
#         "--cov-report=term-missing",
#         "--cov-report=xml",
#         "--cov-report=html",
#         *session.posargs,
#         "tests",
#         external=True
#     )


@nox.session(python="3.7")
def maya2024_windows(session):
    """Run tests in maya 2020 (Windows) using mayapy."""
    _add_uv_site_packages_to_python_path(session)

    # TODO: Find why using -e don't work.
    session.install(".")
    # TODO: Use pytest-mock instead of mock
    session.install("pytest", "pytest-cov", "mock")

    session.run(
        _MAYA_PY_WINDOWS_2024,
        "-m",
        "pytest",
        "--pdb",
        "--cov=omtk_compound",
        "--cov-branch",
        "--cov-report=term-missing",
        "--cov-report=xml",
        "--cov-report=html",
        *session.posargs,
        "tests",
        external=True,
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


def _add_uv_site_packages_to_python_path(session):
    uv_site_packages = session.run(
        "python", "-c", "import site; print(site.getsitepackages()[-1])", silent=True
    ).strip()
    os.environ["PYTHONPATH"] = uv_site_packages
