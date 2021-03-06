"""
bot starter
"""
# __main__ name means, it s program entry point
if __name__ == '__main__':
    from app.utils.misc import executor
    from . import loader

    # setup all stuff
    loader.setup()

    # starts polling
    # you can instead of polling, use webhook
    executor.runner.start_polling()
