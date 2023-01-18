from .flask_classy import FlaskView
from .flask_classy import get_interesting_members
from .flask_classy import DecoratorCompatibilityError


class Classy42(FlaskView):
    ignore_methods = []

    @classmethod
    def register(cls, app, route_base=None, subdomain=None, route_prefix=None,
                 trailing_slash=None):
        """Registers a FlaskView class for use with a specific instance of a
        Flask app. Any methods not prefixes with an underscore are candidates
        to be routed and will have routes registered when this method is
        called.

        :param trailing_slash:
        :param app: an instance of a Flask application

        :param route_base: The base path to use for all routes registered for
                           this class. Overrides the route_base attribute if
                           it has been set.

        :param subdomain:  A subdomain that this registration should use when
                           configuring routes.

        :param route_prefix: A prefix to be applied to all routes registered
                             for this class. Precedes route_base. Overrides
                             the class' route_prefix if it has been set.
        """

        if cls is FlaskView:
            raise TypeError("cls must be a subclass of FlaskView, not FlaskView itself")

        if route_base:
            cls.orig_route_base = cls.route_base
            cls.route_base = route_base

        if route_prefix:
            cls.orig_route_prefix = cls.route_prefix
            cls.route_prefix = route_prefix

        # if not subdomain:
        #     if hasattr(app, "subdomain") and app.subdomain is not None:
        #         subdomain = app.subdomain
        #     elif hasattr(cls, "subdomain"):
        #         subdomain = cls.subdomain

        if trailing_slash is not None:
            cls.orig_trailing_slash = cls.trailing_slash
            cls.trailing_slash = trailing_slash

        members = get_interesting_members(FlaskView, cls)
        special_methods = ["get", "put", "patch", "post", "delete", "index"]
        # print('====')
        for name, value in members:
            # print(name)
            # print(value)
            # print('=====')
            proxy = cls.make_proxy_method(name)
            route_name = cls.build_route_name(name)
            try:
                if hasattr(value, "_rule_cache") and name in value._rule_cache:
                    for idx, cached_rule in enumerate(value._rule_cache[name]):
                        rule, options = cached_rule
                        rule = cls.build_rule(rule)
                        sub, ep, options = cls.parse_options(options)

                        # if not subdomain and sub:
                        #     subdomain = sub

                        if ep:
                            endpoint = ep
                        elif len(value._rule_cache[name]) == 1:
                            endpoint = route_name
                        else:
                            endpoint = "%s_%d" % (route_name, idx,)

                        app.add_url_rule(rule, endpoint, proxy, **options)

                elif name in special_methods:
                    if name in ["get", "index"]:
                        methods = ["GET"]
                    else:
                        methods = [name.upper()]

                    rule = cls.build_rule("/", value)
                    if not cls.trailing_slash:
                        rule = rule.rstrip("/")
                    app.add_url_rule(rule, route_name, proxy, methods=methods)

                else:
                    route_str = '/%s/' % name
                    if not cls.trailing_slash:
                        route_str = route_str.rstrip('/')
                    rule = cls.build_rule(route_str, value)
                    app.add_url_rule(rule, route_name, proxy)
            except DecoratorCompatibilityError:
                raise DecoratorCompatibilityError(
                    "Incompatible decorator detected on %s in class %s" % (name, cls.__name__))

        if hasattr(cls, "orig_route_base"):
            cls.route_base = cls.orig_route_base
            del cls.orig_route_base

        if hasattr(cls, "orig_route_prefix"):
            cls.route_prefix = cls.orig_route_prefix
            del cls.orig_route_prefix

        if hasattr(cls, "orig_trailing_slash"):
            cls.trailing_slash = cls.orig_trailing_slash
            del cls.orig_trailing_slash
