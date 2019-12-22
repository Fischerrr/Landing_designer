from dal_admin_filters import AutocompleteFilter


class AppUserFilter(AutocompleteFilter):
    title = 'Пользователь'
    field_name = 'user'
    autocomplete_url = 'app_auth:autocomplete'
