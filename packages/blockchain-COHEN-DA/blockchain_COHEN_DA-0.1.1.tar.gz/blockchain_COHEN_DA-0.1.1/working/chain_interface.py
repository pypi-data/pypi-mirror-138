class ChainInterface():
    def get_transactions(self, address):
        raise Exception('This function must be implemented by all classes inheriting from ChainInterface')

