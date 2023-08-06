import logging
import re

from django.urls import include, re_path
from django.urls.resolvers import URLPattern, URLResolver
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import DefaultSchema
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin

from .typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union, UrlsType, ViewType
from .views import APIRootView as RootView


__all__ = ["APIRouter"]


logger = logging.getLogger(__name__)


class APIRouter(DefaultRouter):
    """Router that will show APIViews in API root."""

    registry: List[Tuple[str, Type[APIView], str, Dict[str, Any]]]
    APIRootView: APIView = RootView

    def __init__(
        self,
        *,
        name: Optional[str] = None,
        docstring: Optional[str] = None,
        show_in_shema: bool = False,
        ignore_model_permissions: bool = False,
        navigation_routes: Optional[Dict[str, "APIRouter"]] = None,
        **kwargs: Any,
    ):
        self._navigation_routes: Dict[str, "APIRouter"] = navigation_routes or {}

        name = name if name is not None else self.APIRootView.__name__
        self._root_view: Type[self.APIRootView] = type(name, (self.APIRootView,), {})  # noqa
        self._root_view.__doc__ = docstring if docstring else self.APIRootView.__doc__
        self._root_view.schema = DefaultSchema() if show_in_shema else None
        self._root_view._ignore_model_permissions = ignore_model_permissions

        self.root_view_name: str = name
        super().__init__(**kwargs)

    def register(self, prefix: str, view: ViewType, basename: str = None, **kwargs: Any):  # pylint: disable=W0237
        if basename is None:
            basename = self.get_default_basename(view)  # pragma: no cover

        # Construct default values for regex parts
        params = {key: "..." for key in re.compile(prefix).groupindex}
        params.update(kwargs)
        self.registry.append((prefix, view, basename, params))

        # Invalidate the urls cache
        if hasattr(self, "_urls"):  # pragma: no cover
            del self._urls

    @property
    def navigation_routes(self) -> Dict[str, "APIRouter"]:
        """Add urls from these routers to this routers urls under the root-view of the added router,
        which will be named after the given key. This enables browser navigation of the API."""
        return self._navigation_routes

    @navigation_routes.setter
    def navigation_routes(self, value: Dict[str, "APIRouter"]):
        self._navigation_routes = value

    def get_routes(self, viewset: Type[Union[ViewSetMixin, APIView]]):
        if issubclass(viewset, ViewSetMixin):
            return super().get_routes(viewset)
        return []  # pragma: no cover

    def get_api_root_view(self, api_urls: UrlsType = None) -> Callable[..., Any]:
        api_root_dict: Dict[str, Tuple[str, Dict[str, Any]]] = {}
        list_name = self.routes[0].name

        for prefix, viewset, basename, kwargs in self.registry:
            if issubclass(viewset, ViewSetMixin):
                api_root_dict[prefix] = list_name.format(basename=basename), kwargs
            else:
                api_root_dict[prefix] = basename, kwargs

        for basename in self.navigation_routes:
            api_root_dict[rf"{basename}"] = basename, {}

        return self._root_view.as_view(api_root_dict=api_root_dict)

    def format_regex(self, url: str, prefix: str, lookup: str = "") -> str:
        regex = url.format(prefix=prefix, lookup=lookup, trailing_slash=self.trailing_slash)
        if not prefix and regex[:2] == "^/":  # pragma: no cover
            regex = "^" + regex[2:]
        return regex

    def get_urls(self) -> UrlsType:
        urls: List[Union[URLResolver, URLPattern]] = []

        for prefix, view, basename, _ in self.registry:
            if not issubclass(view, ViewSetMixin):
                regex = self.format_regex(url=self.routes[0].url, prefix=prefix)
                urls.append(re_path(regex, view.as_view(), name=basename))
                continue

            lookup = self.get_lookup_regex(view)
            routes = self.get_routes(view)

            for route in routes:
                mapping = self.get_method_map(view, route.mapping)
                if not mapping:
                    continue

                regex = self.format_regex(url=route.url, prefix=prefix, lookup=lookup)
                initkwargs = route.initkwargs.copy()
                initkwargs.update({"basename": basename, "detail": route.detail})

                view_ = view.as_view(mapping, **initkwargs)
                name = route.name.format(basename=basename)
                urls.append(re_path(regex, view_, name=name))

        if self.include_root_view:
            view = self.get_api_root_view(api_urls=urls)
            root_url = re_path(r"^$", view, name=self.root_view_name)
            urls.append(root_url)

        if self.include_format_suffixes:
            urls = format_suffix_patterns(urls)

        for basename, router in self.navigation_routes.items():
            router.root_view_name = basename
            urls.append(re_path(rf"^{basename}/", include(router.urls)))

        return urls
