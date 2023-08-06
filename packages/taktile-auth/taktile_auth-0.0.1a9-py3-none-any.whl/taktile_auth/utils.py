import typing as t

from taktile_auth.entities import Permission, Role
from taktile_auth.parser import RESOURCES, ROLES
from taktile_auth.parser.utils import parse_permission


def build_query(query: str) -> Permission:

    parsed_query = parse_permission(query)
    fields = list(RESOURCES[parsed_query["resource_name"]].args.keys())
    resource_vals = {
        fields[x]: parsed_query["resource_args"][x] for x in range(len(fields))
    }
    return Permission(
        actions=set(parsed_query["actions"]),
        resource=RESOURCES[parsed_query["resource_name"]].get_resource()(
            **resource_vals
        ),
    )


def parse_role(role_signature):
    role_name, sep, role_args_str = role_signature.partition("/")
    role_args = role_args_str.split(",")
    role_def = ROLES[role_name]
    return ROLES[role_name].build(**dict(zip(role_def.args, role_args)))


class InsufficientRightsException(Exception):
    pass


def _is_allowed(query: str, roles: t.List[Role]):
    query = build_query(query)
    if not any(query in role for role in roles):
        raise InsufficientRightsException


def assert_access(query: t.Union[str, t.Sequence[str]], roles: t.List[Role]):
    if isinstance(query, str):
        _is_allowed(query, roles)
    else:
        for q in query:
            _is_allowed(q, roles)
