# Мы сохраняем словарь с значениями параметров колонки продукта
# при этом учитывая колокни каталога. Дабы не получилось, не соответствие колонок таблицы каталога
# с колонками продукта.
def save_param_column_catalog(catalog, product):
    dict_column = {}
    for column in catalog.columntocatalog_set.values_list('column__name'):
        dict_column[column] = {}

    dict_column_copy = dict_column.copy()
    for param in product.paramcolumnproduct_set.select_related('column_product').all():
        if param.column_product.name in dict_column_copy:
            dict_column[param.column_product.name].update(value=param.value, unit=param.column_product.unit)

    dict_param = {}
    for i, param in enumerate(dict_column_copy):
        dict_param[f'{i}#{param}'] = dict_column_copy[param]

    product.json_param = dict_param
    product.save()


def hsl_change(hsl, saturation, lightness):
    h, s, l = hsl
    s += saturation
    l += lightness
    return h, s, l
