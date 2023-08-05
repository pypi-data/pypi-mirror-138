
import os
import platform
from utils.system import get_multi_ip_address, get_platform, get_host_name
from test_framework.database.dut_database import update_agent


class Agent(object):

    def __init__(self):
        self.ip_address = get_multi_ip_address()
        self.port = os.environ.get('agent_port', '5000')

    def get_agent_info(self):
        agent_info = dict()
        agent_info["name"] = get_host_name()
        agent_info["ip"] = ";".join(self.ip_address)
        agent_info["port"] = self.port
        agent_info["os"] = "windows" if platform.system() == 'Windows' else "linux"
        agent_info["platform"] = get_platform()
        return agent_info

    @staticmethod
    def get_agent_name():
        return get_host_name()

    @update_agent
    def refresh(self):
        return self.get_agent_info()


if __name__ == '__main__':
    ag = Agent()
    ag.refresh()
