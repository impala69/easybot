from easybot import models
from admin_panel import FormsHandler
import CategoryManager


class TransactionManager:
    def __init__(self, trans_id=None):
        self.trans_id = trans_id

    def get_all_transactions(self):
        result = models.Transactions.objects.all()
        transaction_data = []
        all_transactions = []
        for transaction in result:
            transaction_data.append(transaction.pk)
            transaction_data.append(transaction.cat_id)
            transaction_data.append(transaction.product_name)
            transaction_data.append(transaction.text)
            transaction_data.append(transaction.image)
            transaction_data.append(transaction.price)
            all_transactions.append(transaction_data)
            transaction_data = []
        return all_transactions

    def get_product_data(self):
        transaction = models.Transactions.objects.get(transaction_id_from_payment=self.trans_id)
        transaction_dict = {'transaction_id': transaction.pk, 'transId': transaction.transaction_id_from_payment,
                            'status': transaction.status, }
        return transaction_dict
