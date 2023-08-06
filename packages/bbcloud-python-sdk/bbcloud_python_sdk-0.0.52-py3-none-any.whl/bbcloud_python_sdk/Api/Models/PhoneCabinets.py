from bbcloud_python_sdk.Api.Models.Model import Model


class PhoneCabinets(Model):
    def __init__(self, *args, **kwargs):
        super(PhoneCabinets, self).__init__(*args, **kwargs)
        self._modal_path = 'phone/phone_cabinets'
