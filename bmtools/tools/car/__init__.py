
from ..registry import register

@register("car")
def car():
    from .api import build_tool
    return build_tool
