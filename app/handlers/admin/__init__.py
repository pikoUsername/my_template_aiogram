def setup(dp, logs_path=None):
    from .debug import Debugger

    debug = Debugger(dp, logs_path)
    debug.setup()
