#!/usr/bin/env python
# -*- coding: utf-8 -*-

import emoji
import telepot
import time
from django.core.management.base import BaseCommand
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from Category import CategoryDataAccess as CatDA
from Comment import CommentDataAccess as com_DA
from CustomerDataAccess import CustomerDataAccess as CDA
from ProductDataAccess import ProductDataAccess as PDA
from Search import SearchDataAccess as SDA
from Shopping_Card import ShoppingCard as SHC
from Order import Order
from ... import models


class Command(BaseCommand):
    help = 'for running bot execution'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        def on_chat_message(msg):


            #Get User data From User RealTime
            print msg
            try:
                username = msg['from']['username']
            except :
                username = "Null"
            content_type, chat_type, chat_id = telepot.glance(msg)
            customer = CDA(chat_id)

            customer_id = customer.return_customer_id()

            if content_type == "text":
                command = msg['text']
                print command
            elif content_type == 'contact':
                command = msg['contact']['phone_number']
            else:
                command = 'None'

            if type(customer.return_user_state()) !=  None:
                user_state = customer.return_user_state()
                print "state: " + str(user_state)
            else:
                user_state = "Null"
                print "state: " + str(user_state)

            #End Of Get Data From User

            keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=emoji.emojize(":mag_right:",use_aliases=True)+u"دسته بندی ها", callback_data="categories"),InlineKeyboardButton(text=emoji.emojize(":mag_right:",use_aliases=True)+u"جستجو", callback_data="search")],[ InlineKeyboardButton(text=emoji.emojize(" :package:",use_aliases=True)+u"سبد خرید", callback_data='sabad'), InlineKeyboardButton(text=emoji.emojize(" :postbox:",use_aliases=True)+u"انتقاد و پیشنهاد", callback_data='enteghadstart')],[ InlineKeyboardButton(text=emoji.emojize(" :memo:",use_aliases=True)+u"وارد کردن اطلاعات شخصی برای خرید", callback_data='enterinfo_firstname')],[InlineKeyboardButton(text=emoji.emojize(" :back:",use_aliases=True)+u"بازگشت به منوی اصلی", callback_data='return')],])
            if command == '/start':
                for i in range(1,4):
                    try:
                        q = models.Sabad_Kharid(cus_id=customer, p_id_id=int(i))
                        q.save()
                    except :
                        pass
                #Add User if thechat_id from user not in Database
                if not customer.check_customer_is():
                    customer.add_customer(username)
                    bot.sendPhoto(chat_id, "http://www.byronbible.org/wp-content/uploads/2013/07/Welcome-1024x576.jpg", caption="به بات گرام خوش آمدید، لطفا یکی از گزینه های زیر زیر را انتخاب کنید.", reply_markup= keyboard)
                else:
                    bot.sendPhoto(chat_id, "http://www.byronbible.org/wp-content/uploads/2013/07/Welcome-1024x576.jpg", caption="به بات گرام خوش آمدید، لطفا یکی از گزینه های زیر زیر را انتخاب کنید.", reply_markup= keyboard)

                #End Of Add User if not exist




            elif content_type == 'text' and user_state == 'search':
                search_obj = SDA(search_word=command, page_number=1)
                search_results = search_obj.search()
                print list(search_results)
                if list(search_results) == []:
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=emoji.emojize(":mag_right:",use_aliases=True)+u"جستجو", callback_data="search")], [ InlineKeyboardButton(text=emoji.emojize(" :back:",use_aliases=True)+' '+ u"بازگشت به منوی اصلی" , callback_data='return')]])
                    bot.sendMessage(chat_id,"نتیجه ای یافت نشد",reply_markup=keyboard)
                    customer.unset_state()

                else :
                    for item in search_results:
                        product = PDA(p_id=str(item['id']))
                        keyboard_1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=str(str(product.show_product()['Price'])+" تومان")+"💵", callback_data="4"), InlineKeyboardButton(text=u"افزودن به سبد خرید"+emoji.emojize(" :package:",use_aliases=True), callback_data='add_to_cart '+str(item['id']))] ,[InlineKeyboardButton(text=u"جزییات بیشتر"+emoji.emojize(" :clipboard:",use_aliases=True) ,callback_data=str("Product"+str(product.show_product()["product_id"])))],])
                        #bot.sendMessage(chat_id,show_product(str(item['id']))['Name'])
                        caption=u"نام محصول: "+product.show_product()['Name']
                        bot.sendPhoto(chat_id,product.show_product()['Image'],caption=caption,reply_markup=keyboard_1)
                    keyboard_morenext= InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=emoji.emojize( " :arrow_right:",use_aliases=True)+ " " + u"نمایش ۱۰ محصول بعدی" ,callback_data='morenext')],[InlineKeyboardButton(text=emoji.emojize(" :back:",use_aliases=True)+ "  " + u"بازگشت به منوی اصلی", callback_data='return')]])
                    bot.sendMessage(chat_id,"  نتیجه جستجوی شما  ", reply_markup=keyboard_morenext)
                    customer.set_current(current_word='search_' + command + '_1')
                    customer.unset_state()

            elif content_type == 'text' and user_state == 'enterinfo_firstname':
                customer.enter_first_name(f_name=command)
                customer.set_state(state_word='enterinfo_lastname')
                bot.sendMessage(chat_id, "نام خانوادگی خود را وارد کنید.")

            elif content_type == 'text' and user_state == 'enterinfo_lastname':
                customer.enter_last_name(l_name=command)
                customer.set_state(state_word='enterinfo_address')
                bot.sendMessage(chat_id, "آدرس خود را وارد کنید")

            elif content_type == 'text' and user_state == 'enterinfo_address':
                customer.enter_address(address=command)
                customer.set_state(state_word='enterinfo_phone')
                bot.sendMessage(chat_id, "شماره تلفن خود را به وسیله دکمه زیر برای ما بفرستید.")
                location_keyboard = KeyboardButton(text="send_location",
                                                   request_location=True)  # creating location button object
                contact_keyboard = KeyboardButton(text='Share contact',
                                                  request_contact=True)  # creating contact button object
                custom_keyboard = [[location_keyboard, contact_keyboard]]  # creating keyboard object
                reply_markup = ReplyKeyboardMarkup(keyboard=custom_keyboard)
                bot.sendMessage(chat_id=chat_id, text="دکمه اشتراک شماره تلفن نمایش داده خواهد شد.", reply_markup=reply_markup)

            elif (content_type == 'text' or content_type == 'contact') and user_state == 'enterinfo_phone':
                if content_type == "contact":
                    customer.enter_phone(phone=command)
                    customer.unset_state()
                    bot.sendMessage(chat_id, "اطلاعات شما  با موفقیت ثبت شد.")
                else:
                    bot.sendMessage(chat_id=chat_id, text="لطفا بر روی دکمه فرستادن شماره تلفن به ربات کلیک کنید")



            elif content_type == 'text' and  'naghd' in user_state:
                naghd_cat = int(user_state.replace("naghd", ""))
                comment_obj = com_DA(t_id=chat_id,new_comment=command, cat_id=naghd_cat)
                if comment_obj.enter_comment():
                    notification="نظر با موفقیت ثبت شد. با تشکر از شما"
                    bot.sendMessage(chat_id, text=notification)
                    customer.unset_state()
                else:
                    notification="لطفا مجددا نظر را وارد نمایید."
                    bot.sendMessage(chat_id, text=notification)


            elif content_type == 'text' and "User_comment" in user_state:
                comment_obj = com_DA(t_id=customer.return_customer_id(), p_id=user_state[12:], new_comment=command)
                if comment_obj.enter_user_comment():
                    notification="نظر با موفقیت ثبت شد. با تشکر از شما"
                    bot.sendMessage(chat_id, text=notification)
                    customer.unset_state()
                else:
                    notification="لططفا مجددا نظر را وارد نمایید."
                    bot.sendMessage(chat_id, text=notification)
            #end buying by getting comment
            elif content_type == 'text' and user_state == 'buy_comment':
                sabad = SHC(c_id=customer_id)
                sabad_products = sabad.sabad_from_customer()
                for product in sabad_products:
                    sabad_product = SHC(c_id=customer_id, p_id=product[0])
                    sabad_product.del_from_cart()
                order = Order(c_id=customer_id, order_time=time.time(), info=command)
                is_order_done = order.add_card_to_order()
                if is_order_done:
                    customer.unset_state()
                    bot.sendMessage(chat_id, "خرید با موفقیت انجام شد")
                else:
                    bot.sendMessage(chat_id, "مشکلی بوجود آمده")




        def on_callback_query(msg):
            #Get User Query Data
            query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
            customer = CDA(from_id)
            customer_id = customer.return_customer_id()
            command = msg
            #ENd of getting Query Data from user

            #Whene user Press on Search Button
            if query_data == u"search":
                if customer.set_state(state_word='search'):
                    bot.answerCallbackQuery(query_id, text="نام محصول را وارد کنید", show_alert=True)
            #End Of Search Button

            #Whene user Press on Enter Info Button
            if query_data == u"enterinfo_firstname":
                if customer.set_state(state_word='enterinfo_firstname'):
                    bot.answerCallbackQuery(query_id, text="اطلاعات خود را وارد کنید", show_alert=True)
                    bot.sendMessage(from_id, "نام خود را وارد نمایید.")
            #End Of Enter Info Button




            #Return to main Menu
            if query_data == u'return':
                keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=emoji.emojize(":mag_right:",use_aliases=True)+u"دسته بندی ها", callback_data="categories"),InlineKeyboardButton(text=emoji.emojize(":mag_right:",use_aliases=True)+u"جستجو", callback_data="search")],[ InlineKeyboardButton(text=emoji.emojize(" :package:",use_aliases=True)+u"سبد خرید", callback_data='sabad'), InlineKeyboardButton(text=emoji.emojize(" :postbox:",use_aliases=True)+u"انتقاد و پیشنهاد", callback_data='enteghadstart')],[ InlineKeyboardButton(text=emoji.emojize(" :memo:",use_aliases=True)+u"وارد کردن اطلاعات شخصی برای خرید", callback_data='enterinfo_firstname')],[InlineKeyboardButton(text=emoji.emojize(" :back:",use_aliases=True)+u"بازگشت به منوی اصلی", callback_data='return')],])
                bot.sendPhoto(from_id, "https://www.turbogram.co/static/images/homepage/icon-6.8cebe055d143.png", caption="منوی اصلی، لطفا یکی از گزینه های زیر زیر را انتخاب کنید.", reply_markup= keyboard)
                #button for return
                #[ InlineKeyboardButton(text=emoji.emojize(" :back:",use_aliases=True)+u"بازگشت به منوی اصلی", callback_data='return')]

            #Categories
            if query_data==u'categories':
                allcats = CatDA()
                cats=allcats.get_cats()
                cats_keyboard=[]
                for category in cats:
                    cats_keyboard.append([InlineKeyboardButton(text=category.cat_name, callback_data="show_cat "+str(category.id))])

                cats_keyboard.append([ InlineKeyboardButton(text=emoji.emojize(" :back:",use_aliases=True)+u"بازگشت به منوی اصلی", callback_data='return')])
                bot.sendMessage(from_id,"دسته مورد نظر خود را انتخاب کنید: ",reply_markup=InlineKeyboardMarkup(inline_keyboard=cats_keyboard))


            #When a category is selected
            if "show_cat" in query_data:
                temp=query_data.rsplit()
                cat_id=temp[-1]
                customer.set_current(current_word="cat_" + str(cat_id) + "_1")


                product = PDA(cat_id=cat_id, page_number=1)
                products=product.get_product_from_category()
                for item in products:
                    product = PDA(p_id=str(item['id']))
                    #keyboard_1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=str(str(show_product(str(item['id']))['Price'])+" تومان"), callback_data="4"), InlineKeyboardButton(text="افزودن به سبد خرید", callback_data='add_to_cart '+str(item['id']))],[InlineKeyboardButton(text="جزییات بیشتر" ,callback_data=str("Product"+str(show_product(str(item['id']))["product_id"])))],])
                    keyboard_1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                        text=str(str(product.show_product()['Price']) + " تومان") + "💵", callback_data="4"),
                                                                        InlineKeyboardButton(
                                                                            text=u"افزودن به سبد خرید" + emoji.emojize(
                                                                                " :package:", use_aliases=True),
                                                                            callback_data='add_to_cart ' + str(
                                                                                item['id']))], [
                                                                           InlineKeyboardButton(
                                                                               text="جزییات بیشتر" ,
                                                                               callback_data=str("Product" + str(
                                                                                   product.show_product()[
                                                                                       "product_id"])))], ])

                    #bot.sendMessage(chat_id,show_product(str(item['id']))['Name'])
                    caption=u"نام محصول: "+product.show_product()['Name']
                    bot.sendPhoto(from_id,product.show_product()['Image'],caption=caption,reply_markup=keyboard_1)
                if len(products) == 10:
                    keyboard_morenext= InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=emoji.emojize(" :arrow_right:",use_aliases=True)+u"نمایش ۱۰ محصول بعدی" ,callback_data='morenext')], [ InlineKeyboardButton(text=emoji.emojize(" :back:",use_aliases=True)+u"بازگشت به منوی اصلی", callback_data='return')]])
                    bot.sendPhoto(chat_id=from_id, photo="http://lorempixel.com/400/50/", reply_markup=keyboard_morenext)
                    current_word = 'cat_' + str(cat_id) + '_' + str(1 + 1)
                    customer.set_current_cat(current_word=current_word)
                else:
                    customer.set_current_cat(current_word="")
                    keyboard_morenext= InlineKeyboardMarkup(inline_keyboard=[[ InlineKeyboardButton(text=emoji.emojize(" :back:",use_aliases=True)+u"بازگشت به منوی اصلی", callback_data='return')]])
                    bot.sendPhoto(chat_id=from_id, photo="http://lorempixel.com/400/50/", reply_markup=keyboard_morenext)




            #Whene user Press on Sabad_kharid Button
            if query_data ==u'sabad':

                shopping_cart = SHC(c_id=customer_id)
                print shopping_cart
                products = shopping_cart.sabad_from_customer()
                print products
                if products == []:
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[[ InlineKeyboardButton(text=emoji.emojize(" :back:",use_aliases=True)+u"بازگشت به منوی اصلی", callback_data='return')],])
                    bot.sendMessage(from_id,"محصولی در سبد خرید شما موجود نیست" , reply_markup=keyboard)
                else:
                    bot.sendMessage(from_id," سبد خرید شما")
                    total_price = 0
                    sabad_items = u""
                    for product_plus_number in products:
                        product = product_plus_number[0]
                        numnber = product_plus_number[1]
                        name=u'نام محصول: '
                        text=u'توضیحات: '
                        price=u'قیمت: '
                        sabad_items += product.product_name + ":" + str(numnber) + "\n"
                        total_price += product.price

                        caption_name=name+product.product_name+'\n'
                        caption_price=price+str(product.price)+'\n'
                        caption=caption_name+caption_price
                        product_id=product.id
                        keyboard_sabad = InlineKeyboardMarkup(
                            inline_keyboard=[[InlineKeyboardButton(text=u"حذف از سبد خرید"+emoji.emojize(" :x:",use_aliases=True)+"\n"+u"موجود: "+str(numnber), callback_data="del_from_cart "+str(product_id))],[InlineKeyboardButton(text=u"کاستن", callback_data="remove_one_more "+str(product_id)),InlineKeyboardButton(text=u"افزودن", callback_data="add_one_more "+str(product_id))]])

                        bot.sendPhoto(from_id,photo=product.image,caption=caption,reply_markup=keyboard_sabad)
                        # bot.sendMessage(from_id,text=caption_text)
                    keyboard_sabad_end = InlineKeyboardMarkup( inline_keyboard=[[InlineKeyboardButton(text=u"بازگشت به منو", callback_data="return"), InlineKeyboardButton(text=u"خرید محصولات", callback_data='buy')]])
                    bot.sendMessage(from_id, u"اقلام موجود: " + "\n" + sabad_items + str(total_price), reply_markup=keyboard_sabad_end)


            #End Of Sabad_kharid Button

            #When User Click on ten more product
            if query_data == u'morenext':

                try:
                    current = customer.get_current_cat()
                    current_info = current.split("_")
                    current_state = current_info[0]
                    current_page = int(current_info[2])
                except:
                    current = customer.get_current()
                    current_info = current.split("_")
                    current_state = current_info[0]
                    current_page = int(current_info[2])

                if current_state == u'cat':
                    cat_id = str(current_info[1])

                    product = PDA(cat_id=cat_id, page_number=current_page)
                    products=product.get_product_from_category()

                    if len(products) == 0:
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[[ InlineKeyboardButton(text=emoji.emojize(" :back:",use_aliases=True)+u"بازگشت به منوی اصلی", callback_data='return')],])
                        bot.sendMessage(from_id," محصولی موجود نیست" , reply_markup=keyboard)
                    else:
                        for item in products:
                            product = PDA(p_id=str(item['id']))
                            #keyboard_1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=str(str(show_product(str(item['id']))['Price'])+" تومان"), callback_data="4"), InlineKeyboardButton(text="افزودن به سبد خرید", callback_data='add_to_cart '+str(item['id']))],[InlineKeyboardButton(text="جزییات بیشتر" ,callback_data=str("Product"+str(show_product(str(item['id']))["product_id"])))],])
                            keyboard_1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                                text=str(str(product.show_product()['Price']) + " تومان") + "💵", callback_data="4"),
                                                                                InlineKeyboardButton(
                                                                                    text=u"افزودن به سبد خرید" + emoji.emojize(
                                                                                        " :package:", use_aliases=True),
                                                                                    callback_data='add_to_cart ' + str(
                                                                                        item['id']))], [
                                                                                   InlineKeyboardButton(
                                                                                       text="جزییات بیشتر" ,
                                                                                       callback_data=str("Product" + str(
                                                                                           product.show_product()[
                                                                                               "product_id"])))], ])

                            #bot.sendMessage(chat_id,show_product(str(item['id']))['Name'])
                            caption=u"نام محصول: "+product.show_product()['Name']
                            bot.sendPhoto(from_id,product.show_product()['Image'],caption=caption,reply_markup=keyboard_1)

                        if len(products) == 10:
                            keyboard_morenext= InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=emoji.emojize(" :arrow_right:",use_aliases=True)+u"نمایش ۱۰ محصول بعدی" ,callback_data='morenext')], [ InlineKeyboardButton(text=emoji.emojize(" :back:",use_aliases=True)+u"بازگشت به منوی اصلی", callback_data='return')]])
                            bot.sendPhoto(chat_id=from_id, photo="http://lorempixel.com/400/50/", reply_markup=keyboard_morenext)
                            current_word = 'cat_' + str(cat_id) + '_' + str(current_page + 1)
                            customer.set_current_cat(current_word=current_word)
                        else:
                            customer.set_current_cat(current_word="")
                            keyboard_morenext= InlineKeyboardMarkup(inline_keyboard=[[ InlineKeyboardButton(text=emoji.emojize(" :back:",use_aliases=True)+u"بازگشت به منوی اصلی", callback_data='return')]])
                            bot.sendPhoto(chat_id=from_id, photo="http://lorempixel.com/400/50/", reply_markup=keyboard_morenext)


                if u'search' == current_state:
                    current_command = str(current_info[1])
                    print(current_info)
                    search_obj = SDA(search_word=current_command, page_number=current_page)
                    search_results = search_obj.search()
                    for item in search_results:
                        product = PDA(p_id=str(item['id']))
                        #keyboard_1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=str(str(show_product(str(item['id']))['Price'])+" تومان"), callback_data="4"), InlineKeyboardButton(text="افزودن به سبد خرید", callback_data='add_to_cart '+str(item['id']))],[InlineKeyboardButton(text="جزییات بیشتر" ,callback_data=str("Product"+str(show_product(str(item['id']))["product_id"])))],])
                        keyboard_1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                            text=str(str(product.show_product()['Price']) + " تومان") + "💵", callback_data="4"),
                                                                            InlineKeyboardButton(
                                                                                text=u"افزودن به سبد خرید" + emoji.emojize(
                                                                                    " :package:", use_aliases=True),
                                                                                callback_data='add_to_cart ' + str(
                                                                                    item['id']))], [
                                                                               InlineKeyboardButton(
                                                                                   text="جزییات بیشتر" ,
                                                                                   callback_data=str("Product" + str(
                                                                                       product.show_product()[
                                                                                           "product_id"])))], ])

                        #bot.sendMessage(chat_id,show_product(str(item['id']))['Name'])
                        caption=u"نام محصول: "+product.show_product()['Name']
                        bot.sendPhoto(from_id,product.show_product()['Image'],caption=caption,reply_markup=keyboard_1)

                    if len(search_results) == 10:
                        keyboard_morenext= InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=emoji.emojize(" :arrow_right:",use_aliases=True)+u"نمایش ۱۰ محصول بعدی" ,callback_data='morenext')], [ InlineKeyboardButton(text=emoji.emojize(" :back:",use_aliases=True)+u"بازگشت به منوی اصلی", callback_data='return')]])
                        bot.sendPhoto(chat_id=from_id, photo="http://lorempixel.com/400/50/", reply_markup=keyboard_morenext)
                        current_word = 'search_' + current_command + '_' + str(current_page + 1)
                        customer.set_current(current_word=current_word)
                    else:
                        keyboard_morenext= InlineKeyboardMarkup(inline_keyboard=[[ InlineKeyboardButton(text=emoji.emojize(" :back:",use_aliases=True)+u"بازگشت به منوی اصلی", callback_data='return')]])
                        bot.sendPhoto(chat_id=from_id, photo="http://lorempixel.com/400/50/", reply_markup=keyboard_morenext)






            #End of When User Click on ten more product

            if query_data == u'4':
                notification = "برای خرید این محصول بر روی افزودن به سبد خرید کلیک کنید"
                bot.answerCallbackQuery(query_id, text=notification)

            for id in models.Product.objects.values('id'):
                product=PDA(p_id=str((id['id'])))
                like_counts=product.get_likes()
                dislike_counts=product.get_dislikes()
                models.Like_dislike.objects.filter(p_id=str((id['id']))).count()

                keyboard_1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=str(str(models.Product.objects.filter(pk=id['id']).values('price')[0]['price'])+" تومان")+"💵", callback_data="4"), InlineKeyboardButton(text=u"افزودن به سبد خرید"+emoji.emojize(" :package:",use_aliases=True), callback_data='add_to_cart '+str(id['id']))],[InlineKeyboardButton(text="👍"+str(like_counts), callback_data='do_like '+str(id['id'])),InlineKeyboardButton(text="👎"+str(dislike_counts), callback_data='do_dislike '+str(id['id']))], [InlineKeyboardButton(text = "ثبت نظر" , callback_data=str("User_comment")+ str(id['id'])) , InlineKeyboardButton(text = "مشاهده نظرات" , callback_data = "Show_comment" + str(id['id']))]])

                if query_data == str("Product" + str((id['id']))):
                    #bot.sendMessage(from_id , models.Product.objects.filter(pk=id['id']).values('product_name')[0]['product_name'])
                    caption= u"نام محصول: " +models.Product.objects.filter(pk=id['id']).values('product_name')[0]['product_name']
                    bot.sendPhoto(from_id , models.Product.objects.filter(pk=id['id']).values('image')[0]['image'],caption=caption)
                    bot.sendMessage(from_id,u"توضیحات: " +models.Product.objects.filter(pk=id['id']).values('text')[0]['text'],reply_markup=keyboard_1)
                if query_data == str("User_comment" + str((id['id']))):
                    print('222')
                    if customer.set_state(state_word=str('User_comment' + str(id['id']))):
                        notification="نظر خود را درمورد این محضول بنویسید"
                        bot.answerCallbackQuery(query_id, text=notification)
                if query_data == str("Show_comment" + str(id['id'])):
                    comments = models.Product_comment.objects.filter(product_id = id['id'])
                    print(list(comments))
                    if list(comments) == []:
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[[ InlineKeyboardButton(text=emoji.emojize(" :back:",use_aliases=True)+u"بازگشت به منوی اصلی", callback_data='return')],])
                        bot.sendMessage(from_id," نظری برای این محصول موجود نیست" , reply_markup=keyboard)
                    else:
                        for comment in comments:
                            bot.sendMessage(from_id, comment.text_comment)

            if "do_like" in query_data:
                query = query_data.rsplit()
                product_id = query[-1]
                product = PDA(t_id=from_id,p_id=product_id)
                flag = product.like()
                if flag:
                    notification="like done"
                    bot.answerCallbackQuery(query_id, text=notification)
                else:
                    notification="like deleted"
                    bot.answerCallbackQuery(query_id, text=notification)

                product = PDA(p_id=product_id)
                like_counts = product.get_likes()
                dislike_counts = product.get_dislikes()
                models.Like_dislike.objects.filter(p_id=str((product_id))).count()
                identifier = msg["message"]
                keyboard_2 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=str(str(models.Product.objects.filter(pk=id['id']).values('price')[0]['price'])+" تومان")+"💵", callback_data="4"), InlineKeyboardButton(text=u"افزودن به سبد خرید"+emoji.emojize(" :package:",use_aliases=True), callback_data='add_to_cart '+str(id['id']))],[InlineKeyboardButton(text="👍"+str(like_counts), callback_data='do_like '+str(id['id'])),InlineKeyboardButton(text="👎"+str(dislike_counts), callback_data='do_dislike '+str(id['id']))], [InlineKeyboardButton(text = "ثبت نظر" , callback_data=str("User_comment")+ str(id['id'])) , InlineKeyboardButton(text = "مشاهده نظرات" , callback_data = "Show_comment" + str(id['id']))]])
                msg_identifier = telepot.message_identifier(identifier)
                telepot.Bot.editMessageReplyMarkup(bot, msg_identifier=msg_identifier, reply_markup=keyboard_2)

            if "do_dislike" in query_data:
                query=query_data.rsplit()
                product_id=query[-1]
                product = PDA(t_id=from_id,p_id=product_id)
                flag=product.dislike()
                if(flag):
                    notification="dislike done"
                    bot.answerCallbackQuery(query_id, text=notification)
                else:
                    notification="dislike deleted"
                    bot.answerCallbackQuery(query_id, text=notification)

                if "do_dislike" in query_data:
                    query = query_data.rsplit()
                    product_id = query[-1]
                    product = PDA(t_id=from_id, p_id=product_id)
                    flag = product.dislike()
                    if (flag):
                        notification = "dislike done"
                        bot.answerCallbackQuery(query_id, text=notification)
                    else:
                        notification = "dislike deleted"
                        bot.answerCallbackQuery(query_id, text=notification)

                product=PDA(p_id=product_id)
                like_counts=product.get_likes()
                dislike_counts=product.get_dislikes()
                models.Like_dislike.objects.filter(p_id=str((product_id))).count()
                identifier = msg["message"]
                keyboard_2 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=str(str(models.Product.objects.filter(pk=id['id']).values('price')[0]['price'])+" تومان")+"💵", callback_data="4"), InlineKeyboardButton(text=u"افزودن به سبد خرید"+emoji.emojize(" :package:",use_aliases=True), callback_data='add_to_cart '+str(id['id']))],[InlineKeyboardButton(text="👍"+str(like_counts), callback_data='do_like '+str(id['id'])),InlineKeyboardButton(text="👎"+str(dislike_counts), callback_data='do_dislike '+str(id['id']))], [InlineKeyboardButton(text = "ثبت نظر" , callback_data=str("User_comment")+ str(id['id'])) , InlineKeyboardButton(text = "مشاهده نظرات" , callback_data = "Show_comment" + str(id['id']))]])
                msg_identifier=telepot.message_identifier(identifier)
                telepot.Bot.editMessageReplyMarkup(bot,msg_identifier=msg_identifier,reply_markup=keyboard_2)

            if "add_to_cart" in query_data:
                query = query_data.rsplit()
                product_id = query[-1]
                shopping_cart = SHC(c_id=customer_id, p_id=product_id)
                flag = shopping_cart.add_to_cart()
                if flag:
                    notification = "محصول با موفقیت به سبد خرید شما اضافه شد"
                    bot.answerCallbackQuery(query_id, text=notification)
                else:
                    notification = "این محصول در سبد خرید شما وجود دارد"
                    bot.answerCallbackQuery(query_id, text=notification)

            if "del_from_cart" in query_data:
                query = query_data.rsplit()
                product_id = query[-1]
                shopping_cart = SHC(c_id=customer_id, p_id=product_id)
                flag = shopping_cart.del_from_cart()
                if(flag):
                    notification="محصول با موفقیت از سبد خرید حذف شد"
                    bot.answerCallbackQuery(query_id, text=notification)
                    identifier = msg["message"]
                    msg_identifier=telepot.message_identifier(identifier)
                    telepot.Bot.deleteMessage(bot, msg_identifier=msg_identifier)


                else:
                    notification="این محصول در سبد شما وجود ندارد"
                    bot.answerCallbackQuery(query_id, text=notification)

            if "add_one_more" in query_data:
                query=query_data.rsplit()
                print "query is: "
                print query
                product_id = query[-1]
                shopping_cart = SHC(c_id=customer_id, p_id=product_id)
                flag = shopping_cart.add_remove(1)
                if flag:
                    notification = "به تعداد محصول شما افزوده شد"
                    bot.answerCallbackQuery(query_id, text=notification)
                    cart = SHC(c_id=customer_id, p_id=product_id)
                    cart_object = cart.get_object()
                    identifier = msg["message"]
                    keyboard_3 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=u"حذف از سبد خرید"+emoji.emojize(" :x:",use_aliases=True)+"\n"+u"موجود: "+str(cart_object.number), callback_data="del_from_cart "+str(cart_object.p_id_id))],[InlineKeyboardButton(text=u"کاستن", callback_data="remove_one_more "+str(cart_object.p_id_id)),InlineKeyboardButton(text=u"افزودن", callback_data="add_one_more "+str(cart_object.p_id_id))]])
                    msg_identifier=telepot.message_identifier(identifier)
                    telepot.Bot.editMessageReplyMarkup(bot,msg_identifier=msg_identifier,reply_markup=keyboard_3)
                else:
                    notification = "انجام عملیات مقدور نبود"
                    bot.answerCallbackQuery(query_id, text=notification)


            if "remove_one_more" in query_data:
                query=query_data.rsplit()
                product_id = query[-1]
                shopping_cart = SHC(c_id=customer_id, p_id=product_id)
                flag = shopping_cart.add_remove(-1)
                if flag:
                    notification = "از تعداد محصول شما کاسته شد"
                    bot.answerCallbackQuery(query_id, text=notification)
                    cart=SHC(c_id=customer_id,p_id=product_id)
                    cart_object=cart.get_object()
                    identifier = msg["message"]
                    keyboard_3 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=u"حذف از سبد خرید"+emoji.emojize(" :x:",use_aliases=True)+"\n"+u"موجود: "+str(cart_object.number), callback_data="del_from_cart "+str(cart_object.p_id_id))],[InlineKeyboardButton(text=u"کاستن", callback_data="remove_one_more "+str(cart_object.p_id_id)),InlineKeyboardButton(text=u"افزودن", callback_data="add_one_more "+str(cart_object.p_id_id))]])
                    msg_identifier=telepot.message_identifier(identifier)
                    telepot.Bot.editMessageReplyMarkup(bot,msg_identifier=msg_identifier,reply_markup=keyboard_3)
                else:
                    notification = "انجام عملیات مقدور نبود"
                    bot.answerCallbackQuery(query_id, text=notification)

            #When you click on buy
            if query_data == 'buy':
                shopping_cart = SHC(c_id=customer_id)
                customer.set_state("buy_comment")
                bot.sendMessage(from_id, "لطفا توضیحات محصول را وارد کنید.")






            if query_data == u"enteghadstart":
                allcats = CatDA()
                cat_keyboard = allcats.feed_back_cat_keyboard()
                bot.sendMessage(from_id, " یک گزینه را انتخاب کنید " ,reply_markup=cat_keyboard)

            if u"naghd" in query_data:
                cat_id = query_data.replace("naghd", "")
                customer.set_state(state_word="naghd" + cat_id)
                bot.sendMessage(from_id, "لطفا نظر خود را وارد کنید.")




        def send_base_product_info(from_id,product):
            caption=u"نام محصول: "+product.product_name
            image=product.image
            keyboard=[[ InlineKeyboardButton(text=str(product.price)+u" تومان"+emoji.emojize(" :dollar:",use_aliases=True), callback_data="4"),InlineKeyboardButton(text=u"افزودن به سبد خرید"+emoji.emojize(" :package:",use_aliases=True), callback_data='add_to_cart '+str(product.id))],[InlineKeyboardButton(text=u"جزییات بیشتر"+emoji.emojize(" :clipboard:",use_aliases=True) ,callback_data=str("Product"+str(product.id)))],]
            try:
                bot.sendPhoto(from_id,photo=image,caption=caption,reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
                return True
            except  Exception :
                print Exception
                return False






        token = '305910807:AAHG7PRJ767S6sMv_4CPpmFeI17Pe5kFbEs'

        bot = telepot.Bot(token)
        bot.message_loop({'chat': on_chat_message, 'callback_query': on_callback_query})
        print('Listening ...')

        while 1:
            time.sleep(10)




