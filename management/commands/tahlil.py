#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand,CommandError
import telepot
from telepot.namedtuple import InlineKeyboardButton , InlineKeyboardMarkup
import time

#settings.configure(DEBUG=True)
#django.setup()
from  bot.models import User,Bot,Category,Product,Customer



def on_chat_message(msg):

    content_type, chat_type, chat_id = telepot.glance(msg)

    print 'Chat:', content_type, chat_type, chat_id
    if content_type != 'text':
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="جستجو" , callback_data="1"), InlineKeyboardButton(text="سبد خرید", callback_data='2')],])


    command = msg['text'].lower()
    if command == '/start':
        bot.sendMessage(chat_id , "یک گزینه را انتخاب کنید"  , reply_markup= keyboard)

    if content_type =='text' and command!= '/start':
        
        products = Product_Name.objects.values('pname')     #inja command dar database search mishavad
        images = Product_Name.objects.values('image')
        texts = Product_Name.objects.values('text')
        for i in range (len(products)):
            pname= products['pname'][i]
            image= images['image'][i]
            text= texts['text'][i]
            if pname == command :
                bot.sendPhoto(chat_id,image)
                bot.sendMessage(chat_id,text)
            else:
                bot.sendMessage(chat_id,"کالای موردنظر یافت نشد,",reply_markup=keyboard)



def on_callback_query(msg):
    success = 'در حال آماده سازی اطلاعات درخوستی'
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)
    bot.answerCallbackQuery(query_id, text=success)

    if query_data==u"1":
        bot.sendMessage(from_id,"نام محصول را وارد کنید")



    if query_data ==u'2':
        '''
        dar database search mishavad Dar coloumn sabade kharid k
        in user-id kodam mahsol ra b sabad kharid ezafe karde
        va ax va caption e mahsol b user-id frstade mishavad hamrah
        buttone hazf az sabad e kharid
        '''
        keyboard= InlineKeyboardMarkup(Inlinekeyboard=[[InlineKeyboardButton(text= "حذف از سبد خرید",callback_data=3)],])
        sabad= Product_Name.objects.values("sabad")
        image= Product_Name.objects.values('image')
        text= Product_Name.objects.values('text')
        for i in range(len(sabad)):
            if sabad['sabad'][i] == 1:
                bot.sendPhoto(from_id,image['image'][i])
                bot.sendMessage(from_id,text['text'][i],reply_markup=keyboard)


    if query_data ==u'3':
        #algorithm hazf az sabad !!


def show_product(p_id):
    product = Product.objects.get(Product.pk = p_id)
    dict = {'product_id': product.pk, 'Name': product.product_name, 'Image':product.image, 'Text':product.text, 'Price':product.price}
    return dict






Token = '328961413:AAH9DnhEQhjH78feXsRfV-1QnbVAwTL9xZU'
bot = telepot.Bot(Token)
bot.message_loop({'chat': on_chat_message , 'callback_query': on_callback_query})
while 1:
    time.sleep(10)


