from ... import models
import requests, json


class TransactionHandler:
    def __init__(self, amount=None, transId=None):
        self.amount = amount
        self.transId = transId

    def create_transid(self):
        request = requests.post('https://pay.ir/payment/send', data={'api': 'test', 'amount': self.amount,
                                                                     'redirect': "http://127.0.0.1:8000/payment/", })
        return ("https://pay.ir/payment/gateway/" + str(json.loads(request.text)['transId']),
                json.loads(request.text)['transId'])

    def create_transaction(self):
        try:
            transaction_object = models.Transactions(transaction_id_from_payment=self.transId, amount=self.amount,
                                                     status=0)
            transaction_object.save()
            return transaction_object
        except Exception as e:
            print e
            return 0

    def return_transaction(self):
        trans_object = models.Transactions.objects.get(transaction_id_from_payment=self.transId)
        trans_data = {'amount': trans_object.amount, "trans_id": trans_object.transaction_id_from_payment, "status": trans_object.status}
        return trans_data
