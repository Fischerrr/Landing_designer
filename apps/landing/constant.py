GREETING = 1
ABOUT_PRODUCT = 2
FEATURE = 3
CATALOG = 4
FORM_SELECTION = 5
SERVICE = 6
BUY_GET = 7
PRODUCT_RANGE = 8
ADD_FORM = 9
HIDE_TEXT = 10
MAP = 11
COMPANY = 12
CERTIFICATES = 13
COMMENT = 14
PARTNERS = 15
SUBSCRIBE = 16
OTHER_OFF = 17

BLOCK_TEMPLATE_CHOICE = (
    (GREETING, 'Приветствие'),
    (ABOUT_PRODUCT, 'О продукте'),
    (FEATURE, 'Особенности'),
    (CATALOG, 'Каталог'),
    (FORM_SELECTION, 'Форма помощи с выбором'),
    (SERVICE, 'Сервис'),
    (BUY_GET, 'Премущества покупки'),
    (PRODUCT_RANGE, 'Ассортимент продукта'),
    (ADD_FORM, 'Форма дополнительных предложений'),
    (HIDE_TEXT, 'Блок со скрытым текстом'),
    (MAP, 'Карта'),
    (COMPANY, 'О компании'),
    (CERTIFICATES, 'Сертификаты'),
    (COMMENT, 'Отзывы'),
    (PARTNERS, 'Партнеры'),
    (SUBSCRIBE, 'Подписка на рассылку'),
    (OTHER_OFF, 'Другие предложения'),
)

CATALOG_IMAGE, CATALOG_GALLERY = [1, 2]

CATALOG_PRODUCT_TEMPLATE = (
    (CATALOG_IMAGE, 'Шаблон с изображением'),
    (CATALOG_GALLERY, 'Шаблон с галереей'),
)

# Данный словарь необходим для отображения необходимых полей в админке у Блока
# значение данного словаря является список в котором перечисленны поля Блока, которые будут отображены пример:
# ['subtitle', 'text_button'] -- поля Блока
# ['title', ['gallery2block_set-0-image']], --- поле Блока и поле с изображением связанной модели Gallery2Block
# ['title', ['gallery2block_set-0-image', ['id_gallery2block_set-MAX_NUM_FORMS', 4]]] --- тоже самое, но теперь
# с указанием максимального количества допустимых экземпляров связанной модели.
BLOCK_FIELDS_DICT = {
    GREETING: ['title', 'subtitle', 'text_button', 'catalog_file',
               ['text2block_set-0-description', 'text2block_set-0-priority', ['id_text2block_set-MAX_NUM_FORMS', 4]]],
    ABOUT_PRODUCT: ['title', 'subtitle'],
    FEATURE: ['title', 'svg_background',
              ['text2block_set-0-description', 'text2block_set-0-priority', ['id_text2block_set-MAX_NUM_FORMS', 6]]],
    CATALOG: ['title', 'catalog', 'gallery_catalog', 'form'],
    FORM_SELECTION: [
        'title', 'subtitle', 'title_form', 'multiselectsform2block_set-group',
        'monoselectsform2block_set-group', 'specificationsform2block_set-group'
    ],
    SERVICE: ['title', 'subtitle',
              ['text2block_set-0-title', 'text2block_set-0-description', 'text2block_set-0-priority',
               ['id_text2block_set-MAX_NUM_FORMS', 4]]],
    BUY_GET: ['title', ['text2block_set-0-svg', 'text2block_set-0-description', 'text2block_set-0-priority',
                        ['id_text2block_set-MAX_NUM_FORMS', 4]]],
    PRODUCT_RANGE: ['title', ['text2block_set-0-title', 'text2block_set-0-description', 'text2block_set-0-priority',
                            ['id_text2block_set-MAX_NUM_FORMS', 3]]],
    ADD_FORM: ['title', 'checkboxform2block_set-group'],
    HIDE_TEXT: [
        'title', 'subtitle', 'text_button',
        ['text2block_set-0-title', 'text2block_set-0-description', 'text2block_set-0-title_hide_text',
         'text2block_set-0-hide_text', 'text2block_set-0-priority', 'text2block_set-0-column_number']
    ],
    MAP: ['title'],
    COMPANY: [
        'title', 'subtitle', 'description',
        ['comments2block_set-0-image', 'comments2block_set-0-name', 'comments2block_set-0-post',
         ['id_text2block_set-MAX_NUM_FORMS', 1]]
    ],
    CERTIFICATES: [['gallery2block_set-0-image', 'gallery2block_set-0-priority']],
    COMMENT: [
        ['comments2block_set-0-name', 'comments2block_set-0-description', 'comments2block_set-0-company',
         'comments2block_set-0-priority', 'comments2block_set-0-image']
    ],
    PARTNERS: [['text2block_set-0-image', 'text2block_set-0-link', 'text2block_set-0-priority']],
    SUBSCRIBE: [],
    OTHER_OFF: ['title'],
}

BLOCK_TEMPLATE = {
    GREETING: '',
    ABOUT_PRODUCT: '',
    FEATURE: '',
    CATALOG: '',
    FORM_SELECTION: '',
    SERVICE: '',
    BUY_GET: '',
    PRODUCT_RANGE: '',
    ADD_FORM: '',
    HIDE_TEXT: '',
    MAP: '',
    COMPANY: '',
    CERTIFICATES: '',
    COMMENT: '',
    PARTNERS: '',
    SUBSCRIBE: '',
    OTHER_OFF: '',
}

COLUMN_NUMBER = (
    (1, 'Первая колонка'),
    (2, 'Вторая колонка'),
)
