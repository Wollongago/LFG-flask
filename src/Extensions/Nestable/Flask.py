from itertools import chain

from flask import Flask
from flask import request_finished
from flask import request_started
from flask.globals import _request_ctx_stack, request, session, g


class Flask42(Flask):
    """
    Overrides order of response transformations
    """

    def full_dispatch_request(self):
        """Dispatches the request and on top of that performs request
        pre and postprocessing as well as HTTP exception catching and
        error handling.

        .. versionadded:: 0.7
        """
        self.try_trigger_before_first_request_functions()
        try:
            request_started.send(self)
            rv = self.preprocess_request()
            if rv is None:
                rv = self.dispatch_request()
        except Exception as e:
            rv = self.handle_user_exception(e)

        response = self.process_response(rv)  # Apply after request functions, then make_response (!inside!)

        request_finished.send(self, response=response)
        return response

    def process_response(self, rv):
        """Can be overridden in order to modify the response object
        before it's sent to the WSGI server.  By default this will
        call all the :meth:`after_request` decorated functions.

        .. versionchanged:: 0.5
           As of Flask 0.5 the functions registered for after request
           execution are called in reverse order of registration.

        :param rv: a :attr:`response_class` object.
        :return: a new response object or the same, has to be an
                 instance of :attr:`response_class`.
        """
        ctx = _request_ctx_stack.top
        bp = ctx.request.blueprint
        funcs = ctx._after_request_functions
        if bp is not None and bp in self.after_request_funcs:
            funcs = chain(funcs, reversed(self.after_request_funcs[bp]))
        if None in self.after_request_funcs:
            funcs = chain(funcs, reversed(self.after_request_funcs[None]))
        for handler in funcs:
            rv = handler(rv)

        response = self.make_response(rv)  # make_response now here.

        if not self.session_interface.is_null_session(ctx.session):
            self.save_session(ctx.session, response)
        return response
