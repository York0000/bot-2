from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from bot.handlers import start, categories_list, category_detail, product_detail, back, search, update_cart, cart_list, \
    checkout
from bot.settings import BOT_TOKEN


def main():
    updater = Updater(BOT_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    dispatcher.add_handler(CallbackQueryHandler(categories_list, pattern='^categories$'))
    dispatcher.add_handler(CallbackQueryHandler(category_detail, pattern='^category_'))
    dispatcher.add_handler(CallbackQueryHandler(product_detail, pattern='^product_'))
    dispatcher.add_handler(CallbackQueryHandler(back, pattern='^back_'))
    dispatcher.add_handler(CallbackQueryHandler(update_cart, pattern='^cart_'))
    dispatcher.add_handler(CallbackQueryHandler(cart_list, pattern='^cart$'))
    dispatcher.add_handler(CallbackQueryHandler(checkout, pattern='^checkout$'))
    dispatcher.add_handler(CallbackQueryHandler(search, pattern='^search$'))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
