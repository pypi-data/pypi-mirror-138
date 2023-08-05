#!/usr/bin/env python
# coding=utf-8
import os
import sys
import yaml
import argparse
sys.path.append(os.path.join(os.path.dirname(__file__)))
from rest_server.reset_server import *
from rest_server.resource.models.ftp_server import thread_start_ftp_server
from test_framework.test_pool import TestPool
from utils.excel import ExcelHandle
from test_framework.database.dut_database import DutDatabase


def add_sub_argument_group(subparsers, name, handler_function):
    regression_parser = subparsers.add_parser(name, help='%s tests executor'%name)
    regression_required_arguments = regression_parser.add_argument_group('required arguments')
    regression_required_arguments.add_argument('--port', '-p', type=str, default="5000",
                                               help='start server port id', required=False)
    regression_required_arguments.add_argument('--work_path', '-w', type=str, default="",
                                               help='automation platform path, test-platform or perses', required=False)
    regression_required_arguments.add_argument('--platform', '-pl', type=str, default="",
                                               help='host platform: oakgate or linux', required=False)
    regression_required_arguments.add_argument('--excel', '-e', type=str, default="",
                                               help='oakgate config excel file', required=False)
    regression_parser.set_defaults(executor_function=handler_function)


def create_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    add_sub_argument_group(subparsers, 'start', start_rest_server)
    add_sub_argument_group(subparsers, 'db', update_db)
    return parser


def update_db(args):
    dut_db = DutDatabase()
    configs = ExcelHandle.get_ogt_config(args.excel)
    # dut_db.update_slot_agent_2_id()
    dut_db.set_ogt_config_2_slot(configs)


def start_rest_server(args):
    _ = TestPool()
    thread_start_ftp_server()
    APP.run(host="0.0.0.0", port=args.port)


def load_global_config():
    config_file = os.path.join(os.getcwd(), 'config.yml')
    if os.path.exists(config_file):
        conf = yaml.load(open(config_file).read(), Loader=yaml.FullLoader)
        for key, val in conf.items():
            os.environ[key] = val


def get_work_path(args):
    work_path = os.getcwd()
    if args.work_path != "":
        if os.path.exists(args.work_path):
            work_path = args.work_path
    return work_path


def add_globals(args):
    load_global_config()
    os.environ["root_path"] = os.path.join(os.path.dirname(__file__))
    os.environ["working_path"] = get_work_path(args)
    os.environ["agent_port"] = args.port
    os.environ["platform"] = args.platform


def run():
    parser = create_parser()
    args = parser.parse_args()
    try:
        add_globals(args)
        args.executor_function(args)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    run()
