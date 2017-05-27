#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
import telepot
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup
import time

from ... import models


class Command(BaseCommand):
    help = 'for running bot execution'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        def on_chat_message(msg):

            content_type, chat_type, chat_id = telepot.glance(msg)

            print 'Chat:', content_type, chat_type, chat_id
            if content_type != 'text':
                return

            keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="جستجو" , callback_data="1"), InlineKeyboardButton(text="سبد خرید", callback_data='2')],])

            command = msg['text']

            if command == '/start':
                for i in range(10):
                    q = models.Sabad_Kharid(cus_id=1, p_id_id=int(i))
                    q.save()


                bot.sendMessage(chat_id , "یک گزینه را انتخاب کنید"  , reply_markup= keyboard)

            if content_type =='text' and command!= '/start':
                search_result = search(command=command)

                for item in search_result:
                    print show_product(str(item['id']))






        def on_callback_query(msg):
            success = 'در حال آماده سازی اطلاعات درخوستی'
            query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
            print('Callback Query:', query_id, from_id, query_data)
            bot.answerCallbackQuery(query_id, text=success)

            if query_data==u"1":
                bot.sendMessage(from_id,"نام محصول را وارد کنید")



            if query_data ==u'2':
                pass
                '''
                dar database search mishavad Dar coloumn sabade kharid k
                in user-id kodam mahsol ra b sabad kharid ezafe karde
                va ax va caption e mahsol b user-id frstade mishavad hamrah
                buttone hazf az sabad e kharid

                keyboard= InlineKeyboardMarkup(Inlinekeyboard=[[InlineKeyboardButton(text= "حذف از سبد خرید",callback_data=3)],])
                sabad= models.Product.objects.values("sabad")
                image= models.Product.objects.values('image')
                text= models.Product.objects.values('text')
                for i in range(len(sabad)):
                    if sabad['sabad'][i] == 1:
                        bot.sendPhoto(from_id,image['image'][i])
                        bot.sendMessage(from_id,text['text'][i],reply_markup=keyboard)
                        '''


            if query_data ==u'3':
                pass
                #algorithm hazf az sabad !!

        def search(command):
            print command
            result = models.Product.objects.filter(product_name__icontains=command).values('id')
            return result

        def show_product(p_id):
            print p_id
            product = models.Product.objects.get(pk=p_id)
            print product
            product_dict = {'product_id': product.pk, 'Name': product.product_name, 'Image':product.image, 'Text':product.text, 'Price':product.price}
            return product_dict

        def cus_id(chat_id):
            customer = models.Customer.objects.get(telegram_id=chat_id).values('id')
            return customer

        def sabad_from_customer(customer_id):
            rows = models.Sabad_Kharid.objects.filter(cus_id=customer_id)
            p_ids = [item.p_id for item in rows]
            products = [Product.objects.get(p_id) for p_id in p_ids]
            return products



        Token = '328961413:AAH9DnhEQhjH78feXsRfV-1QnbVAwTL9xZU'
        bot = telepot.Bot(Token)
        bot.message_loop({'chat': on_chat_message , 'callback_query': on_callback_query})
        while 1:
            time.sleep(10)




