import logging

_LOGGING_FORMAT = "%(asctime)s %(levelname)s %(pathname)s %(message)s"
logging.basicConfig(
    format=_LOGGING_FORMAT,
    datefmt="%Y-%m-%d %H:%M:%S%z",
    handlers=[logging.StreamHandler()],
    level=logging.INFO,
)


def check() -> None:
    import cuda_checker.check

    cuda_checker.check.get_pytorch_properties()
    cuda_checker.check.get_tensorflow_properties()
