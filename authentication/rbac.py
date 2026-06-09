def has_access(
        current_role,
        allowed_roles):

    return (
        current_role
        in allowed_roles
    )
from turtle import st

from authentication.rbac import has_access

if has_access(
    st.session_state.role,
    ["Admin", "Manager"]
):
    pass