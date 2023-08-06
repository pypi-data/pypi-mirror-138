# coding: utf-8
"""
Handles conversion of realitive imports
"""
# region Imports
import re
from dataclasses import dataclass
from typing import List, NamedTuple
from kwhelp.decorator import AcceptedTypes
from functools import cache
import zlib
# endregion Imports


class rimport(NamedTuple):
    # python ≥ 3.6
    frm: str
    imp: str


class rimport_lng(NamedTuple):
    # python ≥ 3.6
    frm: str
    imp: str
    as_: str
@dataclass
class RealitiveInfo:
    """Realitive info"""
    in_branch: str
    """Original input branch"""
    comp_branch: str
    """Original branch to compare to in_branch"""
    sep: str
    """Seperator"""
    in_branch_rel: List[str]
    """Compare result relative part of in_branch"""
    comp_branch_rel: List[str]
    """Compare result relative part of comp_branch"""
    distance: int
    """Distance between branches"""
    common_parts: List[str]
    """part that in_branch and comp_branch have in common"""


@AcceptedTypes(str)
def camel_to_snake(input: str) -> str:
    """
    Converts Camel case to snake clase

    Args:
        name (str): Camel name

    Returns:
        str: snake case
    """
    _input = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', input)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', _input).lower()

@cache
@AcceptedTypes(str, opt_all_args=True)
def get_rel_info(in_branch: str, comp_branch: str, sep: str = '.') -> RealitiveInfo:
    """
    Gets realitive info between branches such as ``com.sun.star.configuration``
    and ``com.sun.star.uno``

    Args:
        in_branch (str): branch to compare
        comp_branch (str): branch to get realitive information from compared to ``in_branch``
        sep (str, optional): Branch seperator. Defaults to ``.``

    Returns:
        RealitiveInfo: Class instance containing realitive info.
    """
    in_branch_parts = in_branch.split(sep)
    comp_branch_parts = comp_branch.split(sep)
    rel_len = len(comp_branch_parts)
    common_roots = 0
    for i, b in enumerate(in_branch_parts):
        if i > rel_len:
            break
        try:
            if b == comp_branch_parts[i]:
                common_roots += 1
                continue
        except IndexError:
            break
        break
    comp_branch_rel = comp_branch_parts[common_roots:]
    in_branch_rel = in_branch_parts[common_roots:]
    diff = len(in_branch_rel)
    distance = diff
    common_parts = in_branch_parts[:common_roots]
    # result = ((diff + 1), sep.join(comp_branch_rel))
    result = RealitiveInfo(
        in_branch=in_branch,
        comp_branch=comp_branch,
        sep=sep,
        in_branch_rel=in_branch_rel,
        comp_branch_rel=comp_branch_rel,
        distance=distance,
        common_parts=common_parts
    )
    # sep_str = sep * (diff + 1)
    return result

@cache
@AcceptedTypes(str, opt_all_args=True)
def get_rel_import(in_str: str, ns: str, sep: str = '.') -> rimport:
    """
    Gets realitive import Tuple

    Args:
        in_str (str): Namespace and object such as ``com.sun.star.uno.Exception``
        ns (str): Namespace used to get realitive postion such as ``com.sun.star.awt``
        sep (str, optional): Namespace seperator. Defaults to ``.``

    Returns:
        Tuple[str, str]: realitive import info such as ``('..uno.exception', 'Exception')``
    """
    # i_str = com.sun.star.uno.Exception
    # ns = com.sun.star.configuration
    # ("..uno.exception", "Exception")
    # compare ns to ns so drop last name of i_str
    name_parts = in_str.split(sep)
    name = name_parts.pop()
    camel_name = camel_to_snake(name)
    if len(name_parts) == 0:
        # this is a single word such as XInterface
        # assume it is in the same namespace as this import
        return rimport(f'.{camel_name}', f'{name}')
    ns2 = sep.join(name_parts)
    if ns2 == ns:
        return (f'.{camel_name}', f'{name}')
    if len(name_parts) == 1:
        # this is a single word
        # assume it is in the same namespace as this import
        return rimport(f'.{camel_to_snake(in_str)}', f'{in_str}')
    try:
        info = get_rel_info(in_branch=ns, comp_branch=ns2, sep=sep)
        prefix = sep * (info.distance + 1)
        result_parts = info.comp_branch_rel + [camel_name]
        from_str = prefix
        from_str = from_str + sep.join(result_parts)
        return rimport(from_str, name)
    except Exception:
        # logger.error(e, exc_info=True)
        pass
    short = ns2.replace('com.sun.star.', '')
    # logger.warn(f"get_rel_import(): Last ditch effort. Returning: (ooo_uno.uno_obj.{short}.{camel_name}', {name})")
    return rimport(f'ooo_uno.uno_obj.{short}.{camel_name}', f'{name}')

