
from test_framework.dut.sub_slot.oakgate_slot import OakgateSlot
from test_framework.dut.sub_slot.linux_slot import LinuxSlot
from test_framework.database.dut_database import DutDatabase
from utils.system import get_platform
from utils import log


class Slot(object):

    def __init__(self, agent):
        self.agent = agent
        self.agent_name = self.agent.get_agent_name()
        self.db_client = DutDatabase()
        self.platform = get_platform()

    def refresh(self):
        agent_id = self.db_client.get_agent_id(self.agent.ip_address, self.agent.port)
        if agent_id is not None:
            slots = self.db_client.get_agent_related_slots_by_id(agent_id)
            if self.platform == "oakgate":
                self.oakgate_refresh(slots, agent_id)
            else:
                self.linux_refresh(slots, agent_id)
        else:
            log.ERR("Slot is not find Agent: {}".format(";".join(self.agent.ip_address)))

    @staticmethod
    def oakgate_refresh(slots, agent_id):
        oak_slot = OakgateSlot(slots, agent_id)
        oak_slot.refresh_all()

    @staticmethod
    def linux_refresh(slots, agent_id):
        slot = LinuxSlot(slots, agent_id)
        slot.refresh_all()
