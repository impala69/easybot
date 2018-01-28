from easybot import models
import requests, json
import OrderManager


class TransactionManager:
    def __init__(self, trans_id=None):
        self.trans_id = trans_id

    def get_all_transactions(self):
        result = models.Transactions.objects.all()
        transaction_data = []
        all_transactions = []
        for transaction in result:
            order = OrderManager.OrderManager(transaction_object=transaction)
            transaction_data.append(transaction.pk)
            transaction_data.append(transaction.amount)
            transaction_data.append(transaction.status)
            transaction_data.append(transaction.transaction_id_from_payment)
            transaction_data.append(order.return_order_with_transaction())
            all_transactions.append(transaction_data)
            transaction_data = []
        return all_transactions

    def get_transaction_data(self):
        transaction = models.Transactions.objects.get(transaction_id_from_payment=self.trans_id)
        transaction_dict = {'transaction_id': transaction.pk, 'transId': transaction.transaction_id_from_payment,
                            'status': transaction.status, }
        return transaction_dict

    def set_status(self, state):
        try:
            transaction = models.Transactions.objects.get(transaction_id_from_payment=self.trans_id)
            transaction.status = state
            transaction.save()
            return 1
        except Exception as e:
            print e
            return 0