@cache
@AcceptedTypes(str, opt_all_args=True)
def get_rel_import_long(in_str: str, ns: str, sep: str = '.') -> rimport_lng:
    """
    Gets realitive import Tuple

    Args:
        in_str (str): Namespace and object such as ``com.sun.star.uno.Exception``
        ns (str): Namespace used to get realitive postion such as ``com.sun.star.awt``
        sep (str, optional): Namespace seperator. Defaults to ``.``

    Returns:
        Tuple[str, str]: realitive import info such as ``('..uno.exception', 'Exception', 'uno_exception')``
    """
    if in_str.startswith('com.'):
        full_name = in_str
    else:
        full_name = ns + sep + in_str
    frm, imp = get_rel_import(in_str=in_str, ns=ns, sep=sep)
    sas = imp + '_' + get_shortened(full_name)
    return rimport_lng(frm, imp, sas)


@AcceptedTypes(str, opt_all_args=True)
def get_rel_import_long_name(in_str: str, ns: str, sep: str = '.') -> str:
    """
    Geta a long Name. Same as getting last part of ``get_rel_import_long()``

    Args:
        in_str (str): Namespace and object such as ``com.sun.star.uno.Exception``
        ns (str): Namespace used to get realitive postion such as ``com.sun.star.awt``
        sep (str, optional): Namespace seperator. Defaults to ``.``

    Returns:
        str: Long name such as ``uno_exception``
    """
    _, _, sas = get_rel_import_long(in_str=in_str, ns=ns, sep=sep)
    return sas

@AcceptedTypes(str)
def get_shortened(in_str:str) -> str:
    """
    Shortens input string

    Args:
        in_str (str): string to shorten

    Returns:
        str: Shortend string
        
    Example:
        >>> get_shortened('com.sun.star.inspection.XObjectInspector')
        3c860faa
    """
    res = bytes(in_str, 'utf-8')
    return hex(zlib.adler32(res))[2:]


@AcceptedTypes(str, opt_all_args=True)
def get_rel_import_short_name(in_str: str, ns: str, sep: str = '.') -> str:
    """
    Geta a name. Same as getting last part of ``get_rel_import()``

    Args:
        in_str (str): Namespace and object such as ``com.sun.star.uno.Exception``
        ns (str): Namespace used to get realitive postion such as ``com.sun.star.awt``
        sep (str, optional): Namespace seperator. Defaults to ``.``

    Returns:
        str: name such as ``XInterface``
    """
    _, sn = get_rel_import(in_str=in_str, ns=ns, sep=sep)
    return sn


@AcceptedTypes(str, opt_all_args=True)
def get_ns_from_rel(full_ns:str, rel_from:str, comp:str, sep: str = '.') -> str:
    """
    Converts a relative import into a full namespace

    Args:
        full_ns (str): The namespace that import is relative to
        rel_from (str): from part of import such as ``..uno.x_interface``
        comp (str): Component name such as ``XInterface``
        sep (str, optional): Seperator. Defaults to ``.``.

    Returns:
        str: full namespace such as ``com.sun.star.uno.XInterface``
    """
    s = rel_from
    sep_count = 0
    while s.startswith(sep):
        s = s[1:]
        sep_count += 1
    if sep_count == 1:
        # import is in the same namespace
        return full_ns + sep + comp
    s_parts = s.rsplit(sep=sep, maxsplit=1) # drop camel module name
    if len(s_parts) == 1:
        # import is in the same namespace
        return full_ns + sep + comp
    else:
        s = s_parts[0]
    if sep_count == 0:
        return full_ns + sep + s + sep + comp
    ns_parts = full_ns.split(sep)
    if sep_count > len(ns_parts):
        return s + sep + comp
    slice = 1 - sep_count # ignore first . and convert to neg
    if slice >= 0:
        return sep.join(ns_parts) + sep + comp
    ns = sep.join(ns_parts[:slice])
    return ns + sep + s + sep + comp
    
    