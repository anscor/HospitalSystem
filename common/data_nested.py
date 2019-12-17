def get_data_nested(
    instance, serializer, sub_serializer, arrt_name="items", data_name="items", many=False, is_consist=True
):
    """
    组装items数据
    """
    if not instance:
        return None

    data = serializer(instance).data
    sub = None
    if hasattr(instance, arrt_name):
        data[data_name] = sub_serializer(
            getattr(instance, arrt_name), many=many
        ).data
    elif is_consist:
        data[data_name] = None

    return data
