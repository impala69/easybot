from ... import models
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

class Ticket:
    def __init__(self,ticket_title = None,ticket_question = None,ticket_id = None , ticket_order = None):
        self.__ticket_title = ticket_title
        self.__ticket_question = ticket_question
        self.__ticket_id = ticket_id
        self.__ticket_order = ticket_order

    def enter_ticket(self):
        try:
            ticket = models.Ticket(title = self.__ticket_title )
            ticket.save()
            return True
        except:
            return False
    def enter_question(self):
        try:
            ticket_data = models.AnswerQuestionTicket(ticket_id = self.__ticket_id,order = self.__ticket_order,text =self.__ticket_question)
            ticket_data.save()
            self.__ticket_order += 2
            return True
        except:
            return False




    '''def return_ticket_data(self):
        ticket = models.Ticket.objects.get(title = self.__ticket_title)
        return ticket.title'''