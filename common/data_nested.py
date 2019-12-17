def get_data_nested(
    instance, serializer, sub_serializer, arrt_name, data_name, many=False
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

    return data
