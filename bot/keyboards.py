from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('Categories', callback_data='categories'),
        ],
        [
            InlineKeyboardButton('Cart', callback_data='cart'),
        ],
        [
            InlineKeyboardButton('Search', callback_data='search')
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def get_categories_list_keyboard(data):
    keyboard = list()
    temp = list()
    for i in data:
        temp.append(
            InlineKeyboardButton(i["id"], callback_data=f'category_{i["id"]}'),
        )
    keyboard.append(temp)

    keyboard.append(
        [
            InlineKeyboardButton('Back', callback_data='back_menu'),
        ]
    )

    return InlineKeyboardMarkup(keyboard)


def get_category_detail_keyboard(data=None):
    keyboard = []
    if data:
        temp = []
        for i in data:
            temp.append(
                InlineKeyboardButton(i["id"], callback_data=f'product_{i["id"]}'),
            )
        keyboard.append(temp)

    keyboard.append(
        [
            InlineKeyboardButton('Back', callback_data='back_categories'),
        ]
    )

    return InlineKeyboardMarkup(keyboard)


def get_product_detail_keyboard(product, context):
    text = 'Add to cart'

    if product["id"] in context.user_data.get('cart', []):
        text = 'Remove from cart'

    keyboard = [
        [
            InlineKeyboardButton('Add to cart', callback_data=f'cart_{product["id"]}'),
        ],
        [
            InlineKeyboardButton('Cart', callback_data='cart'),
        ],
        [
            InlineKeyboardButton('Back', callback_data=f'back_category_{product["category"]["id"]}'),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def get_cart_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('Checkout', callback_data=f'checkout'),
        ],
        [
            InlineKeyboardButton('Back', callback_data=f'back_menu'),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)
