# pylint: disable=broad-except, invalid-name
import os
from utils import log
from test_framework.database.database import SqlConnection
from test_framework.state import SlotState
from utils.system import get_host_name, get_multi_ip_address


class DutDatabase(SqlConnection):

    def __init__(self):
        super(DutDatabase, self).__init__(db_name="dutdb")
        self.ip_address = get_multi_ip_address()
        self.port = os.environ.get('agent_port', '5000')
        self.agent_table = "agent"
        self.slot_table = "slot"

    def update_agent(self, agent):
        agent_id = self.get_agent_id(self.ip_address, self.port)
        if agent_id is not None:
            self.update_exist_agent(agent, agent_id)
        else:
            self.create_new_agent(agent)

    def update_slot(self, slot_id, slot):
        if slot_id != -1:
            self.update_exist_slot(slot_id, slot)
        else:
            self.create_new_slot(slot)

    def update_exist_slot(self, slot_id, slot):
        update_str = self._covert_dict_2_update_string(**slot)
        update_command = "UPDATE {} SET {} where `id`='{}'".format(self.slot_table, update_str, slot_id)
        self.cursor.execute(update_command)
        self.conn.commit()

    def create_new_slot(self, slot):
        col_str, value_str = self._covert_dict_2_insert_string(**slot)
        insert_command = "INSERT INTO `{}` ({}) VALUES({})".format(self.slot_table, col_str, value_str)
        self.cursor.execute(insert_command)
        self.conn.commit()

    def is_exist_agent(self, ip_addresses, port):
        result = False
        for ip in ip_addresses:
            sql_command = "SELECT * from {} WHERE ip like'%{}%' AND port='{}'".format(self.agent_table, ip, port)
            gets = self.execute_sql_command(sql_command)
            if gets:
                result = True
                break
        return result

    def get_agent_id(self, ip_addresses, port):
        agent_id = None
        for ip in ip_addresses:
            sql_command = "SELECT * from {} WHERE ip like'%{}%' AND port='{}'".format(self.agent_table, ip, port)
            get_agents = self.execute_sql_command(sql_command)
            for item in get_agents:
                db_ip_list = item[3].split(";")
                if ip in db_ip_list:
                    agent_id = item[0]
                    break
        return agent_id

    def is_exist_slot(self, ogt_config, agent_id):
        sql_command = "SELECT * from {} WHERE config_name='{}' AND agent='{}'".format(self.slot_table, ogt_config, agent_id)
        gets = self.execute_sql_command(sql_command)
        result = True if gets else False
        return result

    def update_exist_agent(self, agent, agent_id):
        str_date = "`os`='{}',`platform`='{}',`ip`='{}',`name`='{}'".format(agent["os"], agent["platform"], agent["ip"],
                                                                            agent["name"])
        cmd = "UPDATE {} SET {} WHERE `id`='{}'".format(self.agent_table, str_date, agent_id)
        self.cursor.execute(cmd)
        self.conn.commit()

    def create_new_agent(self, agent):
        self.insert_to_table(self.agent_table,
                             name=agent["name"],
                             ip=agent["ip"],
                             port=agent["port"],
                             os=agent["os"],
                             platform=agent["platform"])

    def get_agent_related_slots(self, agent):
        cmd = "SELECT * FROM {} where agent='{}'".format(self.slot_table, agent)
        result = self.execute_sql_command(cmd)
        return result

    def get_agent_related_slots_by_id(self, agent_id):
        cmd = "SELECT * FROM {} where `agent`='{}'".format(self.slot_table, agent_id)
        result = self.execute_sql_command(cmd)
        return result

    def agent_heart_beat(self, state):
        update_time = self.get_datetime()
        agent_id = self.get_agent_id(self.ip_address, self.port)
        status = "`status`='{}', update_time='{}'".format(state, update_time)
        update_command = "UPDATE {} SET {} WHERE `id`='{}'".format(self.agent_table, status, agent_id)
        self.cursor.execute(update_command)
        self.conn.commit()

    def delete_removed_slot(self, slot_id):
        if slot_id is not None:
            update_command = "DELETE FROM {} WHERE `id`='{}'".format(self.slot_table, slot_id)
            self.cursor.execute(update_command)
            self.conn.commit()

    def set_slot_to_lost(self, slot_id):
        if slot_id is not None:
            log.INFO("Find slot is lost: {}".format(slot_id))
            cmd = "UPDATE  {} SET `status`='{}' WHERE `id`='{}'".format(self.slot_table, SlotState.Lost, slot_id)
            self.cursor.execute(cmd)
            self.conn.commit()

    def get_all_agents(self):
        sql_cmd = "SELECT * from {} ".format(self.agent_table)
        agents = self.execute_sql_command(sql_cmd)
        return agents

    def get_all_slots(self):
        sql_cmd = "SELECT * from {} ".format(self.slot_table)
        slots = self.execute_sql_command(sql_cmd)
        return slots

    @staticmethod
    def map_agent_name_2_id(agent_name, all_agents):
        agent_id = None
        for agent in all_agents:
            if agent[1] == agent_name:
                agent_id = agent[0]
                break
        return agent_id

    def update_slot_agent_2_id(self):
        agents = self.get_all_agents()
        slots = self.get_all_slots()
        for slot in slots:
            agent_name = slot[15]
            agent_id = self.map_agent_name_2_id(agent_name, agents)
            if agent_id is not None:
                cmd = "UPDATE  {} SET `agent`='{}' WHERE `id`='{}'".format(self.slot_table, agent_id, slot[0])
                self.cursor.execute(cmd)
                self.conn.commit()

    def set_ogt_config_2_slot(self, configs):
        for config in configs:
            ip = config["ip"]
            ogt_config = config["ogt_config"]
            ip_list = list()
            ip_list.append(ip)
            agent_id = self.get_agent_id(ip_list, "5000")
            if agent_id is None:
                agent = {"name": "", "ip": ip, "port": "5000", "os": "windows", "platform": "oakgate"}
                self.create_new_agent(agent)
                agent_id = self.get_agent_id(ip_list, "5000")
            if self.is_exist_slot(ogt_config, agent_id) is False:
                slot = {"agent": agent_id, "config_name": ogt_config}
                self.create_new_slot(slot)


