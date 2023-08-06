from bbcloud_python_sdk.Api.Models.Model import Model


class Phones(Model):
    def __init__(self, *args, **kwargs):
        super(Phones, self).__init__(*args, **kwargs)
        self._modal_path = 'phone/phones'
