
""" Helpers to implement a plugin infrastructure in Python. """

import logging
import pkg_resources
import typing as t

from nr.util.generic import T

logger = logging.getLogger(__name__)


def load_entrypoint(group: str, name: str) -> t.Any:
  """ Load a single entrypoint value. Raises a #RuntimeError if no such entrypoint exists. """

  for ep in pkg_resources.iter_entry_points(group, name):
    return ep.load()
  raise RuntimeError(f'no entrypoint "{name}" in group "{group}"')


def load_plugins_from_entrypoints(
  group: str,
  base_class: type[T],
  constructor: t.Callable[[type[T]], T] | None = None,
  do_raise: bool = False,
  names: list[str] | None = None,
  filter: t.Callable[[pkg_resources.EntryPoint], bool] | None = None,
) -> dict[str, T]:
  """ Loads plugins from an entrypoint group. All entrypoints must point to a class of the specified *base_class*.
  If *do_raise* is `True` and an entrypoint does not point to a subclass of the given type, a #RuntimeError is
  raised, otherwise a warning is printed. If the entrypoint cannot be imported and *do_raise* is `False`, a warning
  will be printed as well.

  The *constructor* will be used to create instances of the *base_class*. If it is omitted, the instances will be
  created without arguments. If the construction fails and *do_raise* is `False`, a warning will be printed.

  By passing a predicate for the *filter* argument, you can filter which entry points in the group are considered
  for loading in the first place. """

  if not isinstance(base_class, type):
    raise TypeError(f'base_class must be a type, got {type(base_class).__name__}')

  result = {}
  for ep in pkg_resources.iter_entry_points(group):
    if names is not None and ep.name not in names:
      continue
    if filter is not None and not filter(ep):
      continue

    try:
      cls = ep.load()
    except ImportError:
      if do_raise:
        raise
      logger.exception(f'Unable to load entrypoint "%s" due to ImportError', ep)
      continue

    if not isinstance(cls, type) or not issubclass(cls, base_class):
      message = f'Entrypoint "%s" does not point to a %s subclass (got value: %r)'
      if do_raise:
        raise RuntimeError(message % (ep, base_class.__name__, cls))
      logger.error(message, ep, base_class.__name__, cls)
      continue

    try:
      result[ep.name] = constructor(cls) if constructor else cls()
    except Exception:
      message = f'Instance from entrypoint "%s" could not be created'
      if do_raise:
        raise RuntimeError(message % (ep,))
      logger.exception(message, ep)

  if names is not None and (missing_plugins := set(names) - result.keys()):
    msg = f'missing plugin{"" if len(missing_plugins) == 1 else "s"} in entrypoint group "{group}": {missing_plugins}'
    raise RuntimeError(msg)

  return result
