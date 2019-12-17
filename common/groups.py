def get_all_groups(group, groups=None):
    """
    获取组的所有父组（包括自身）
    """
    if not group:
        return None

    ret = groups
    if not groups:
        ret = set()

    if group not in ret:
        ret.add(group)
    else:
        return ret

    if not hasattr(group, "profile"):
        return ret

    pg = group.profile.parent_group
    if not pg:
        return ret

    gs = get_all_groups(pg, ret)
    return ret & gs
