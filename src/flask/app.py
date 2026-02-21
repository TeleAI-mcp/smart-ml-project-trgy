from .globals import request
from .helpers import _endpoint_from_view_func
from .sansio.app import App
from .sansio.scaffold import Scaffold
from .wrappers import Request


class Flask(Scaffold, App):
    """The flask object implements a WSGI application and acts as the central
    object.  It is passed the name of the module or package of the
    application.  Once it is created it will act as a central registry for
    the view functions, the URL rules, template configuration and much more.

    The name of the package is used to resolve resources from inside the
    package or the folder the module is contained in depending on if the
    package parameter resolves to an actual python package (a folder with
    an ``__init__.py`` file inside) or a standard module (just a ``.py`` file).

    For more information about resource loading, see :func:`open_resource`.

    Usually you create a :class:`Flask` instance in your main module or
    in the ``__init__.py`` file of your package like this::

        from flask import Flask
        app = Flask(__name__)

    .. admonition:: About the First Parameter

        The idea of the first parameter is to give Flask an idea of what
        belongs to your application.  This name is used to find resources
        on the filesystem, can be used by extensions to improve debugging
        information and a lot more.

        So it's important what you provide there.  If you are using a single
        module, ``__name__`` is always the correct value.  If you however are
        using a package, it's usually recommended to hardcode the name of
        your package there.

        For example if your application is defined in ``yourapplication/app.py``
        you should create it with one of the two versions below::

            app = Flask('yourapplication')
            app = Flask(__name__.split('.')[0])

        Why is that?  The application will work even with ``__name__``, thanks
        to how resources are looked up.  However it will make debugging more
        painful.  Certain extensions can make assumptions based on the import
        name of your application.

    .. versionadded:: 0.7
       The ``static_url_path``, ``static_folder``, and ``template_folder``
       parameters were added.

    .. versionadded:: 0.8
       The ``instance_path`` and ``instance_relative_config`` parameters were
       added.

    .. versionadded:: 1.0
       The ``root_path`` parameter was added.

    :param import_name: the name of the application package
    :param static_url_path: can be used to specify a different path for the
                            static files on the web.  Defaults to the name
                            of the ``static_folder`` folder.
    :param static_folder: the folder with static files that should be served
                          at ``static_url_path``.  Defaults to the ``'static'``
                          folder in the root path of the application.
    :param static_host: the host to use when adding the static route.
                        Defaults to None. Required when using ``host_matching=True``
                        with a ``static_folder`` configured.
    :param host_matching: set ``True`` if the application should handle host
                          matching. This requires ``SERVER_NAME`` to be set.
    :param subdomain_matching: consider the subdomain relative to
                               ``SERVER_NAME`` when matching routes.
    :param template_folder: the folder that contains the templates that should
                            be used by the application.  Defaults to
                            ``'templates'`` folder in the root path of the
                            application.
    :param instance_path: An alternative instance path for the application.
                          By default the folder ``'instance'`` next to the
                          package or module is assumed to be the instance
                          path.
    :param instance_relative_config: if set to ``True`` relative configuration
                                     filenames are assumed to be relative to the
                                     instance path and not to the application
                                     root.
    :param root_path: The path to the root of the application files.
    """

    def __init__(
        self,
        import_name,
        static_url_path=None,
        static_folder="static",
        static_host=None,
        host_matching=False,
        subdomain_matching=False,
        template_folder="templates",
        instance_path=None,
        instance_relative_config=False,
        root_path=None,
    ):
        super().__init__(
            import_name=import_name,
            static_url_path=static_url_path,
            static_folder=static_folder,
            static_host=static_host,
            host_matching=host_matching,
            subdomain_matching=subdomain_matching,
            template_folder=template_folder,
            instance_path=instance_path,
            instance_relative_config=instance_relative_config,
            root_path=root_path,
        )

    def _get_error_handler_500(self):
        """Override to use the Request object from the context."""
        from .views import DefaultErrorHandler

        return DefaultErrorHandler(request)

    def make_config(self, instance_relative=False):
        """Override to use the Request object from the context."""
        config = super().make_config(instance_relative=instance_relative)
        config["REQUEST"] = request
        return config

    def url_defaults(self, f):
        """Callback function for URL defaults for all view functions of the
        application.  It's called with the endpoint and values and should update
        the values passed in place.
        """
        self.url_default_functions.setdefault(None, []).append(f)
        return f

    def url_value_preprocessor(self, f):
        """Register a URL value preprocessor function for all view functions
        in the application.  These functions will be called before the
        :meth:`before_request` functions.

        The function can modify the values captured from the matched URL before
        they are passed to the view function.
        """
        self.url_value_preprocessors.setdefault(None, []).append(f)
        return f

    def _find_error_handler(self, error):
        """Override to use the Request object from the context."""
        from .views import DefaultErrorHandler

        return DefaultErrorHandler(request)
