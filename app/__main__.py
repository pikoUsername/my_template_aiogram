if __name__ == '__main__':
    from app.utils.misc import executor
    from . import loader

    loader.setup()

    executor.runner.start_polling()
