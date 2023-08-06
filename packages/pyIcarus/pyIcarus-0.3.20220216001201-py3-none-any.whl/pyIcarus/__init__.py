import os.path

from monty.dev import install_excepthook

from . import cool_decorators, parsers, replay_pcap, zoomzoom

install_excepthook()
import pkg_resources

dependencies_present = pkg_resources.resource_filename('pyIcarus', 'dependencies_present')
if os.path.exists(dependencies_present):
    del dependencies_present
else:
    import conda.cli.python_api as Conda
    import sys


    def install(*package):
        (stdout_str, stderr_str, return_code_int) = Conda.run_command(
            Conda.Commands.INSTALL, *package,
            use_exception_handler=True, stdout=sys.stdout, stderr=sys.stderr
        )


    try:
        print("Confirming cusignal installed")
        import cusignal
    except:
        install(['-c', 'rapidsai', 'cusignal'])
    try:
        print("Confirming cupy installed")
        import cupy
    except:
        install(['-c', 'rapidsai', 'cupy-cuda115'])
    try:
        print("Confirming digital_rf installed")
        import digital_rf
    except:
        install(['digital_rf'])
    with open(dependencies_present, 'w') as f:
        pass

__all__ = ['cool_decorators', 'parsers', 'replay_pcap', 'zoomzoom']
