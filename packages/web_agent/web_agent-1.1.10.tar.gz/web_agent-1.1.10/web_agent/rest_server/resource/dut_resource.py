# coding=utf-8
import sys
import threading
from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import marshal_with
from rest_server.resource.models.helper import resource_fields
from test_framework.dut.dut import Dut
from test_framework.state import State
from utils import log


PARSER = reqparse.RequestParser()
PARSER.add_argument('name')


class DutResource(Resource):

    def __init__(self):
        pass

    @marshal_with(resource_fields, envelope='resource')
    def post(self):
        log.INFO("REST refresh DUT")
        args = PARSER.parse_args()
        self.start_thread_refresh_dut()
        result = {"msg": "start refresh dut", "state": State.PASS}
        return result

    def start_thread_refresh_dut(self):
        thread_p = threading.Thread(target=self.refresh_dut)
        thread_p.setDaemon(True)
        thread_p.start()

    @staticmethod
    def refresh_dut():
        log.INFO("Start refresh DUT")
        dut = Dut()
        dut.refresh()
        log.INFO("End refresh DUT")
