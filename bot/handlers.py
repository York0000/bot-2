import requests

from bot.keyboards import get_menu_keyboard, get_categories_list_keyboard, get_category_detail_keyboard, \
    get_product_detail_keyboard, get_cart_keyboard
from bot.utils import save_user


def start(update, context):
    user = update.effective_user
    save_user(user)
    update.message.reply_text('Menu', reply_markup=get_menu_keyboard())


def categories_list(update, context):
    query = update.callback_query

    data = requests.get('http://127.0.0.1:8000/categories/').json()

    text = ''
    for category in data:
        text += f'{category["id"]}. {category["title"]}\n'

    query.edit_message_text(text=text, reply_markup=get_categories_list_keyboard(data))


def category_detail(update, context):
    query = update.callback_query
    pk = query.data.split('_')[1]

    data = requests.get(f'http://127.0.0.1:8000/categories/{pk}/').json()

    if not data:
        query.edit_message_text(text='No products yet',
                                reply_markup=get_category_detail_keyboard())
        return

    text = ''
    for product in data:
        text += f'{product["id"]}. {product["title"]}\n'

    query.edit_message_text(text=text, reply_markup=get_category_detail_keyboard(data))


def product_detail(update, context):
    query = update.callback_query
    pk = query.data.split('_')[1]

    product = requests.get(f'http://127.0.0.1:8000/products/{pk}').json()

    text = f'Title: {product["title"]}\n' \
           f'Price: {product["price"]}\n' \
           f'Description: {product["description"]}\n'

    context.bot.send_photo(
        chat_id=query.message.chat.id,
        photo=requests.get(product["image"]).content,
        caption=text,
        reply_markup=get_product_detail_keyboard(product, context)
    )
    context.bot.delete_message(chat_id=query.message.chat.id,
                               message_id=query.message.message_id)


def search(update, context):
    pass


def back(update, context):
    query = update.callback_query
    level = query.data.split('_')[1]

    if level == 'menu':
        query.message.reply_text(text='Menu', reply_markup=get_menu_keyboard())
    elif level == 'categories':
        data = requests.get('http://127.0.0.1:8000/categories/').json()

        text = ''
        for category in data:
            text += f'{category["id"]}. {category["title"]}\n'

        query.message.reply_text(text=text, reply_markup=get_categories_list_keyboard(data))

    if level == 'category':
        pk = query.data.split('_')[2]

        data = requests.get(f'http://127.0.0.1:8000/categories/{pk}/').json()

        if not data:
            query.message.reply_text(text='No products yet',
                                     reply_markup=get_category_detail_keyboard())
            return

        text = ''
        for product in data:
            text += f'{product["id"]}. {product["title"]}\n'

        query.message.reply_text(text=text, reply_markup=get_category_detail_keyboard(data))

    context.bot.delete_message(chat_id=query.message.chat.id,
                               message_id=query.message.message_id)


def update_cart(update, context):
    query = update.callback_query
    pk = query.data.split('_')[1]

    cart = context.user_data.get('cart', [])

    if pk in cart:
        cart.remove(pk)
        text = 'Removed from cart'
    else:
        cart.append(pk)
        text = 'Added to cart'

    context.user_data['cart'] = cart
    query.answer(text=text)


def cart_list(update, context):
    cart = context.user_data.get('cart', [])
    query = update.callback_query

    if not cart:
        query.answer(text='Cart in empty')
    else:
        data = requests.get(f'http://127.0.0.1:8000/cart-data/?products={cart}').json()

        text = ''
        for product in data:
            text += f'{product["id"]}. {product["title"]}\n'

        query.message.reply_text(text=text, reply_markup=get_cart_keyboard())
        context.bot.delete_message(chat_id=query.message.chat.id,
                                   message_id=query.message.message_id)


def checkout(update, context):
    query = update.callback_query
    user_id = update.effective_user.id
    cart = context.user_data['cart']

    requests.post(
        'http://127.0.0.1:8000/orders/create/',
        data={
            'user_id': user_id,
            'products': cart
        }
    )

    query.answer('Order is created')
    context.user_data['cart'] = []
    
    query.edit_message_text(text='Menu', reply_markup=get_menu_keyboard())

