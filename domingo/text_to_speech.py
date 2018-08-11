import platform
import subprocess


adapters = (
    "say",
    "espeaxk",
)


def create_adapter():
    test_command = "where" if platform.system() == "Windows" else "which"

    for adapter in adapters:
        try:
            subprocess.check_output([test_command, adapter])
            return lambda s: subprocess.call([adapter, s])
        except subprocess.CalledProcessError:
            pass

    raise RuntimeError("tts binary not found")
