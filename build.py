#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This file is part of the MindStudio project.
# Copyright (c) 2025 Huawei Technologies Co.,Ltd.
#
# MindStudio is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#
#          http://license.coscl.org.cn/MulanPSL2
#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.
# -------------------------------------------------------------------------

import os
import sys
import logging
import subprocess
import multiprocessing
import argparse


def exec_cmd(cmd):
    result = subprocess.run(cmd, capture_output=False, text=True, timeout=36000)
    if result.returncode != 0:
        logging.error("execute command %s failed, please check the log", " ".join(cmd))
        sys.exit(result.returncode)


def execute_make(build_path, cmake_cmd, make_cmd):
    if not os.path.exists(build_path):
        os.makedirs(build_path, mode=0o755)
    os.chdir(build_path)
    exec_cmd(cmake_cmd)
    exec_cmd(make_cmd)


def execute_test(build_path, test_cmd):
    os.chdir(build_path)
    if test_cmd != "":
        logging.info("============ start to execute C++ code UT test ============")
        exec_cmd(test_cmd)


def execute_python_test(build_path, test_cmd):
    os.chdir(build_path)
    if test_cmd != "":
        logging.info("============ start to execute Python code UT test ============")
        exec_cmd(test_cmd)
        exec_cmd(["coverage3", "xml", "-o", "report/coverage.xml"])
        exec_cmd(["coverage3", "html", "-d", "report"])
        exec_cmd(["coverage3", "report", "-m"])


def create_arg_parser():
    parser = argparse.ArgumentParser(description='Build script with optional testing')
    parser.add_argument('command', nargs='*', default=[],
                        choices=[[], 'local', 'test'],
                        help='Command to execute (python build.py [ |local|test])')
    parser.add_argument('-r', '--revision',
                        help="Build with specific revision or tag")
    return parser


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = create_arg_parser()
    args = parser.parse_args()

    # 1. 参数设置：
    current_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
    cpu_cores = multiprocessing.cpu_count()

    build_path = os.path.join(current_dir, "build")
    cmake_cmd = ["cmake", ".."]
    make_cmd = ["make", "-j", str(cpu_cores), "install"]
    ctest_cmd = ""
    pythontest_cmd = ""

    # ut参数单独设置，使用单独的目录构建，与build区分开，避免相互影响，并传入对应的参数
    if 'test' in args.command:
        build_path = os.path.join(current_dir, "build_ut")
        cmake_cmd.append("-DBUILD_TESTS=ON")
        ctest_cmd = ["./test/csrc_test/mskpp_test_c", "--gtest_output=xml:test_detail.xml"]
        pythontest_cmd = ["coverage3", "run", "--branch", "--source=" + current_dir, "-m", "pytest",
                         current_dir + "/test/cases/", "--junitxml=report/final.xml", "-W", "ignore::DeprecationWarning"] 

    # 2. 更新代码：只有测试构建时才会依赖更新三方代码
    if 'test' in args.command and 'local' not in args.command:
        from download_dependencies import update_submodule
        update_submodule(args)

    # 3. 执行构建
    os.chdir(current_dir)
    execute_make(build_path, cmake_cmd, make_cmd)

    # 4. 执行C代码UT测试
    execute_test(build_path, ctest_cmd)

    # 5. 执行python代码UT测试
    os.environ['PYTHONPATH'] = current_dir + os.pathsep + os.environ.get('PYTHONPATH', '')
    os.environ['PYTHONPYCACHEPREFIX'] = os.getcwd()
    execute_python_test(build_path, pythontest_cmd)
