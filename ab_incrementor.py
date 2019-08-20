#
# This pusher executes transactions:
# 1. del a/put b (for b assigns value a+1)
# 2. del b/put a (for a assigns value b+1)
#
# This test needed to clarify the watcher behavior in this case and determine:
# 1. can or not etcd server reorder events
# 2. can or not etcd server drop some events
#    or simplify two transactions [del a/put b] and [del b/put a] into one event: put b
#    (because put b/del b will be occured in the same response in case of events combination to the single response)
#


class ABIncrementor:
    def __init__(self, etcd_client):
        self.__etcd_client = etcd_client

    def run(self):
        self.__etcd_client.delete_prefix('/')

        transaction_count = 0
        self.__etcd_client.put('/a', str(transaction_count))

        for i in range(1000000):
            self.__execute_transaction(transaction_count)
            print('transaction', i)
            transaction_count = transaction_count + 2

    def __execute_transaction(self, transaction_count):
        self.__etcd_client.transaction(
            compare=[
                self.__etcd_client.transactions.value('/a') == str(transaction_count)
            ],
            success=[
                self.__etcd_client.transactions.delete('/a'),
                self.__etcd_client.transactions.put('/b', str(transaction_count + 1))
            ],
            failure=[]
        )

        self.__etcd_client.transaction(
            compare=[
                self.__etcd_client.transactions.value('/b') == str(transaction_count + 1)
            ],
            success=[
                self.__etcd_client.transactions.delete('/b'),
                self.__etcd_client.transactions.put('/a', str(transaction_count + 2))
            ],
            failure=[]
        )
