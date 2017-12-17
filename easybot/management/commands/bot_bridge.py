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
from AdvanceSearch import AdvanceSearchDataAccess as ASDA
from Shopping_Card import ShoppingCard as SHC
from SurveyDataAccess import SurveyDataAccess as SDA
from AnswerHandler import AnswerHandler as AH
from Order import Order
from Advertise import Advertise
from ... import models

admin_id = 116016698
admin_buffer = {}


class Command(BaseCommand):
    help = 'for running bot execution'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        def on_chat_message(msg):

            # Get User data From User RealTime
            print msg
            try:
                username = msg['from']['username']
                user_id = msg['from']['id']
            except:
                username = "Null"
                user_id = 0
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

            if type(customer.return_user_state()) != None:
                user_state = customer.return_user_state()
                print "state: " + unicode(user_state)
            else:
                user_state = "Null"
                print "state: " + unicode(user_state)

            # End Of Get Data From User


            if user_id == admin_id:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text=emoji.emojize(":mag_right:", use_aliases=True) + u"اضافه کردن تبلیغ",
                                          callback_data="add_advertise"), InlineKeyboardButton(
                        text=emoji.emojize(":mag_right:", use_aliases=True) + u"اضافه کردن محصول",
                        callback_data="add_product")],
                    [InlineKeyboardButton(text=emoji.emojize(" :package:",
                                                             use_aliases=True) + u"مشاهده نظرات",
                                          callback_data='0'),
                     InlineKeyboardButton(text=emoji.emojize(" :postbox:",
                                                             use_aliases=True) + u"مشاهده سفارشات",
                                          callback_data='0')],
                    [InlineKeyboardButton(text=emoji.emojize(":mag_right:",
                                                             use_aliases=True) + u"ارسال دستی تبلیغ",
                                          callback_data='manual_advertise')],
                    [InlineKeyboardButton(text=emoji.emojize(" :memo:",
                                                             use_aliases=True) + u"مشاهده دسته بندی محصولات",
                                          callback_data='0')],
                    [InlineKeyboardButton(text=emoji.emojize(" :back:",
                                                             use_aliases=True) + u"بازگشت به منوی اصلی",
                                          callback_data='return')], ])
            else:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                    text=emoji.emojize(":mag_right:", use_aliases=True) + u"دسته بندی ها", callback_data="categories"),
                    InlineKeyboardButton(text=emoji.emojize(":mag_right:",
                                                            use_aliases=True) + u"جستجو",
                                         callback_data="search")], [
                    InlineKeyboardButton(
                        text=emoji.emojize(" :package:",
                                           use_aliases=True) + u"سبد خرید",
                        callback_data='sabad'), InlineKeyboardButton(
                        text=emoji.emojize(" :postbox:", use_aliases=True) + u"انتقاد و پیشنهاد",
                        callback_data='enteghadstart')], [InlineKeyboardButton(
                    text=emoji.emojize(":mag_right:", use_aliases=True) + u"جستجوی پیشرفته",
                    callback_data='advance_search')], [InlineKeyboardButton(text=emoji.emojize(":mag_right:",
                                                                                               use_aliases=True) + u"نظرسنجی‌ها",
                                                                            callback_data='show_surveys')], [
                    InlineKeyboardButton(text=emoji.emojize(" :memo:",
                                                            use_aliases=True) + u"وارد کردن اطلاعات شخصی برای خرید",
                                         callback_data='enterinfo_firstname')],
                    [InlineKeyboardButton(text=emoji.emojize(" :back:",
                                                             use_aliases=True) + u"بازگشت به منوی اصلی",
                                          callback_data='return')], ])
            if command == '/start':

                for i in range(1, 4):
                    try:
                        q = models.Sabad_Kharid(cus_id=customer, p_id_id=int(i))
                        q.save()
                    except:
                        pass
                # Add User if thechat_id from user not in Database
                if not customer.check_customer_is():
                    customer.add_customer(username)
                    bot.sendPhoto(chat_id, "http://www.byronbible.org/wp-content/uploads/2013/07/Welcome-1024x576.jpg",
                                  caption="به بات گرام خوش آمدید، لطفا یکی از گزینه های زیر زیر را انتخاب کنید.",
                                  reply_markup=keyboard)
                else:
                    bot.sendPhoto(chat_id, "http://www.byronbible.org/wp-content/uploads/2013/07/Welcome-1024x576.jpg",
                                  caption="به بات گرام خوش آمدید، لطفا یکی از گزینه های زیر زیر را انتخاب کنید.",
                                  reply_markup=keyboard)

                    # End Of Add User if not exist




            elif content_type == 'text' and user_state == 'search':
                search_obj = SDA(search_word=command, page_number=1)
                search_results = search_obj.search()
                print list(search_results)
                if list(search_results) == []:
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                        text=emoji.emojize(":mag_right:", use_aliases=True) + u"جستجو", callback_data="search")], [
                        InlineKeyboardButton(
                            text=emoji.emojize(" :back:",
                                               use_aliases=True) + ' ' + u"بازگشت به منوی اصلی",
                            callback_data='return')]])
                    bot.sendMessage(chat_id, "نتیجه ای یافت نشد", reply_markup=keyboard)
                    customer.unset_state()

                else:
                    for item in search_results:
                        product = PDA(p_id=str(item['id']))
                        keyboard_1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                            text=str(str(product.show_product()['Price']) + " تومان") + "💵", callback_data="4"),
                            InlineKeyboardButton(
                                text=u"افزودن به سبد خرید" + emoji.emojize(
                                    " :package:", use_aliases=True),
                                callback_data='add_to_cart ' + str(
                                    item['id']))], [
                            InlineKeyboardButton(
                                text=u"جزییات بیشتر" + emoji.emojize(
                                    " :clipboard:",
                                    use_aliases=True),
                                callback_data=str("Product" + str(
                                    product.show_product()[
                                        "product_id"])))], ])
                        # bot.sendMessage(chat_id,show_product(str(item['id']))['Name'])
                        caption = u"نام محصول: " + product.show_product()['Name']
                        bot.sendPhoto(chat_id, product.show_product()['Image'], caption=caption,
                                      reply_markup=keyboard_1)
                    keyboard_morenext = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                        text=emoji.emojize(" :arrow_right:", use_aliases=True) + " " + u"نمایش ۱۰ محصول بعدی",
                        callback_data='morenext')], [InlineKeyboardButton(
                        text=emoji.emojize(" :back:", use_aliases=True) + "  " + u"بازگشت به منوی اصلی",
                        callback_data='return')]])
                    bot.sendMessage(chat_id, "  نتیجه جستجوی شما  ", reply_markup=keyboard_morenext)
                    customer.set_current(current_word='search_' + command + '_1')
                    customer.unset_state()

                    # When going to AdvanceSearch after entering search word
            elif content_type == 'text' and 'advance_search' in user_state:
                # print unicode(user_state)
                # search_obj = ASDA(search_word=command)
                # search_results = search_obj.search()
                # print list(search_results)
                # if list(search_results) == []:
                if (user_state.split("_")[0] == "s"):
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                        text=emoji.emojize(":mag_right:", use_aliases=True) + u"جستجوی همه",
                        callback_data="search_all")], [InlineKeyboardButton(
                        text=emoji.emojize(":mag_right:", use_aliases=True) + u"جستجوی موجودها",
                        callback_data="search_avalable")], [InlineKeyboardButton(
                        text=emoji.emojize(":mag_right:", use_aliases=True) + u"انتخاب کلمه",
                        callback_data="advance_search")], [InlineKeyboardButton(
                        text=emoji.emojize(":mag_right:", use_aliases=True) + u"کف قیمت", callback_data="low_price")], [
                        InlineKeyboardButton(
                            text=emoji.emojize(":mag_right:",
                                               use_aliases=True) + u"سقف قیمت",
                            callback_data="high_price")], [
                        InlineKeyboardButton(
                            text=emoji.emojize(" :back:",
                                               use_aliases=True) + ' ' + u"بازگشت به منوی اصلی",
                            callback_data='return')]])
                    message_dict = get_AdvanceSearchOptions(user_state)
                    message_dict["word"] = command
                    bot.sendMessage(chat_id, u"جستجوی: " + message_dict.get("word",
                                                                            u"تعیین نشده") + "\n" + u"کف قیمت: " + message_dict.get(
                        "low_price", u"تعیین نشده") + "\n" + u"سقف قیمت: " + message_dict.get("high_price",
                                                                                              u"تعیین نشده"),
                                    reply_markup=keyboard)
                    customer.unset_state()
                    next_str = ""
                    for item in user_state.split(",")[2:]:
                        next_str += item + ","
                    next_str = next_str[:-1]
                    customer.set_state(user_state.split(",")[0] + "," + command + "," + next_str)
                elif (user_state.split("_")[0] == "lgh"):
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                        text=emoji.emojize(":mag_right:", use_aliases=True) + u"جستجوی همه",
                        callback_data="search_all")], [InlineKeyboardButton(
                        text=emoji.emojize(":mag_right:", use_aliases=True) + u"جستجوی موجودها",
                        callback_data="search_avalable")], [InlineKeyboardButton(
                        text=emoji.emojize(":mag_right:", use_aliases=True) + u"انتخاب کلمه",
                        callback_data="advance_search")], [InlineKeyboardButton(
                        text=emoji.emojize(":mag_right:", use_aliases=True) + u"کف قیمت", callback_data="low_price")], [
                        InlineKeyboardButton(
                            text=emoji.emojize(":mag_right:",
                                               use_aliases=True) + u"سقف قیمت",
                            callback_data="high_price")], [
                        InlineKeyboardButton(
                            text=emoji.emojize(" :back:",
                                               use_aliases=True) + ' ' + u"بازگشت به منوی اصلی",
                            callback_data='return')]])
                    message_dict = get_AdvanceSearchOptions(user_state)
                    message_dict["low_price"] = command
                    bot.sendMessage(chat_id, u"جستجوی: " + message_dict.get("word",
                                                                            u"تعیین نشده") + "\n" + u"کف قیمت: " + message_dict.get(
                        "low_price", u"تعیین نشده") + "\n" + u"سقف قیمت: " + message_dict.get("high_price",
                                                                                              u"تعیین نشده"),
                                    reply_markup=keyboard)
                    customer.unset_state()
                    next_str = ""
                    for item in user_state.split(",")[3:]:
                        next_str += item + ","
                    next_str = next_str[:-1]
                    pre_str = ""
                    for item in user_state.split(",")[:2]:
                        pre_str += item + ","
                    pre_str = pre_str[:-1]
                    customer.set_state(pre_str + "," + command + "," + next_str)
                elif (user_state.split("_")[0] == "hgh"):
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                        text=emoji.emojize(":mag_right:", use_aliases=True) + u"جستجوی همه",
                        callback_data="search_all")], [InlineKeyboardButton(
                        text=emoji.emojize(":mag_right:", use_aliases=True) + u"جستجوی موجودها",
                        callback_data="search_avalable")], [InlineKeyboardButton(
                        text=emoji.emojize(":mag_right:", use_aliases=True) + u"انتخاب کلمه",
                        callback_data="advance_search")], [InlineKeyboardButton(
                        text=emoji.emojize(":mag_right:", use_aliases=True) + u"کف قیمت", callback_data="low_price")], [
                        InlineKeyboardButton(
                            text=emoji.emojize(":mag_right:",
                                               use_aliases=True) + u"سقف قیمت",
                            callback_data="high_price")], [
                        InlineKeyboardButton(
                            text=emoji.emojize(" :back:",
                                               use_aliases=True) + ' ' + u"بازگشت به منوی اصلی",
                            callback_data='return')]])
                    message_dict = get_AdvanceSearchOptions(user_state)
                    message_dict["high_price"] = command
                    bot.sendMessage(chat_id, u"جستجوی: " + message_dict.get("word",
                                                                            u"تعیین نشده") + "\n" + u"کف قیمت: " + message_dict.get(
                        "low_price", u"تعیین نشده") + "\n" + u"سقف قیمت: " + message_dict.get("high_price",
                                                                                              u"تعیین نشده"),
                                    reply_markup=keyboard)
                    customer.unset_state()
                    next_str = ""
                    for item in user_state.split(",")[4:]:
                        next_str += item + ","
                    next_str = next_str[:-1]
                    pre_str = ""
                    for item in user_state.split(",")[:3]:
                        pre_str += item + ","
                    pre_str = pre_str[:-1]
                    customer.set_state(pre_str + "," + command + "," + next_str)



                    # else :
                    #     for item in search_results:
                    #         product = PDA(p_id=str(item['id']))
                    #         keyboard_1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=str(str(product.show_product()['Price'])+" تومان")+"💵", callback_data="4"), InlineKeyboardButton(text=u"افزودن به سبد خرید"+emoji.emojize(" :package:",use_aliases=True), callback_data='add_to_cart '+str(item['id']))] ,[InlineKeyboardButton(text=u"جزییات بیشتر"+emoji.emojize(" :clipboard:",use_aliases=True) ,callback_data=str("Product"+str(product.show_product()["product_id"])))],])
                    #         #bot.sendMessage(chat_id,show_product(str(item['id']))['Name'])
                    #         caption=u"نام محصول: "+product.show_product()['Name']
                    #         bot.sendPhoto(chat_id,product.show_product()['Image'],caption=caption,reply_markup=keyboard_1)
                    #     keyboard_morenext= InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=emoji.emojize( " :arrow_right:",use_aliases=True)+ " " + u"نمایش ۱۰ محصول بعدی" ,callback_data='morenext')],[InlineKeyboardButton(text=emoji.emojize(" :back:",use_aliases=True)+ "  " + u"بازگشت به منوی اصلی", callback_data='return')]])
                    #     bot.sendMessage(chat_id,"  نتیجه جستجوی شما  ", reply_markup=keyboard_morenext)
                    #     customer.set_current(current_word='search_' + command + '_1')
                    #     customer.unset_state()
                    # End
            elif content_type == 'text' and user_state == 'enterinfo_firstname':
                customer.enter_first_name(f_name=command)
                customer.set_state(state_word='enterinfo_lastname')
                bot.sendMessage(chat_id, "نام خانوادگی خود را وارد کنید.")

            elif content_type == 'text' and user_state == 'enterinfo_lastname':
                customer.enter_last_name(l_name=command)
                customer.set_state(state_word='enterinfo_email')
                bot.sendMessage(chat_id, "ایمیل خود را وارد کنید")

            elif content_type == 'text' and user_state == 'enterinfo_email':
                customer.enter_email(email=command)
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
                bot.sendMessage(chat_id=chat_id, text="دکمه اشتراک شماره تلفن نمایش داده خواهد شد.",
                                reply_markup=reply_markup)

            elif (content_type == 'text' or content_type == 'contact') and user_state == 'enterinfo_phone':
                if content_type == "contact":
                    customer.enter_phone(phone=command)
                    customer.unset_state()
                    bot.sendMessage(chat_id, "اطلاعات شما  با موفقیت ثبت شد.")
                else:
                    bot.sendMessage(chat_id=chat_id, text="لطفا بر روی دکمه فرستادن شماره تلفن به ربات کلیک کنید")



            elif content_type == 'text' and 'naghd' in user_state:
                naghd_cat = int(user_state.replace("naghd", ""))
                comment_obj = com_DA(t_id=chat_id, new_comment=command, cat_id=naghd_cat)
                if comment_obj.enter_comment():
                    notification = "نظر با موفقیت ثبت شد. با تشکر از شما"
                    bot.sendMessage(chat_id, text=notification)
                    customer.unset_state()
                else:
                    notification = "لطفا مجددا نظر را وارد نمایید."
                    bot.sendMessage(chat_id, text=notification)


            elif content_type == 'text' and "User_comment" in user_state:
                comment_obj = com_DA(t_id=customer.return_customer_id(), p_id=user_state[12:], new_comment=command)
                if comment_obj.enter_user_comment():
                    notification = "نظر با موفقیت ثبت شد. با تشکر از شما"
                    bot.sendMessage(chat_id, text=notification)
                    customer.unset_state()
                else:
                    notification = "لططفا مجددا نظر را وارد نمایید."
                    bot.sendMessage(chat_id, text=notification)
                    # end buying by getting comment
            elif content_type == 'text' and user_state == 'buy_comment':
                sabad = SHC(c_id=customer_id)
                sabad_products = sabad.sabad_from_customer()
                order = Order(c_id=customer_id, order_time=time.time(), info=command)
                process_card = order.add_card_to_order()
                is_order_done = process_card[0]
                order_id = process_card[1]
                print "Ohh"
                print sabad.sabad_from_customer_objects()
                print order_id
                order_to_products = Order(products=sabad.sabad_from_customer_objects(), order_id=order_id)
                order_to_products.add_products_to_order()
                for product in sabad_products:
                    sabad_product = SHC(c_id=customer_id, p_id=product[0])
                    sabad_product.del_from_cart()
                if is_order_done:
                    customer.unset_state()
                    bot.sendMessage(chat_id, "خرید با موفقیت انجام شد")
                else:
                    bot.sendMessage(chat_id, "مشکلی بوجود آمده")
                    # ADMIN PANEL messages
            if (user_id == admin_id):
                if content_type == 'text' and 'advertise' in user_state:
                    if 'title' in user_state:
                        admin_buffer['title'] = command
                        customer.set_state("advertise_description")
                        bot.sendMessage(chat_id, "توضیحات محصول را وارد کنید")
                    elif 'description' in user_state:
                        admin_buffer['description'] = command
                        customer.set_state('advertise_image')
                        bot.sendMessage(chat_id, "لینک تصویر تبلیغ را وارد کنید")
                    elif 'image' in user_state:
                        admin_buffer['image'] = command
                        customer.set_state("advertise_repeat")
                        bot.sendMessage(chat_id, "تعداد تکرار تبلیغ را وارد کنید")
                    elif 'repeat' in user_state:
                        admin_buffer['repeat'] = command
                        ad = Advertise()
                        if ad.add_advertise(admin_buffer):
                            customer.unset_state()
                            bot.sendMessage(chat_id, "تبلیغ با موفقیت ذخیره شد.")
                            admin_buffer.clear()
                        else:
                            customer.unset_state()
                            bot.sendMessage(chat_id, "مشکلی بوجود آمد")
                            admin_buffer.clear()

            elif content_type == "text" and "answer" in user_state:
                survey_data_from_state = user_state.split("@")
                survey_id = survey_data_from_state[1]
                question_order = survey_data_from_state[2]
                print "answer is: " + command + "from this q order: " + str(
                    int(question_order) - 1) + " question_id is: " + str(survey_data_from_state[3])
                answer_object = AH(question_id=survey_data_from_state[3], question_answer=command)
                answer_object.add_answer()
                survey_object = SDA(survey_id=survey_id)
                question = survey_object.get_question_data(question_order=question_order)
                if question == 0:
                    bot.sendMessage(chat_id=chat_id, text="با تشکر پاسخ‌های شما با موفقیت ثبت شد.")
                else:
                    bot.sendMessage(chat_id=chat_id, text=question.text)
                if int(question_order) > survey_object.get_number_of_questions():
                    customer.unset_state()
                else:
                    customer.set_state(
                        "answer@" + str(survey_id) + "@" + str(int(question_order) + 1) + "@" + str(question.pk))

        def on_callback_query(msg):
            # Get User Query Data
            query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
            customer = CDA(from_id)
            customer_id = customer.return_customer_id()
            customer_sabad = SHC(c_id=customer_id)
            max_cart = customer_sabad.number_items_in_cart()
            command = msg
            # ENd of getting Query Data from user

            # ADMIN PANEL
            if from_id == admin_id:

                # when press on manual advertise
                if query_data == u"manual_advertise":
                    ad = Advertise(0)
                    advertises = ad.getAllAdvertises()
                    for advertise in advertises:
                        image = advertise.image
                        print image
                        try:
                            keyboard_1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                                text=u"ارسال", callback_data="send_ad " + str(advertise.id))]])
                            bot.sendPhoto(chat_id=admin_id,
                                          photo=str(image),
                                          caption=advertise.title + "\n" + advertise.text, reply_markup=keyboard_1)
                        except Exception as e:
                            print e
                            print "failed sending advertise"
                # End of press on manual advertise

                # When sending an advertise
                if u'send_ad' in query_data:
                    ad = Advertise()
                    advertise = ad.getAdvertise(query_data.rsplit()[1])
                    customers = ad.getAllCustomers()
                    for customer in customers:
                        image = advertise.image
                        print image
                        try:
                            bot.sendPhoto(chat_id=customer.telegram_id,
                                          photo=str(image),
                                          caption=advertise.title + "\n" + advertise.text)
                        except Exception as e:
                            print e
                            print "failed sending advertise"

                # End of sending an advertise


                # when press on add advertise
                if query_data == u"add_advertise":
                    if customer.set_state("advertise_title"):
                        bot.answerCallbackQuery(query_id, text="عنوان تبلیغ را وارد کنید")
                # end of add advertise

                # when press on add product
                # if query_data == u"add_product":
                #     if customer
                # End of add product

            # End of ADMIN PANEL
            # Whene user Press on Search Button
            if query_data == u"search":
                if customer.set_state(state_word='search'):
                    bot.answerCallbackQuery(query_id, text="نام محصول را وارد کنید", show_alert=True)
            # End Of Search Button

            # When user Press on AdvanceSearch Button
            if query_data == u"advance_search":
                customer = CDA(from_id)
                user_state = customer.return_user_state()
                print user_state
                if "advance_search" in user_state:
                    bot.answerCallbackQuery(query_id, text="نام محصول را وارد کنید", show_alert=True)
                    next_str = ""
                    for item in user_state.split(",")[1:]:
                        next_str += item + ","
                    next_str = next_str[:-1]
                    customer.set_state("s_advance_search," + next_str)

                else:
                    customer.set_state(state_word='s_advance_search,¢,0,999999999,0')
                    bot.answerCallbackQuery(query_id, text="نام محصول را وارد کنید", show_alert=True)
            # End Of AdvanceSearch Button

            # When user press on low_price button
            if query_data == u"low_price":
                customer = CDA(from_id)
                user_state = customer.return_user_state()
                print user_state
                next_str = ""
                for item in user_state.split(",")[1:]:
                    next_str += item + ","
                next_str = next_str[:-1]
                customer.set_state("lgh_advance_search," + next_str)
                print customer.return_user_state()

                # customer.set_state(state_word='lgh_advance_search,¢,0,999999999,0')
                bot.answerCallbackQuery(query_id, text="کف قیمت محصول را وارد کنید", show_alert=True)

            # End of low price button

            # When user press on high_price button
            if query_data == u"high_price":
                customer = CDA(from_id)
                user_state = customer.return_user_state()
                print user_state
                next_str = ""
                for item in user_state.split(",")[1:]:
                    next_str += item + ","
                next_str = next_str[:-1]
                customer.set_state("hgh_advance_search," + next_str)
                print customer.return_user_state()

                # customer.set_state(state_word='lgh_advance_search,¢,0,999999999,0')
                bot.answerCallbackQuery(query_id, text="سقف قیمت محصول را وارد کنید", show_alert=True)
            # End of high price button

            # When user press on search all button
            if query_data == u"search_all":
                print "search_allllll"
                customer = CDA(from_id)
                user_state = customer.return_user_state()
                advance_search_dict = get_AdvanceSearchOptions(user_state)
                advance_search_obj = ASDA(advance_search_dict.get("word"), advance_search_dict.get("low_price", 0),
                                          advance_search_dict.get("high_price", 999999999))
                customer.unset_state()
                search_results = advance_search_obj.searchAll()
                for item in search_results:
                    product = PDA(p_id=str(item['id']))
                    # keyboard_1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=str(str(show_product(str(item['id']))['Price'])+" تومان"), callback_data="4"), InlineKeyboardButton(text="افزودن به سبد خرید", callback_data='add_to_cart '+str(item['id']))],[InlineKeyboardButton(text="جزییات بیشتر" ,callback_data=str("Product"+str(show_product(str(item['id']))["product_id"])))],])
                    keyboard_1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                        text=str(str(product.show_product()['Price']) + " تومان") + "💵", callback_data="4"),
                        InlineKeyboardButton(
                            text=u"افزودن به سبد خرید" + emoji.emojize(
                                " :package:", use_aliases=True),
                            callback_data='add_to_cart ' + str(
                                item['id']))], [
                        InlineKeyboardButton(
                            text="جزییات بیشتر",
                            callback_data=str("Product" + str(
                                product.show_product()[
                                    "product_id"])))], ])

                    # bot.sendMessage(chat_id,show_product(str(item['id']))['Name'])
                    caption = u"نام محصول: " + product.show_product()['Name']
                    bot.sendPhoto(from_id, product.show_product()['Image'], caption=caption, reply_markup=keyboard_1)
                if len(search_results) == 0:
                    bot.sendMessage(from_id, u"متاسفانه محصولی با این مشخصات یافت نشد")
                print "search_allllll_done"
            if query_data == u"search_avalable":
                print "search_allllll"
                customer = CDA(from_id)
                user_state = customer.return_user_state()
                advance_search_dict = get_AdvanceSearchOptions(user_state)
                advance_search_obj = ASDA(advance_search_dict.get("word"), advance_search_dict.get("low_price", 0),
                                          advance_search_dict.get("high_price", 999999999))
                search_results = advance_search_obj.searchAvalable()
                customer.unset_state()
                for item in search_results:
                    product = PDA(p_id=str(item['id']))
                    # keyboard_1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=str(str(show_product(str(item['id']))['Price'])+" تومان"), callback_data="4"), InlineKeyboardButton(text="افزودن به سبد خرید", callback_data='add_to_cart '+str(item['id']))],[InlineKeyboardButton(text="جزییات بیشتر" ,callback_data=str("Product"+str(show_product(str(item['id']))["product_id"])))],])
                    keyboard_1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                        text=str(str(product.show_product()['Price']) + " تومان") + "💵", callback_data="4"),
                        InlineKeyboardButton(
                            text=u"افزودن به سبد خرید" + emoji.emojize(
                                " :package:", use_aliases=True),
                            callback_data='add_to_cart ' + str(
                                item['id']))], [
                        InlineKeyboardButton(
                            text="جزییات بیشتر",
                            callback_data=str("Product" + str(
                                product.show_product()[
                                    "product_id"])))], ])

                    # bot.sendMessage(chat_id,show_product(str(item['id']))['Name'])
                    caption = u"نام محصول: " + product.show_product()['Name']
                    bot.sendPhoto(from_id, product.show_product()['Image'], caption=caption, reply_markup=keyboard_1)
                if len(search_results) == 0:
                    bot.sendMessage(from_id, u"متاسفانه محصولی با این مشخصات یافت نشد")
                print "search_allllll_done"

            # End of search all button

            # Whene user Press on Enter Info Button
            if query_data == u"enterinfo_firstname":
                if customer.set_state(state_word='enterinfo_firstname'):
                    bot.answerCallbackQuery(query_id, text="اطلاعات خود را وارد کنید", show_alert=True)
                    bot.sendMessage(from_id, "نام خود را وارد نمایید.")
            # End Of Enter Info Button




            # Return to main Menu
            if query_data == u'return':
                keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                    text=emoji.emojize(":mag_right:", use_aliases=True) + u"دسته بندی ها", callback_data="categories"),
                    InlineKeyboardButton(text=emoji.emojize(":mag_right:",
                                                            use_aliases=True) + u"جستجو",
                                         callback_data="search")], [
                    InlineKeyboardButton(
                        text=emoji.emojize(" :package:",
                                           use_aliases=True) + u"سبد خرید",
                        callback_data='sabad'), InlineKeyboardButton(
                        text=emoji.emojize(" :postbox:", use_aliases=True) + u"انتقاد و پیشنهاد",
                        callback_data='enteghadstart')], [InlineKeyboardButton(
                    text=emoji.emojize(" :memo:", use_aliases=True) + u"وارد کردن اطلاعات شخصی برای خرید",
                    callback_data='enterinfo_firstname')], [InlineKeyboardButton(
                    text=emoji.emojize(" :back:", use_aliases=True) + u"بازگشت به منوی اصلی",
                    callback_data='return')], ])
                bot.sendPhoto(from_id, "https://www.turbogram.co/static/images/homepage/icon-6.8cebe055d143.png",
                              caption="منوی اصلی، لطفا یکی از گزینه های زیر زیر را انتخاب کنید.", reply_markup=keyboard)
                # button for return
                # [ InlineKeyboardButton(text=emoji.emojize(" :back:",use_aliases=True)+u"بازگشت به منوی اصلی", callback_data='return')]

            # Categories
            if query_data == u'categories':
                allcats = CatDA()
                cats = allcats.get_cats()
                cats_keyboard = []
                for category in cats:
                    cats_keyboard.append(
                        [InlineKeyboardButton(text=category.cat_name, callback_data="show_cat " + str(category.id))])

                cats_keyboard.append([InlineKeyboardButton(
                    text=emoji.emojize(" :back:", use_aliases=True) + u"بازگشت به منوی اصلی", callback_data='return')])
                bot.sendMessage(from_id, "دسته مورد نظر خود را انتخاب کنید: ",
                                reply_markup=InlineKeyboardMarkup(inline_keyboard=cats_keyboard))
            # show all surveys
            if query_data == "show_surveys":
                survey_object = SDA()
                all_surveys_data = survey_object.get_all_survey()
                keyboard = []
                print all_surveys_data
                for survey in all_surveys_data:
                    keyboard.append(
                        [InlineKeyboardButton(text=survey['title'], callback_data="survey" + str(survey['id']))])

                markup_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
                print markup_keyboard
                bot.sendMessage(chat_id=from_id, text="Surveys", reply_markup=markup_keyboard)

            elif "survey" in query_data:
                survey_id = query_data.replace("survey", "")
                # last number is order of question
                survey_object = SDA(survey_id=survey_id)
                question = survey_object.get_question_data(question_order=1)
                bot.sendMessage(chat_id=from_id, text="لطفا به سوالات پاسخ دهید.")
                bot.sendMessage(chat_id=from_id, text=question.text)
                # last number is question id
                customer.set_state("answer@" + str(survey_id) + "@2@" + str(question.pk))

            # When a category is selected
            if "show_cat" in query_data:
                temp = query_data.rsplit()
                cat_id = temp[-1]
                customer.set_current(current_word="cat_" + str(cat_id) + "_1")

                product = PDA(cat_id=cat_id, page_number=1)
                products = product.get_product_from_category()
                for item in products:
                    product = PDA(p_id=str(item['id']))
                    # keyboard_1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=str(str(show_product(str(item['id']))['Price'])+" تومان"), callback_data="4"), InlineKeyboardButton(text="افزودن به سبد خرید", callback_data='add_to_cart '+str(item['id']))],[InlineKeyboardButton(text="جزییات بیشتر" ,callback_data=str("Product"+str(show_product(str(item['id']))["product_id"])))],])
                    keyboard_1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                        text=str(str(product.show_product()['Price']) + " تومان") + "💵", callback_data="4"),
                        InlineKeyboardButton(
                            text=u"افزودن به سبد خرید" + emoji.emojize(
                                " :package:", use_aliases=True),
                            callback_data='add_to_cart ' + str(
                                item['id']))], [
                        InlineKeyboardButton(
                            text="جزییات بیشتر",
                            callback_data=str("Product" + str(
                                product.show_product()[
                                    "product_id"])))], ])

                    # bot.sendMessage(chat_id,show_product(str(item['id']))['Name'])
                    caption = u"نام محصول: " + product.show_product()['Name']
                    bot.sendPhoto(from_id, product.show_product()['Image'], caption=caption, reply_markup=keyboard_1)
                if len(products) == 10:
                    keyboard_morenext = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                        text=emoji.emojize(" :arrow_right:", use_aliases=True) + u"نمایش ۱۰ محصول بعدی",
                        callback_data='morenext')], [InlineKeyboardButton(
                        text=emoji.emojize(" :back:", use_aliases=True) + u"بازگشت به منوی اصلی",
                        callback_data='return')]])
                    bot.sendPhoto(chat_id=from_id, photo="http://lorempixel.com/400/50/",
                                  reply_markup=keyboard_morenext)
                    current_word = 'cat_' + str(cat_id) + '_' + str(1 + 1)
                    customer.set_current_cat(current_word=current_word)
                else:
                    customer.set_current_cat(current_word="")
                    keyboard_morenext = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                        text=emoji.emojize(" :back:", use_aliases=True) + u"بازگشت به منوی اصلی",
                        callback_data='return')]])
                    bot.sendPhoto(chat_id=from_id, photo="http://lorempixel.com/400/50/",
                                  reply_markup=keyboard_morenext)

            # Whene user Press on Sabad_kharid Button
            if query_data == u'sabad':

                shopping_cart = SHC(c_id=customer_id)
                print shopping_cart
                products = shopping_cart.sabad_from_customer()
                print products
                if products == []:
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                        text=emoji.emojize(" :back:", use_aliases=True) + u"بازگشت به منوی اصلی",
                        callback_data='return')], ])
                    bot.sendMessage(from_id, "محصولی در سبد خرید شما موجود نیست", reply_markup=keyboard)
                else:
                    bot.sendMessage(from_id, " سبد خرید شما")
                    total_price = 0
                    sabad_items = u""
                    for product_plus_number in products:
                        product = product_plus_number[0]
                        numnber = product_plus_number[1]
                        name = u'نام محصول: '
                        text = u'توضیحات: '
                        price = u'قیمت: '
                        sabad_items += product.product_name + ":" + str(numnber) + "\n"
                        total_price += product.price

                        caption_name = name + product.product_name + '\n'
                        caption_price = price + str(product.price) + '\n'
                        caption = caption_name + caption_price
                        product_id = product.id
                        keyboard_sabad = InlineKeyboardMarkup(
                            inline_keyboard=[[InlineKeyboardButton(text=u"حذف از سبد خرید" + emoji.emojize(" :x:",
                                                                                                           use_aliases=True) + "\n" + u"موجود: " + str(
                                numnber), callback_data="del_from_cart " + str(product_id))], [
                                                 InlineKeyboardButton(text=u"کاستن",
                                                                      callback_data="remove_one_more " + str(
                                                                          product_id)),
                                                 InlineKeyboardButton(text=u"افزودن",
                                                                      callback_data="add_one_more " + str(
                                                                          product_id))]])

                        bot.sendPhoto(from_id, photo=product.image, caption=caption, reply_markup=keyboard_sabad)
                        # bot.sendMessage(from_id,text=caption_text)
                    keyboard_sabad_end = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text=u"بازگشت به منو", callback_data="return"),
                         InlineKeyboardButton(text=u"خرید محصولات", callback_data='buy')]])
                    bot.sendMessage(from_id, u"اقلام موجود: " + "\n" + sabad_items + str(total_price),
                                    reply_markup=keyboard_sabad_end)

            # End Of Sabad_kharid Button

            # When User Click on ten more product
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
                    products = product.get_product_from_category()

                    if len(products) == 0:
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                            text=emoji.emojize(" :back:", use_aliases=True) + u"بازگشت به منوی اصلی",
                            callback_data='return')], ])
                        bot.sendMessage(from_id, " محصولی موجود نیست", reply_markup=keyboard)
                    else:
                        for item in products:
                            product = PDA(p_id=str(item['id']))
                            # keyboard_1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=str(str(show_product(str(item['id']))['Price'])+" تومان"), callback_data="4"), InlineKeyboardButton(text="افزودن به سبد خرید", callback_data='add_to_cart '+str(item['id']))],[InlineKeyboardButton(text="جزییات بیشتر" ,callback_data=str("Product"+str(show_product(str(item['id']))["product_id"])))],])
                            keyboard_1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                                text=str(str(product.show_product()['Price']) + " تومان") + "💵", callback_data="4"),
                                InlineKeyboardButton(
                                    text=u"افزودن به سبد خرید" + emoji.emojize(
                                        " :package:", use_aliases=True),
                                    callback_data='add_to_cart ' + str(
                                        item['id']))], [
                                InlineKeyboardButton(
                                    text="جزییات بیشتر",
                                    callback_data=str("Product" + str(
                                        product.show_product()[
                                            "product_id"])))], ])

                            # bot.sendMessage(chat_id,show_product(str(item['id']))['Name'])
                            caption = u"نام محصول: " + product.show_product()['Name']
                            bot.sendPhoto(from_id, product.show_product()['Image'], caption=caption,
                                          reply_markup=keyboard_1)

                        if len(products) == 10:
                            keyboard_morenext = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                                text=emoji.emojize(" :arrow_right:", use_aliases=True) + u"نمایش ۱۰ محصول بعدی",
                                callback_data='morenext')], [InlineKeyboardButton(
                                text=emoji.emojize(" :back:", use_aliases=True) + u"بازگشت به منوی اصلی",
                                callback_data='return')]])
                            bot.sendPhoto(chat_id=from_id, photo="http://lorempixel.com/400/50/",
                                          reply_markup=keyboard_morenext)
                            current_word = 'cat_' + str(cat_id) + '_' + str(current_page + 1)
                            customer.set_current_cat(current_word=current_word)
                        else:
                            customer.set_current_cat(current_word="")
                            keyboard_morenext = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                                text=emoji.emojize(" :back:", use_aliases=True) + u"بازگشت به منوی اصلی",
                                callback_data='return')]])
                            bot.sendPhoto(chat_id=from_id, photo="http://lorempixel.com/400/50/",
                                          reply_markup=keyboard_morenext)

                if u'search' == current_state:
                    current_command = str(current_info[1])
                    print(current_info)
                    search_obj = SDA(search_word=current_command, page_number=current_page)
                    search_results = search_obj.search()
                    for item in search_results:
                        product = PDA(p_id=str(item['id']))
                        # keyboard_1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=str(str(show_product(str(item['id']))['Price'])+" تومان"), callback_data="4"), InlineKeyboardButton(text="افزودن به سبد خرید", callback_data='add_to_cart '+str(item['id']))],[InlineKeyboardButton(text="جزییات بیشتر" ,callback_data=str("Product"+str(show_product(str(item['id']))["product_id"])))],])
                        keyboard_1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                            text=str(str(product.show_product()['Price']) + " تومان") + "💵", callback_data="4"),
                            InlineKeyboardButton(
                                text=u"افزودن به سبد خرید" + emoji.emojize(
                                    " :package:", use_aliases=True),
                                callback_data='add_to_cart ' + str(
                                    item['id']))], [
                            InlineKeyboardButton(
                                text="جزییات بیشتر",
                                callback_data=str("Product" + str(
                                    product.show_product()[
                                        "product_id"])))], ])

                        # bot.sendMessage(chat_id,show_product(str(item['id']))['Name'])
                        caption = u"نام محصول: " + product.show_product()['Name']
                        bot.sendPhoto(from_id, product.show_product()['Image'], caption=caption,
                                      reply_markup=keyboard_1)

                    if len(search_results) == 10:
                        keyboard_morenext = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                            text=emoji.emojize(" :arrow_right:", use_aliases=True) + u"نمایش ۱۰ محصول بعدی",
                            callback_data='morenext')], [InlineKeyboardButton(
                            text=emoji.emojize(" :back:", use_aliases=True) + u"بازگشت به منوی اصلی",
                            callback_data='return')]])
                        bot.sendPhoto(chat_id=from_id, photo="http://lorempixel.com/400/50/",
                                      reply_markup=keyboard_morenext)
                        current_word = 'search_' + current_command + '_' + str(current_page + 1)
                        customer.set_current(current_word=current_word)
                    else:
                        keyboard_morenext = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                            text=emoji.emojize(" :back:", use_aliases=True) + u"بازگشت به منوی اصلی",
                            callback_data='return')]])
                        bot.sendPhoto(chat_id=from_id, photo="http://lorempixel.com/400/50/",
                                      reply_markup=keyboard_morenext)

            # End of When User Click on ten more product

            if query_data == u'4':
                notification = "برای خرید این محصول بر روی افزودن به سبد خرید کلیک کنید"
                bot.answerCallbackQuery(query_id, text=notification)

            for id in models.Product.objects.values('id'):
                product = PDA(p_id=str((id['id'])))
                like_counts = product.get_likes()
                dislike_counts = product.get_dislikes()
                models.Like_dislike.objects.filter(p_id=str((id['id']))).count()

                keyboard_1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=str(
                    str(models.Product.objects.filter(pk=id['id']).values('price')[0]['price']) + " تومان") + "💵",
                                                                                         callback_data="4"),
                                                                    InlineKeyboardButton(
                                                                        text=u"افزودن به سبد خرید" + emoji.emojize(
                                                                            " :package:", use_aliases=True),
                                                                        callback_data='add_to_cart ' + str(id['id']))],
                                                                   [InlineKeyboardButton(text="👍" + str(like_counts),
                                                                                         callback_data='do_like ' + str(
                                                                                             id['id'])),
                                                                    InlineKeyboardButton(
                                                                        text="👎" + str(dislike_counts),
                                                                        callback_data='do_dislike ' + str(id['id']))], [
                                                                       InlineKeyboardButton(text="ثبت نظر",
                                                                                            callback_data=str(
                                                                                                "User_comment") + str(
                                                                                                id['id'])),
                                                                       InlineKeyboardButton(text="مشاهده نظرات",
                                                                                            callback_data="Show_comment" + str(
                                                                                                id['id']))]])

                if query_data == str("Product" + str((id['id']))):
                    # bot.sendMessage(from_id , models.Product.objects.filter(pk=id['id']).values('product_name')[0]['product_name'])
                    caption = u"نام محصول: " + models.Product.objects.filter(pk=id['id']).values('product_name')[0][
                        'product_name']
                    bot.sendPhoto(from_id, models.Product.objects.filter(pk=id['id']).values('image')[0]['image'],
                                  caption=caption)
                    bot.sendMessage(from_id,
                                    u"توضیحات: " + models.Product.objects.filter(pk=id['id']).values('text')[0]['text'],
                                    reply_markup=keyboard_1)
                if query_data == str("User_comment" + str((id['id']))):
                    print('222')
                    if customer.set_state(state_word=str('User_comment' + str(id['id']))):
                        notification = "نظر خود را درمورد این محضول بنویسید"
                        bot.answerCallbackQuery(query_id, text=notification)
                if query_data == str("Show_comment" + str(id['id'])):
                    comments = models.Product_comment.objects.filter(product_id=id['id'])
                    print(list(comments))
                    if list(comments) == []:
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                            text=emoji.emojize(" :back:", use_aliases=True) + u"بازگشت به منوی اصلی",
                            callback_data='return')], ])
                        bot.sendMessage(from_id, " نظری برای این محصول موجود نیست", reply_markup=keyboard)
                    else:
                        for comment in comments:
                            bot.sendMessage(from_id, comment.text_comment)

            if "do_like" in query_data:
                query = query_data.rsplit()
                product_id = query[-1]
                product = PDA(t_id=from_id, p_id=product_id)
                flag = product.like()
                if flag:
                    notification = "like done"
                    bot.answerCallbackQuery(query_id, text=notification)
                else:
                    notification = "like deleted"
                    bot.answerCallbackQuery(query_id, text=notification)

                product = PDA(p_id=product_id)
                like_counts = product.get_likes()
                dislike_counts = product.get_dislikes()
                models.Like_dislike.objects.filter(p_id=str((product_id))).count()
                identifier = msg["message"]
                keyboard_2 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=str(
                    str(models.Product.objects.filter(pk=id['id']).values('price')[0]['price']) + " تومان") + "💵",
                                                                                         callback_data="4"),
                                                                    InlineKeyboardButton(
                                                                        text=u"افزودن به سبد خرید" + emoji.emojize(
                                                                            " :package:", use_aliases=True),
                                                                        callback_data='add_to_cart ' + str(id['id']))],
                                                                   [InlineKeyboardButton(text="👍" + str(like_counts),
                                                                                         callback_data='do_like ' + str(
                                                                                             id['id'])),
                                                                    InlineKeyboardButton(
                                                                        text="👎" + str(dislike_counts),
                                                                        callback_data='do_dislike ' + str(id['id']))], [
                                                                       InlineKeyboardButton(text="ثبت نظر",
                                                                                            callback_data=str(
                                                                                                "User_comment") + str(
                                                                                                id['id'])),
                                                                       InlineKeyboardButton(text="مشاهده نظرات",
                                                                                            callback_data="Show_comment" + str(
                                                                                                id['id']))]])
                msg_identifier = telepot.message_identifier(identifier)
                telepot.Bot.editMessageReplyMarkup(bot, msg_identifier=msg_identifier, reply_markup=keyboard_2)

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

                product = PDA(p_id=product_id)
                like_counts = product.get_likes()
                dislike_counts = product.get_dislikes()
                models.Like_dislike.objects.filter(p_id=str((product_id))).count()
                identifier = msg["message"]
                keyboard_2 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=str(
                    str(models.Product.objects.filter(pk=id['id']).values('price')[0]['price']) + " تومان") + "💵",
                                                                                         callback_data="4"),
                                                                    InlineKeyboardButton(
                                                                        text=u"افزودن به سبد خرید" + emoji.emojize(
                                                                            " :package:", use_aliases=True),
                                                                        callback_data='add_to_cart ' + str(id['id']))],
                                                                   [InlineKeyboardButton(text="👍" + str(like_counts),
                                                                                         callback_data='do_like ' + str(
                                                                                             id['id'])),
                                                                    InlineKeyboardButton(
                                                                        text="👎" + str(dislike_counts),
                                                                        callback_data='do_dislike ' + str(id['id']))], [
                                                                       InlineKeyboardButton(text="ثبت نظر",
                                                                                            callback_data=str(
                                                                                                "User_comment") + str(
                                                                                                id['id'])),
                                                                       InlineKeyboardButton(text="مشاهده نظرات",
                                                                                            callback_data="Show_comment" + str(
                                                                                                id['id']))]])
                msg_identifier = telepot.message_identifier(identifier)
                telepot.Bot.editMessageReplyMarkup(bot, msg_identifier=msg_identifier, reply_markup=keyboard_2)

            if "add_to_cart" in query_data:
                query = query_data.rsplit()
                product_id = query[-1]
                shopping_cart = SHC(c_id=customer_id, p_id=product_id)
                print max_cart
                if max_cart < 5:
                    flag = shopping_cart.add_to_cart()
                    if flag:
                        notification = "محصول با موفقیت به سبد خرید شما اضافه شد"
                        bot.answerCallbackQuery(query_id, text=notification)
                    else:
                        notification = "این محصول در سبد خرید شما وجود دارد"
                        bot.answerCallbackQuery(query_id, text=notification)
                else:
                    notification = "تنها مجاز به اضافه کردن 5 محصول در سبد خرید خود هستید."
                    bot.answerCallbackQuery(query_id, text=notification)

            if "del_from_cart" in query_data:
                query = query_data.rsplit()
                product_id = query[-1]
                shopping_cart = SHC(c_id=customer_id, p_id=product_id)
                flag = shopping_cart.del_from_cart()
                if (flag):
                    notification = "محصول با موفقیت از سبد خرید حذف شد"
                    bot.answerCallbackQuery(query_id, text=notification)
                    identifier = msg["message"]
                    msg_identifier = telepot.message_identifier(identifier)
                    telepot.Bot.deleteMessage(bot, msg_identifier=msg_identifier)


                else:
                    notification = "این محصول در سبد شما وجود ندارد"
                    bot.answerCallbackQuery(query_id, text=notification)

            if "add_one_more" in query_data:
                query = query_data.rsplit()
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
                    keyboard_3 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                        text=u"حذف از سبد خرید" + emoji.emojize(" :x:", use_aliases=True) + "\n" + u"موجود: " + str(
                            cart_object.number), callback_data="del_from_cart " + str(cart_object.p_id_id))], [
                        InlineKeyboardButton(text=u"کاستن",
                                             callback_data="remove_one_more " + str(
                                                 cart_object.p_id_id)),
                        InlineKeyboardButton(text=u"افزودن",
                                             callback_data="add_one_more " + str(
                                                 cart_object.p_id_id))]])
                    msg_identifier = telepot.message_identifier(identifier)
                    telepot.Bot.editMessageReplyMarkup(bot, msg_identifier=msg_identifier, reply_markup=keyboard_3)
                else:
                    notification = "انجام عملیات مقدور نبود"
                    bot.answerCallbackQuery(query_id, text=notification)

            if "remove_one_more" in query_data:
                query = query_data.rsplit()
                product_id = query[-1]
                shopping_cart = SHC(c_id=customer_id, p_id=product_id)
                flag = shopping_cart.add_remove(-1)
                if flag:
                    notification = "از تعداد محصول شما کاسته شد"
                    bot.answerCallbackQuery(query_id, text=notification)
                    cart = SHC(c_id=customer_id, p_id=product_id)
                    cart_object = cart.get_object()
                    identifier = msg["message"]
                    keyboard_3 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                        text=u"حذف از سبد خرید" + emoji.emojize(" :x:", use_aliases=True) + "\n" + u"موجود: " + str(
                            cart_object.number), callback_data="del_from_cart " + str(cart_object.p_id_id))], [
                        InlineKeyboardButton(text=u"کاستن",
                                             callback_data="remove_one_more " + str(
                                                 cart_object.p_id_id)),
                        InlineKeyboardButton(text=u"افزودن",
                                             callback_data="add_one_more " + str(
                                                 cart_object.p_id_id))]])
                    msg_identifier = telepot.message_identifier(identifier)
                    telepot.Bot.editMessageReplyMarkup(bot, msg_identifier=msg_identifier, reply_markup=keyboard_3)
                else:
                    notification = "انجام عملیات مقدور نبود"
                    bot.answerCallbackQuery(query_id, text=notification)

            # When you click on buy
            if query_data == 'buy':
                shopping_cart = SHC(c_id=customer_id)
                customer.set_state("buy_comment")
                bot.sendMessage(from_id, "لطفا توضیحات محصول را وارد کنید.")

            if query_data == u"enteghadstart":
                allcats = CatDA()
                cat_keyboard = allcats.feed_back_cat_keyboard()
                bot.sendMessage(from_id, " یک گزینه را انتخاب کنید ", reply_markup=cat_keyboard)

            if u"naghd" in query_data:
                cat_id = query_data.replace("naghd", "")
                customer.set_state(state_word="naghd" + cat_id)
                bot.sendMessage(from_id, "لطفا نظر خود را وارد کنید.")

        def send_base_product_info(from_id, product):
            caption = u"نام محصول: " + product.product_name
            image = product.image
            keyboard = [[InlineKeyboardButton(
                text=str(product.price) + u" تومان" + emoji.emojize(" :dollar:", use_aliases=True), callback_data="4"),
                InlineKeyboardButton(
                    text=u"افزودن به سبد خرید" + emoji.emojize(" :package:", use_aliases=True),
                    callback_data='add_to_cart ' + str(product.id))], [
                InlineKeyboardButton(text=u"جزییات بیشتر" + emoji.emojize(" :clipboard:", use_aliases=True),
                                     callback_data=str("Product" + str(product.id)))], ]
            try:
                bot.sendPhoto(from_id, photo=image, caption=caption,
                              reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
                return True
            except  Exception:
                print Exception
                return False

        def get_AdvanceSearchOptions(user_state):
            states = user_state.rsplit(",")
            res_dict = {}
            # customer.set_state(state_word='lgh_advance_search,¢,0,999999999,0')
            if states[1] != "¢":
                res_dict["word"] = states[1]
            if states[2] != "0":
                res_dict["low_price"] = states[2]
            if states[3] != "999999999":
                res_dict["high_price"] = states[3]
            return res_dict

        token = '305910807:AAHG7PRJ767S6sMv_4CPpmFeI17Pe5kFbEs'

        bot = telepot.Bot(token)
        bot.message_loop({'chat': on_chat_message, 'callback_query': on_callback_query})
        print('Listening ...')

        counter = 0
        adCounter = 0
        while 1:
            time.sleep(10)
            if counter % 1 == 0:
                ad = Advertise(adCounter)
                adCounter += 1
                advertise = ad.getAdvertise()
                if advertise != 0:
                    print advertise.title
                    customers = ad.getAllCustomers()
                    for customer in customers:
                        image = advertise.image
                        print image
                        try:
                            bot.sendPhoto(chat_id=customer.telegram_id,
                                          photo=open(str(image)),
                                          caption=advertise.title + "\n" + advertise.text)
                        except Exception as e:
                            print e
                            print "failed sending advertise"
            counter += 1
