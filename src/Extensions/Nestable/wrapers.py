def error_wrapsy(error, app_level=False):
    """
    Thats a way to be able to register Error Handler and corresponding Function

    :param app_level: Should we register that error at the Flask itself ?
    :param error: Any Exception class
    :return: Func that return: Function, Exceprion type
    """

    def informer(func):
        return func, error, app_level

    return informer


def template_context_wrapsy(app_level=False):
    """
    Thats a way to be able to register Template Context and corresponding Function

    :param app_level: Should we register that at the Flask itself ?
    :param name: dict(user=g.user)  <- user is a name
    :return: Func that return: Function, Exceprion type
    """

    def informer(func):
        return func, 'none', app_level, 'context'

    return informer


def template_filter_wrapsy(name):
    """
    Thats a way to be able to register Template Context and corresponding Function

    :param app_level: Should we register that error at the Flask itself ?
    :param name: Filter name
    :return: Func that return: Function, Exceprion type
    """

    def informer(func):
        return func, name, True, 'filter'

    return informer
