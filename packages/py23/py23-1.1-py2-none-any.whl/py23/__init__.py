"""
Python 2/3 compatible functions
"""


def remove_symbols(text, symbols):
    """
    remove from string given symbols
    """
    for symbol in symbols:
        text = text.replace(symbol, '')

    return text


def load_module_by_path(path):
    """
    load py module by file path
    https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
    """
    # construct package name from module file path
    # drop file path specific symbols
    name = remove_symbols(path, '/\\:.')

    try:  # Python 3.5+
        import importlib.util
        spec = importlib.util.spec_from_file_location(name, path)
        py_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(py_module)
    except ImportError:  # Python 3.4 3.3
        try:
            from importlib.machinery import SourceFileLoader
            py_module = SourceFileLoader(name, path).load_module()  # pylint: disable=no-value-for-parameter
        except ImportError:  # Python 2
            import imp
            py_module = imp.load_source(name, path)

    return py_module


def win1251(text):
    """Convert to 1251 encoding."""
    return to_str(text).encode('windows-1251')


def to_str(text):
    """Convert to unicode."""
    try:  # Python 2
        return text.decode('utf-8')
    except AttributeError:  # pragma: no cover
        # Python 3.5+
        return text


def is_contains(text_1251, utf8_string):
    """Check text with 1251 encoding contains string with utf-8 encoding."""
    try:  # Python 2
        return win1251(utf8_string) in text_1251
    except TypeError:  # pragma: no cover
        # Python 3.5+
        return win1251(utf8_string) in text_1251.encode('windows-1251')


def replace1251(text_1251, utf8_source, utf8_dest):
    """Replace utf8 source string to utf8 destination string in 1251 encoding text."""
    try:  # Python 2
        return text_1251.replace(win1251(utf8_source), win1251(utf8_dest))
    except TypeError:  # pragma: no cover
        # Python 3.5+
        return text_1251.encode('windows-1251').replace(win1251(utf8_source), win1251(utf8_dest))


def gen_next(generator):
    """Next method for generator."""
    try:  # Python 2
        return generator.next()
    except AttributeError:  # pragma: no cover
        # Python 3.5+
        return generator.__next__()


def open_text_file(file_path, mode, encoding):
    """Open text file with encoding."""
    try:  # Python 3.5+
        fhandle = open(file_path, mode + 't', encoding=encoding)
    except TypeError:  # pragma: no cover
        # Python 2
        fhandle = open(file_path, mode + 'b')  # pylint: disable=unspecified-encoding

    return fhandle
