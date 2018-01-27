from easybot import models
from admin_panel import FormsHandler


class TicketManager:
    def __init__(self):
        pass

    def get_all_tickets(self):
        result = models.Ticket.objects.all()
        tickets = []
        for ticket in result:
            ticket_dict = {}
            ticket_dict['id'] = ticket.pk
            ticket_dict['title'] = ticket.title
            tickets.append(ticket_dict)

        return tickets

