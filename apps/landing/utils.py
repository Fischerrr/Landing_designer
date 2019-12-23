def save_param_column_catalog(product):
    dict_column = {}
    for param in product.paramcolumnproduct_set.select_related('column_product').all():
        if param.column_product.name in dict_column:
            dict_column[param.column_product.name].update(value=param.value, unit=param.column_product.unit)

    dict_param = {}
    for i, param in enumerate(dict_column):
        dict_param[f'{i}#{param}'] = dict_column[param]

    product.json_param = dict_param
    product.save()


def hsl_change(hsl, saturation, lightness):
    h, s, l = hsl
    s += saturation
    l += lightness
    return h, s, l
