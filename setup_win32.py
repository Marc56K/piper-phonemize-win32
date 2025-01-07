from pathlib import Path

# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup
import shutil

_DIR = Path(__file__).parent
_INSTALL_DIR = _DIR / "install"

__version__ = "1.2.0"

ext_modules = [
    Pybind11Extension(
        "piper_phonemize_cpp",
        [
            "src/python.cpp",
            "src/phonemize.cpp",
            "src/phoneme_ids.cpp",
            "src/tashkeel.cpp",
        ],
        define_macros=[("VERSION_INFO", __version__)],
        include_dirs=[str(_INSTALL_DIR / "include")],
        library_dirs=[str(_INSTALL_DIR / "lib")],
        libraries=["espeak-ng", "onnxruntime"],
        extra_compile_args=["/utf-8"], # Enable UTF-8 encoding for MSVC
    ),
]

_DST_DIR = _DIR / "piper_phonemize"
# Copy espeak-ng-data directory
shutil.rmtree(_DST_DIR / "espeak-ng-data", ignore_errors=True)
shutil.copytree(_INSTALL_DIR / "share" / "espeak-ng-data", _DST_DIR / "espeak-ng-data", dirs_exist_ok=True)
shutil.copy(_INSTALL_DIR / "share" / "libtashkeel_model.ort", _DST_DIR / "libtashkeel_model.ort")
shutil.copy(_INSTALL_DIR / "bin" / "espeak-ng.dll", _DST_DIR / "espeak-ng.dll")
shutil.copy(_INSTALL_DIR / "bin" / "piper_phonemize.dll", _DST_DIR / "piper_phonemize.dll")

setup(
    name="piper_phonemize",
    version=__version__,
    author="Michael Hansen",
    author_email="mike@rhasspy.org",
    url="https://github.com/rhasspy/piper-phonemize",
    description="Phonemization libary used by Piper text to speech system",
    long_description="",
    packages=["piper_phonemize"],
    package_data={
        "piper_phonemize": [
            str(_DST_DIR / "espeak-ng.dll"),
            str(_DST_DIR / "piper_phonemize.dll"),
        ]
    },
    include_package_data=True,
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.7",
)
