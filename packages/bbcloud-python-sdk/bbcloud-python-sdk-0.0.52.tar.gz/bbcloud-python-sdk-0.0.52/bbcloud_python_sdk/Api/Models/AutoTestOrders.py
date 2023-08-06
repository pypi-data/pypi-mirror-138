from bbcloud_python_sdk.Api.Models.Model import Model


class AutoTestOrders(Model):
    def __init__(self, *args, **kwargs):
        super(AutoTestOrders, self).__init__(*args, **kwargs)
        self._modal_path = 'auto_test/auto_test_orders'