def update_agent(func):
    def func_wrapper(*args, **kwargs):
        agent = func(*args, **kwargs)
        try:
            sql_connection = DutDatabase()
            sql_connection.update_agent(agent)
        except Exception as all_exception:
            log.ERR(all_exception)
        return agent
    return func_wrapper


def update_slot(func):
    def func_wrapper(*args, **kwargs):
        slot_id, slot = func(*args, **kwargs)
        if slot is not None:
            try:
                sql_connection = DutDatabase()
                sql_connection.update_slot(slot_id, slot)
            except Exception as all_exception:
                log.ERR(all_exception)
        return slot_id, slot
    return func_wrapper


def agent_heart_beat(func):
    def func_wrapper(*args, **kwargs):
        status = func(*args, **kwargs)
        try:
            sql_connection = DutDatabase()
            sql_connection.agent_heart_beat(status)
        except Exception as all_exception:
            log.ERR(all_exception)
        return status
    return func_wrapper


def delete_removed_slot(func):
    def func_wrapper(*args, **kwargs):
        slot_id = func(*args, **kwargs)
        try:
            sql_connection = DutDatabase()
            sql_connection.delete_removed_slot(slot_id)
        except Exception as all_exception:
            log.ERR(all_exception)
        return slot_id
    return func_wrapper


def check_lost_slot(func):
    def func_wrapper(*args, **kwargs):
        slot_id = func(*args, **kwargs)
        try:
            sql_connection = DutDatabase()
            sql_connection.set_slot_to_lost(slot_id)
        except Exception as all_exception:
            log.ERR(all_exception)
        return slot_id
    return func_wrapper


if __name__ == '__main__':
    a = DutDatabase()
    b = a.get_agent_id(["10.124.126.234"], "5000")
    pass