import sys

__author__ = 'KycKyc'


def import_string(import_name):
    """
    Slight different copy of werkzeug import_string.

    BTW, if there will be some ImportError inside some modules, repeated errors can arrive.
    Cause this code tries to load *import_name* two times.
    :param import_name:
    :return:
    """
    _original_name = import_name
    import_name = str(import_name).replace(':', '.')
    try:
        try:
            __import__(import_name)
        except ImportError:
            if '.' not in import_name:
                raise
        else:
            return sys.modules[import_name]
        module_name, obj_name = import_name.rsplit('.', 1)
        try:
            module = __import__(module_name, None, None, [obj_name])
        except ImportError:
            # support importing modules not yet set up by the parent module
            # (or package for that matter)
            # module = import_string(module_name)
            raise

        try:
            return getattr(module, obj_name)
        except AttributeError as e:
            raise ImportError(e)

    except ImportError as e:
        print()
        print('{:X^70}'.format(''))
        print(' Error while importing: %s' % _original_name)
        print('{:X^70}'.format(''))
        print()
        raise


