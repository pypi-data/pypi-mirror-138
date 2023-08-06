from bbcloud_python_sdk.Api.Models.Model import Model


class SubPacketTasks(Model):
    def __init__(self, *args, **kwargs):
        super(SubPacketTasks, self).__init__(*args, **kwargs)
        self._modal_path = 'sub_packet/sub_packet_tasks'
