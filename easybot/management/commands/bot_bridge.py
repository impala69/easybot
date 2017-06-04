#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
import telepot, time
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist


from ... import models


class Command(BaseCommand):
    help = 'for running bot execution'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        def on_chat_message(msg):
            #Get User data From User RealTime
            print msg
            username = msg['from']['username']
            content_type, chat_type, chat_id = telepot.glance(msg)
            customer_id = return_customer_id(chat_id)
            if content_type == "text":
                command = msg['text']
                print command
            elif content_type == 'contact':
                command = msg['contact']['phone_number']
            else:
                command = 'None'
            if type(return_user_state(chat_id)) != None:
                user_state = return_user_state(chat_id)
                print "state: " + str(user_state)
            else:
                user_state = "Null"
                print "state: " + str(user_state)
            #End Of Get Data From User


            keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="جستجو" , callback_data="search"),],[ InlineKeyboardButton(text="سبد خرید", callback_data='sabad')],[ InlineKeyboardButton(text="واردکردن اطلاعات شخصی برای خرید از ربات", callback_data='enterinfo_firstname')],[ InlineKeyboardButton(text="نظردهی", callback_data='enteghadstart')]])


            if command == '/start':


                #Add User if thechat_id from user not in Database
                if not check_customer_is(chat_id):
                    add_customer(chat_id, username)

                #End Of Add User if not exist




                for i in range(1,4):
                    try:
                        q = models.Sabad_Kharid(cus_id=customer, p_id_id=int(i))
                        q.save()
                    except :
                        pass
                        #print
                        #print "cant save:"+str(i)

                bot.sendMessage(chat_id , "یک گزینه را انتخاب کنید"  , reply_markup= keyboard)

            elif content_type == 'text' and user_state == 'search':
                search_results = search(command=command, page_number=1)
                print search_results
                for item in search_results:
                    keyboard_1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=str(str(show_product(str(item['id']))['Price'])+" تومان"), callback_data="4"), InlineKeyboardButton(text="افزودن به سبد خرید", callback_data='add_to_cart '+str(item['id']))],[InlineKeyboardButton(text="جزییات بیشتر" ,callback_data=str("Product"+str(show_product(str(item['id']))["product_id"])))],])
                    #bot.sendMessage(chat_id,show_product(str(item['id']))['Name'])
                    caption=u"نام محصول: "+show_product(str(item['id']))['Name']
                    bot.sendPhoto(chat_id,show_product(str(item['id']))['Image'],caption=caption,reply_markup=keyboard_1)
                keyboard_morenext= InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="نمایش ۱۰ محصول بعدی" ,callback_data='morenext')]])
                bot.sendPhoto(chat_id=chat_id, photo="http://lorempixel.com/400/50/", reply_markup=keyboard_morenext)
                set_current(telegram_id=chat_id, current_word='search_' + command + '_1')
                unset_state(chat_id)

            elif content_type == 'text' and user_state == 'enterinfo_firstname':
                enter_first_name(chat_id, f_name=command)
                set_state(telegram_id=chat_id, state_word='enterinfo_lastname')
                bot.sendMessage(chat_id, "نام خانوادگی خود را وارد کنید.")

            elif content_type == 'text' and user_state == 'enterinfo_lastname':
                enter_last_name(telegram_id=chat_id, l_name=command)
                set_state(telegram_id=chat_id, state_word='enterinfo_address')
                bot.sendMessage(chat_id, "آدرس خود را وارد کنید")

            elif content_type == 'text' and user_state == 'enterinfo_address':
                enter_address(telegram_id=chat_id, address=command)
                set_state(telegram_id=chat_id, state_word='enterinfo_phone')
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
                    enter_phone(telegram_id=chat_id, phone=command)
                    unset_state(chat_id)
                    bot.sendMessage(chat_id, "اطلاعات شما  با موفقیت ثبت شد.")
                else:
                    bot.sendMessage(chat_id=chat_id, text="لطفا بر روی دکمه فرستادن شماره تلفن به ربات کلیک کنید")



            elif content_type == 'text' and  'naghd' in user_state:
                naghd_cat = int(user_state.replace("naghd", ""))
                if enter_comment(telegram_id=chat_id,new_comment=command, cat_id=naghd_cat):
                    notification="نظر با موفقیت ثبت شد. با تشکر از شما"
                    bot.sendMessage(chat_id, text=notification)
                    unset_state(chat_id)
                else:
                    notification="لططفا مجددا نظر را وارد نمایید."
                    bot.sendMessage(chat_id, text=notification)


            elif content_type == 'text' and "User_comment" in user_state:
                if enter_user_comment(customer_id= return_customer_id(chat_id),p_id = user_state[12:],new_comment=command):
                    notification="نظر با موفقیت ثبت شد. با تشکر از شما"
                    bot.sendMessage(chat_id, text=notification)
                    unset_state(chat_id)
                else:
                    notification="لططفا مجددا نظر را وارد نمایید."
                    bot.sendMessage(chat_id, text=notification)










        def on_callback_query(msg):
            #Get User Query Data
            query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
            customer_id = cus_id(from_id)

            command = msg
            #ENd of getting Query Data from user

            #Whene user Press on Search Button
            if query_data == u"search":
                if set_state(from_id, 'search'):
                    bot.answerCallbackQuery(query_id, text="نام محصول را وارد کنید", show_alert=True)
            #End Of Search Button

            #Whene user Press on Enter Info Button
            if query_data == u"enterinfo_firstname":
                if set_state(from_id, 'enterinfo_firstname'):
                    bot.answerCallbackQuery(query_id, text="اطلاعات خود را وارد کنید", show_alert=True)
                    bot.sendMessage(from_id, "نام خود را وارد نمایید.")
            #End Of Enter Info Button




            #Whene user Press on Sabad_kharid Button
            if query_data ==u'sabad':
                bot.sendMessage(from_id,"sabad kharid")
                customer=cus_id(from_id)
                products=sabad_from_customer(customer.id)
                for product in products:
                    name=u'نام محصول: '
                    text=u'توضیحات: '
                    price=u'قیمت: '

                    caption_name=name+product.product_name+'\n'
                    caption_text=text+product.text+'\n'
                    caption_price=price+str(product.price)+'\n'
                    caption=caption_name+caption_price
                    product_id=product.id
                    keyboard_sabad = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="حذف از سبد خرید", callback_data="del_from_cart "+str(product_id))]])

                    bot.sendPhoto(from_id,photo=product.image,caption=caption,reply_markup=keyboard_sabad)
                    bot.sendMessage(from_id,text=caption_text)

            #End Of Sabad_kharid Button

            #When User Click on ten more product
            if query_data == u'morenext':
                current = get_current(telegram_id=from_id)
                current_info = current.split("_")
                current_state = current_info[0]
                if u'search' == current_state:
                    current_command = str(current_info[1])
                    current_page = int(current_info[2])
                    search_results = search(current_command, current_page + 1)
                    for item in search_results:
                        keyboard_1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=str(str(show_product(str(item['id']))['Price'])+" تومان"), callback_data="4"), InlineKeyboardButton(text="افزودن به سبد خرید", callback_data='add_to_cart '+str(item['id']))],[InlineKeyboardButton(text="جزییات بیشتر" ,callback_data=str("Product"+str(show_product(str(item['id']))["product_id"])))],])
                        #bot.sendMessage(chat_id,show_product(str(item['id']))['Name'])
                        caption=u"نام محصول: "+show_product(str(item['id']))['Name']
                        bot.sendPhoto(from_id,show_product(str(item['id']))['Image'],caption=caption,reply_markup=keyboard_1)

                    if len(search_results) == 10:
                        keyboard_morenext= InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="نمایش ۱۰ محصول بعدی" ,callback_data='morenext')]])
                        bot.sendPhoto(chat_id=from_id, photo="http://lorempixel.com/400/50/", reply_markup=keyboard_morenext)
                        current_word = 'search_' + current_command + '_' + str(current_page + 1)
                        set_current(telegram_id=from_id, current_word=current_word)




            #End of When User Click on ten more product

            if query_data == u'4':
                notification = "برای خرید این محصول بر روی افزودن به سبد خرید کلیک کنید"
                bot.answerCallbackQuery(query_id, text=notification)

            for id in models.Product.objects.values('id'):
                like_counts=get_likes(str((id['id'])))
                dislike_counts=get_dislikes(str((id['id'])))
                models.Like_dislike.objects.filter(p_id=str((id['id']))).count()
                keyboard_1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=str(str(models.Product.objects.filter(pk=id['id']).values('price')[0]['price'])+" تومان"), callback_data="4"), InlineKeyboardButton(text="افزودن به سبد خرید", callback_data='add_to_cart '+str(id['id']))],[InlineKeyboardButton(text="like"+str(like_counts), callback_data='do_like '+str(id['id'])),InlineKeyboardButton(text="dislike"+str(dislike_counts), callback_data='do_dislike '+str(id['id']))], [InlineKeyboardButton(text = "ثبت نظر" , callback_data=str("User_comment")+ str(id['id'])) , InlineKeyboardButton(text = "مشاهده نظرات" , callback_data = "Show_comment" + str(id['id']))]])

                if query_data == str("Product" + str((id['id']))):
                    #bot.sendMessage(from_id , models.Product.objects.filter(pk=id['id']).values('product_name')[0]['product_name'])
                    caption= u"نام محصول: " +models.Product.objects.filter(pk=id['id']).values('product_name')[0]['product_name']
                    bot.sendPhoto(from_id , models.Product.objects.filter(pk=id['id']).values('image')[0]['image'],caption=caption)
                    bot.sendMessage(from_id,u"توضیحات: " +models.Product.objects.filter(pk=id['id']).values('text')[0]['text'],reply_markup=keyboard_1)
                if query_data == str("User_comment" + str((id['id']))):
                    if set_state(from_id, str('User_comment' + str(id['id']))):
                        notification="نظر خود را درمورد این محضول بنویسید"
                        bot.answerCallbackQuery(query_id, text=notification)
                if query_data == str("Show_comment" + str(id['id'])):
                    comments = models.Product_comment.objects.filter(product_id = id['id'])
                    for comment in comments:
                        bot.sendMessage(from_id, comment.text_comment)

            if "do_like" in query_data:
               query=query_data.rsplit()
               product_id=query[-1]
               flag=like(from_id,product_id)
               if(flag):
                   notification="like done"
                   bot.answerCallbackQuery(query_id, text=notification)
               else:
                   notification="like deleted"
                   bot.answerCallbackQuery(query_id, text=notification)

            if "do_dislike" in query_data:
                query=query_data.rsplit()
                product_id=query[-1]
                flag=dislike(from_id,product_id)
                if(flag):
                    notification="dislike done"
                    bot.answerCallbackQuery(query_id, text=notification)
                else:
                    notification="dislike deleted"
                    bot.answerCallbackQuery(query_id, text=notification)


            if "add_to_cart" in query_data:
                query=query_data.rsplit()
                #bot.sendMessage(from_id,str(query))
                product_id=query[-1]
                flag=add_to_cart(customer_id,product_id)
                if(flag):
                    notification="محصول با موفقیت به سبد خرید شما اضافه شد"
                    bot.answerCallbackQuery(query_id, text=notification)

                else:
                    notification="این محصول در سبد خرید شما وجود دارد"
                    bot.answerCallbackQuery(query_id, text=notification)




            if  "del_from_cart" in query_data:
                query=query_data.rsplit()
                product_id=query[-1]
                flag=del_from_cart(customer_id,product_id)
                if(flag):
                    notification="محصول با موفقیت از سبد خرید حذف شد"
                    bot.answerCallbackQuery(query_id, text=notification)

                else:
                    notification="این محصول در سبد شما وجود ندارد"
                    bot.answerCallbackQuery(query_id, text=notification)

            if query_data == u"enteghadstart":
                cat_keyboard=feed_back_cat_keyboard()
                bot.sendMessage(from_id, " یک گزینه را انتخاب کنید " ,reply_markup=cat_keyboard)

            if u"naghd" in query_data:
                cat_id = query_data.replace("naghd", "")
                set_state(from_id, "naghd" + cat_id)
                bot.sendMessage(from_id, "لطفا نظر خود را وارد کنید.")





        def search(command, page_number):
            if page_number == 1:
                result = models.Product.objects.filter(product_name__icontains=command).order_by('id').values('id')[:10]
                return result
            else:
                offset = (page_number-1)*10
                result = models.Product.objects.filter(product_name__icontains=command).order_by('id').values('id')[offset:offset+9]
                return result


        def show_product(p_id):
            product = models.Product.objects.get(pk=p_id)
            product_dict = {'product_id': product.pk, 'Name': product.product_name, 'Image':product.image, 'Text':product.text, 'Price':product.price}
            return product_dict


        def cus_id(chat_id):
            customer = models.Customer.objects.get(telegram_id=chat_id)
            return customer


        def sabad_from_customer(customer_id):
            rows = models.Sabad_Kharid.objects.filter(cus_id=customer_id)
            products = [item.p_id for item in rows]
            return products

        def del_from_cart(c_id,product_id):
            cart = models.Sabad_Kharid.objects.filter(cus_id=c_id)
            count0 = models.Sabad_Kharid.objects.filter(cus_id=c_id).count()
            cart = cart.filter(p_id=product_id)
            count = cart.filter(p_id=product_id).count()
            if count0 == 0 or count == 0:
                return False
            else:
                cart.delete()
                return True

        def add_to_cart(c_id,product_id):
            try:
                product=models.Product.objects.get(id=product_id)
                entry = models.Sabad_Kharid(cus_id=c_id, p_id=product)
                entry.save()
                return True
            except:
                return False

        def enter_comment(telegram_id, new_comment, cat_id):
            try:
                comment = models.Comment(telegram_id=telegram_id, comment=new_comment, comment_cat=cat_id)
                comment.save()
                return True
            except:
                return False

        #Function From Iman
        def return_customer_id(chat_id):
            try:
                customer = models.Customer.objects.get(telegram_id=chat_id)
                return customer.id
            except ObjectDoesNotExist:
                customer = None
                return customer

        #function From Iman
        def add_customer(telegram_id, username):
            try:
                entry = models.Customer(telegram_id=telegram_id, username=username)
                entry.save()
                return True
            except:
                return False

        #function From Iman
        def check_customer_is(telegram_id):
            try:
                customer = get_object_or_404(models.Customer, telegram_id=telegram_id)
                return 1
            except:
                return 0

        #Function From Iman
        def return_user_state(telegram_id):
            try:
                state = models.Customer.objects.get(telegram_id=telegram_id)
                return state.state
            except ObjectDoesNotExist:
                state = None
                return state

        #Function From Iman
        def set_state(telegram_id, state_word):
            try:

                state = models.Customer.objects.get(telegram_id=telegram_id)
                state.state = state_word
                state.save()
                return True
            except:
                return False

        #Function From Iman
        def unset_state(telegram_id):
            try:
                state = models.Customer.objects.get(telegram_id=telegram_id)
                state.state = ''
                state.save()
                return True
            except:
                return False

        #Function From Iman
        def enter_first_name(telegram_id, f_name):
            try:
                customer = models.Customer.objects.get(telegram_id=telegram_id)
                customer.first_name = f_name
                customer.save()
                return True
            except:
                return False

        #Function From Iman
        def enter_last_name(telegram_id, l_name):
            try:
                customer = models.Customer.objects.get(telegram_id=telegram_id)
                customer.last_name = l_name
                customer.save()
                return True
            except:
                return False

        #Function From Iman
        def enter_address(telegram_id, address):
            try:
                customer = models.Customer.objects.get(telegram_id=telegram_id)
                customer.address = address
                customer.save()
                return True
            except:
                return False



        #Function From Iman
        def enter_phone(telegram_id, phone):
            try:
                customer = models.Customer.objects.get(telegram_id=telegram_id)
                customer.phone = phone
                customer.save()
                return True
            except:
                return False

        #Function From Iman
        def get_current(telegram_id):
            try:
                current = models.Customer.objects.get(telegram_id=telegram_id)
                return current.current
            except ObjectDoesNotExist:
                current = None
                return current

        #Function From Iman
        def set_current(telegram_id, current_word):
            try:
                current = models.Customer.objects.get(telegram_id=telegram_id)
                current.current = current_word
                current.save()
                return True
            except:
                return False

        #Function From MhD
        def enter_user_comment(customer_id, p_id, new_comment):
            try:
                comment = models.Product_comment(customer_id=customer_id,product_id = p_id,text_comment=new_comment)
                comment.save()
                return True
            except:
                return False

        #Function From Kazi
        def like(telegram_id,product_id):
            product=models.Product.objects.get(id=product_id)
            try:
                entry=models.Like_dislike(telegram_id=telegram_id,p_id=product,like=True)
                entry.save()
                print "adding like"
                return True
            except:
                entry=models.Like_dislike.objects.get(telegram_id=telegram_id,p_id=product)
                if(entry.like):
                    print "clearing like"
                    entry.delete()
                    return False
                else:
                    print "changing dislike to like"
                    entry.like=True
                    entry.save()
                    return True

        def dislike(telegram_id,product_id):
            product=models.Product.objects.get(id=product_id)
            try:
                entry=models.Like_dislike(telegram_id=telegram_id,p_id=product,like=False)
                entry.save()
                print "adding dislike"
                return True
            except:
                entry=models.Like_dislike.objects.get(telegram_id=telegram_id,p_id=product)
                if(not entry.like):
                    print "clearing dislike"
                    entry.delete()
                    return False
                else:
                    print "changing like to dislike "
                    entry.like=False
                    entry.save()
                    return True

        def get_likes(p_id):
            return models.Like_dislike.objects.filter(p_id=p_id,like=True).count()

        def get_dislikes(p_id):
            return models.Like_dislike.objects.filter(p_id=p_id,like=False).count()


        def feed_back_cat_keyboard():
            list1 = []
            for item in models.Feedback_cat.objects.all():
                name = item.fb_name
                cat_keyboard = [InlineKeyboardButton(text=str(name), callback_data='naghd' + str(item.pk))]
                list1.append(cat_keyboard)
            cat_keyboard = InlineKeyboardMarkup(inline_keyboard=list1)

            return cat_keyboard



        #Token = '328961413:AAH9DnhEQhjH78feXsRfV-1QnbVAwTL9xZU'
        #Token = '359562635:AAHFCq9EnVrFtpOme-H81u67TJJdWLmw0g8'
        #Token = '362176353:AAGfkbKFdQS0pe1jhrjGbL7z2Sglq9tXyzY'
        Token = '305910807:AAHG7PRJ767S6sMv_4CPpmFeI17Pe5kFbEs'

        bot = telepot.Bot(Token)
        bot.message_loop({'chat': on_chat_message , 'callback_query': on_callback_query})
        print('Listening ...')

        while 1:
            time.sleep(10)




