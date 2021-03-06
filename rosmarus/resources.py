from __future__ import annotations
from collections import namedtuple
from typing import Callable
from os import path as os_path

_resource_handlers = {}
_resource_cleaner_uppers = {}
_resource_cache = {}

resource = namedtuple("resource", ["loaded", "lifespan", "type"])

_DATA_PATH = ""


def register_type_handler(resource_type: str,
                          loader: Callable[[str], object],
                          cleaner_upper: Callable = None) -> None:
    if resource_type in _resource_handlers:
        raise ValueError(
            f"Resource type handler '{resource_type}' already exists!")

    _resource_handlers[resource_type] = loader
    _resource_cleaner_uppers[resource_type] = cleaner_upper


def clear_lifespan(lifespan: str) -> None:
    if lifespan == "":
        raise ValueError("Unable to delete default resource lifespan")

    for k, r in _resource_cache.items():
        if r.lifespan == lifespan:
            _cleanup_resource(_resource_cache[k])
            del _resource_cache[k]


def load(resource_type: str,
         path: str,
         lifespan: str = "",
         *args,
         **kwargs) -> object:
    if resource_type not in _resource_handlers:
        raise ValueError(
            f"No resource handler found for type '{resource_type}'")

    path = os_path.join(_DATA_PATH, path)

    cached_resource = _check_cache(path)
    if cached_resource is not None:
        return cached_resource.value

    loaded_resource = _resource_handlers[resource_type](path, *args, **kwargs)
    _resource_cache[path] = resource(loaded=loaded_resource,
                                     lifespan=lifespan,
                                     type=resource_type)
    return loaded_resource


def cleanup() -> None:
    for res in _resource_cache.values():
        _cleanup_resource(res)


def _cleanup_resource(resource: resource) -> None:
    cleaner_upper = _resource_cleaner_uppers[resource.type]
    if cleaner_upper is not None:
        cleaner_upper(resource.loaded)


def _check_cache(path: str) -> resource:
    return _resource_cache.get(path, None)


def _register_data_path(data_path: str) -> None:
    global _DATA_PATH
    _DATA_PATH = data_path