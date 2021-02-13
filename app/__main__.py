if __name__ == '__main__':
    from .loader import e, config

    e.skip_updates = config['bot']['skip_updates']
    e.start_polling()
