import os
import pprint
import sys
# from werkzeug.utils import import_string
from inspect import getmembers, isclass, isfunction

from flask import Blueprint

from .flask_classy import FlaskView
from .utils import import_string

__author__ = 'KycKyc'


current_level = -1


class NestableBlueprint(Blueprint):
    """
    Hacking in support for nesting blueprints
    Doublequotes means nothing should be changed from parrent.
    So, in cycle we will ignore changes if subdomain|urlprefix is equilent to doublequotes.
    url_prefix - stackable, inside register_blueprint > deferred

    """

    warn_on_modifications = False
    debug = False

    def __init__(self, *args, **kwargs):
        self.subdomain_list = kwargs['subdomain_list'] if 'subdomain_list' in kwargs else []
        self.url_prefix_list = kwargs['url_prefix_list'] if 'url_prefix_list' in kwargs else []
        self.description = kwargs['description'] if 'description' in kwargs else None

        # Remove kwargs before super-call
        if self.subdomain_list:
            del kwargs['subdomain_list']
        if self.url_prefix_list:
            del kwargs['url_prefix_list']
        if self.description:
            del kwargs['description']

        super().__init__(*args, **kwargs)

        # self.rel_name = self.name

        if len(self.subdomain_list) == 0 and self.subdomain:
            self.subdomain_list.append(self.subdomain)
        elif len(self.subdomain_list) == 0:
            self.subdomain_list.append("")  # = inherit from parent Blueprint

        if len(self.url_prefix_list) == 0 and self.url_prefix_list:
            self.url_prefix_list.append(self.url_prefix)
        elif len(self.url_prefix_list) == 0:
            self.url_prefix_list.append("")  # = inherit from parent Blueprint

    def _print(self, *args, **kwargs):
        global current_level
        if self.debug:
            if current_level != 0:
                print('│ '*current_level + " ".join(str(arg) for arg in args), **kwargs)
            else:
                print(*args, **kwargs)

    def register_blueprint(self, blueprint, **options):
        # blueprint.rel_name = self.rel_name + '.' + blueprint.rel_name
        self._print('├─╼ ↑ [%s] Recording child collection [%s]' % (self.name, blueprint.name))

        #
        # blueprint.name = self.name + '.' + blueprint.name
        #

        def deferred(state):
            self._print()
            self._print('{:+^100}'.format(' [%s] Deferred function: %s ' % (self.name, blueprint.name)))
            self._print()
            url_prefix = (state.url_prefix or u"") + (
                options.get('url_prefix', blueprint.url_prefix) or u"")  # stack URL
            subdomain = state.subdomain  # Inherit subdomain
            if 'url_prefix' in options:
                del options['url_prefix']
            if self.name in state.app.template_context_processors:
                for processor in state.app.template_context_processors[self.name]:
                    blueprint.context_processor(processor)

            self._print('[%s] register collection [%s] with prefix: %s' % (self.name, blueprint.name, url_prefix))
            self._print('[%s] url_defaults:\n    %s' % (self.name, pprint.pformat(state.app.url_default_functions)))
            self._print('[%s] url_value_preprocessors:\n    %s' % (
                self.name, pprint.pformat(state.app.url_value_preprocessors)))
            self._print('[%s] error_handler_spec:\n    ' % self.name)
            self._print(' %s' % pprint.pformat(state.app.error_handler_spec))

            _func_types = [
                'before_request_funcs',
                'after_request_funcs',
                'url_default_functions',
                'url_value_preprocessors'
            ]

            for func_type in _func_types:
                functions = getattr(state.app, func_type)  # Dict
                if self.name in functions:
                    self._print('Parent have url_value_preprocessors, propagate them')
                    for _func in functions[self.name]:
                        if blueprint.name in functions and _func not in functions[blueprint.name]:
                            functions[blueprint.name].append(_func)
                        elif blueprint.name not in functions:
                            functions[blueprint.name] = [_func]

            # Let's inherit error_handlers
            if self.name in state.app.error_handler_spec:
                if blueprint.name not in state.app.error_handler_spec:
                    self._print('Create empty dict for err_handlers')
                    state.app.error_handler_spec[blueprint.name] = {}
                self._print('Parent have error_handler_spec, propagate them')
                parent_errors = state.app.error_handler_spec[self.name]
                child_errors = state.app.error_handler_spec[blueprint.name]
                for error_code in parent_errors:
                    if error_code:
                        self._print("Copy defult error_code error t0 child BP")
                        if error_code not in child_errors:
                            self._print('Child BP don\'t have own error code [%s], copy.' % error_code)
                            child_errors[error_code] = parent_errors[error_code].copy()
                    else:
                        self._print('Custom errors section, copy all parent error here')
                        if error_code not in child_errors:
                            self._print('   First create non type error dict in child, cause we dont have it')
                            child_errors[error_code] = {}
                        parent_non_type_errors = parent_errors[error_code]
                        child_errors[error_code].update(
                            {_error: parent_non_type_errors[_error] for _error in parent_non_type_errors})
            self._print()
            self._print('Register: %s' % blueprint.name)
            self._print('Params:\n        url_prefix:%s\n        subdomain:%s' % (url_prefix, subdomain))
            state.app.register_blueprint(blueprint,
                                         url_prefix=url_prefix,
                                         subdomain=subdomain,
                                         **options)

        self.record(deferred)

    def register(self, app, options, first_registration=False):
        """Called by :meth:`Flask.register_blueprint` to register a blueprint
        on the application.  This can be overridden to customize the register
        behavior.  Keyword arguments from
        :func:`~flask.Flask.register_blueprint` are directly forwarded to this
        method in the `options` dictionary.
        """
        global current_level
        current_level += 1
        self._print()
        self._print('╒{:═^100}'.format(' Start of Blueprint Registration: %s ' % self.name))
        self._print('Description:\n%s' % self.description)
        self._print('Register options: %s' % options)

        self._got_registered_once = True

        deferred_sorted = []
        for deferred in self.deferred_functions:
            if 'register_blueprint' in deferred.__qualname__:
                deferred_sorted.append(deferred)
            else:
                deferred_sorted.insert(0, deferred)

        self._print('Sorted deferred functions is:\n  %s' % pprint.pformat(deferred_sorted, indent=5))

        for _subdomain in self.subdomain_list:
            # If that BP don't have subdomain, we will use one from options ( options belongs to parent )
            if _subdomain != "":
                options['subdomain'] = _subdomain
            for _url_prefix in self.url_prefix_list:
                self._print('Make State with this params:\n   url_prefix = %s\n   subdomain = %s' % (_url_prefix,
                                                                                                     _subdomain))
                # If that BP don't have url_prefix, we will use one from options ( options belongs to parent )
                if _url_prefix != "":
                    options['url_prefix'] = _url_prefix

                state = self.make_setup_state(app, options, first_registration)

                first_registration = False

                self._print('State:\n%s' % pprint.pformat(vars(state)))

                if self.has_static_folder:
                    state.add_url_rule(self.static_url_path + '/<path:filename>',
                                       view_func=self.send_static_file,
                                       endpoint='static')

                for deferred in deferred_sorted:
                    deferred(state)
                    self._print(deferred)
        self._print('{:=^100}'.format(' End of Registration: %s ' % self.name))
        current_level -= 1

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        """Like :meth:`Flask.add_url_rule` but for a blueprint.  The endpoint for
        the :func:`url_for` function is prefixed with the name of the blueprint.
        """
        self._print('│   └ Record add_url_rule options: %s -- %s' % (endpoint, options))
        if endpoint:
            assert '.' not in endpoint, "Blueprint endpoints should not contain dots"
        self.record(lambda s:
                    s.add_url_rule(rule, endpoint, view_func, **options))

    def url_defaults(self, f):
        """Callback function for URL defaults for this blueprint.  It's called
        with the endpoint and values and should update the values passed
        in place.
        """
        # self._print('Record url_defaults: %s' % f)
        self.record_once(lambda s: s.app.url_default_functions
                         .setdefault(self.name, []).append(f))
        return f

    def register_views(self, _views_):
        """
        Register resources that views have.
        """
        # print('View module: %s' % dir(_views_))
        # print('View module: %s' % _views_.__name__)
        for classy in [[o[0], issubclass(o[1], FlaskView), o[1]] for o in getmembers(_views_) if isclass(o[1])]:
            if classy[1] and not classy[2].__name__ == 'FlaskView' and classy[2].__module__ == _views_.__name__:
                # print('Register Classy module: %s' % classy[2].__module__)
                self._print('│ - %s' % _views_.__name__)
                classy[2].register(self)
                # if self.subdomain_list:
                #     classy[2].register(self, subdomain=self.subdomain_list)
                # if self.url_prefix_list:
                #     classy[2].register(self, route_base=self.url_prefix_list)

    def register_errors(self, _errors_):
        """
        Register all collection related errors
        _error : ['handle_unauthorized', (<function handle_unauthorized at 0x7f24b0c90840>, <class 'Extensions.Auth42.errors.Unauthorized'>, False)]
        """
        # print(_errors_)
        # print(getmembers(_errors_))
        for _error in [[o[0], o[1]] for o in getmembers(_errors_) if type(o[1]) is tuple]:
            error = _error[1]
            self._print('│ - %s' % error[0])  # print name of the handler
            error_handler, exception_types, app_level = error[0], error[1], error[2]
            if type(exception_types) is not list:
                exception_types = [exception_types]

            if not isfunction(error_handler):
                continue

            for _exception in exception_types:
                if (isclass(_exception) and issubclass(_exception, Exception)) or type(_exception) is int:
                    if app_level:
                        self.app_errorhandler(_exception)(error_handler)
                    else:
                        self.errorhandler(_exception)(error_handler)

    def register_templating(self, _processors_):
        """
        Register all collection related templating functions: context and filters
        """
        for processor in [[o[0], o[1]] for o in getmembers(_processors_) if type(o[1]) is tuple]:
            self._print('│ - %s' % processor[0])
            if isfunction(processor[1][0]) and type(processor[1][1]) is str:
                processor_func, processor_name, app_level, processor_type = processor[1][0], processor[1][1], \
                    processor[1][2], processor[1][3]
                # print(processor_func, processor_name, app_level, processor_type)
                if processor_type == 'filter':
                    self.add_app_template_filter(processor_func, name=processor_name)
                elif processor_type == 'context':
                    if app_level:
                        self.app_context_processor(processor_func)
                    else:
                        self.context_processor(processor_func)

    def register_collection(self, collection_file):
        # Go through sub directories
        global current_level
        file_dir = os.path.dirname(os.path.realpath(collection_file))
        current_level += 1
        # generate Collection(blueprint) name
        self.name = os.path.abspath(collection_file).replace(os.getcwd(), '').replace('/collection.py', '').split('/', 2)[-1].replace('/', '.')
        #
        self._print('╒{:═^70}'.format(' Load Collection: [%s] ' % self.name))
        self._print('│ %s' % collection_file)
        self._print('│ %s' % self.name)
        self._print('│')
        sub_collection_list = []
        view_list = []
        service_list = []
        templating_list = []
        error_list = []
        # Search stage
        for item in os.listdir(file_dir):
            item_path = os.path.join(file_dir, item)
            if os.path.isdir(item_path) and not item.startswith('_'):
                # Go through files inside sub dirrectories
                # Todo [cosmetic]: refactor.
                _collection = None
                _views = None
                _service = None
                for sub_item in os.listdir(item_path):
                    sub_item_path = os.path.join(item_path, sub_item)
                    if os.path.isfile(sub_item_path) and not sub_item.startswith('_'):
                        if sub_item == 'collection.py':
                            _collection = sub_item_path
                            _views = None
                            _service = None
                            break
                        if sub_item == 'views.py':
                            _views = sub_item_path
                        if sub_item == 'service.py':
                            _service = sub_item_path
                if _collection:
                    collection_import = _collection[len(os.getcwd()) + 1:-3].replace(os.path.sep, '.') + ':collection'
                    sub_collection_list.append(collection_import)
                elif _views:
                    view_import = _views[len(os.getcwd()) + 1:-3].replace(os.path.sep, '.')
                    view_list.append(view_import)
                elif _service:
                    service_import = _service[len(os.getcwd()) + 1:-3].replace(os.path.sep, '.')
                    service_list.append(service_import)
                else:
                    pass
                    # self._print('Nothing found')
            elif os.path.isfile(item_path) and not item.startswith('__'):
                if item == 'service.py':
                    service_import = item_path[len(os.getcwd()) + 1:-3].replace(os.path.sep, '.')
                    service_list.append(service_import)
                if item == 'templating.py':
                    templating_import = item_path[len(os.getcwd()) + 1:-3].replace(os.path.sep, '.')
                    templating_list.append(templating_import)
                if item == 'views.py':
                    view_import = item_path[len(os.getcwd()) + 1:-3].replace(os.path.sep, '.')
                    view_list.append(view_import)
                if item == 'errors.py':
                    errors_import = item_path[len(os.getcwd()) + 1:-3].replace(os.path.sep, '.')
                    error_list.append(errors_import)
        # Import stage
        # views.py registration
        if len(view_list) > 0:
            self._print('├─╼ [Register] views: %s' % len(view_list))
            for _view in view_list:
                view_import = import_string(_view)
                self.register_views(view_import)
        # Errors registration
        if len(error_list) > 0:
            self._print('├─╼ [Register] Blueprint-level Error-Handlers: %s' % len(error_list))
            for _error in error_list:
                errors_import = import_string(_error)
                self.register_errors(errors_import)
        # Services registration
        if len(service_list) > 0:
            self._print('├─╼ [Register] Services: %s' % len(service_list))
            for _service in service_list:
                import_string(_service)
        # Templating functions registration
        if len(templating_list) > 0:
            self._print('├─╼ [Register] Templating: %s' % len(error_list))
            for _processor in templating_list:
                templating_import = import_string(_processor)
                self.register_templating(templating_import)
        # Sub-collections registration
        if len(sub_collection_list) > 0:
            self._print('│')
            self._print('├─╼ Sub collections to register: %s ' % len(sub_collection_list))
            for _collection in sub_collection_list:
                self._print('│')
                # self._print('├{:─^70}'.format(' %s ' % _collection))
                # self._print('│')
                collection_import = import_string(_collection)
                self.register_blueprint(collection_import)
        self._print('│')
        self._print('╘{:═^70}'.format(' Done: [%s] ' % self.name))
        current_level -= 1
        self._print('│')
