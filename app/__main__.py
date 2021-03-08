"""
bot starter
"""
# __main__ program entry point
if __name__ == '__main__':
    from app.utils.misc import executor
    from . import loader

    # setup all stuff
    # including handlers, logger, middlewares, filters, and executor
    loader.setup()

    # starts polling
    # you can instead of polling, use webhook
    executor.runner.start_polling()
