def handle_file(func):
    def wrapper(filepath):
        with open(filepath, 'rb') as f:
            return func(f)

    return wrapper
