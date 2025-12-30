#!/usr/bin/python
# -*- coding: UTF-8 -*-
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

from mskpp.utils import logger
from .output_tool import SAVE_DATA_FILE_AUTHORITY


class DataVisualization():
    @staticmethod
    def cycle_info_visualization(label_list, cycle_list, title_name, data_file_name):
        try:
            import plotly
            import plotly.graph_objs as go
        except ImportError:
            logger.warning("Plotly is not installed, if you want to visualize data, please install it")
            return
        else:
            fig = go.Figure()
            fig.add_trace(go.Pie(labels=label_list, values=cycle_list))
            fig.update_layout(title=go.layout.Title(text=title_name, x=0.5), width=500, height=500)
            plotly.offline.plot(fig, auto_open=False, filename=data_file_name)
            os.chmod(path=data_file_name, mode=SAVE_DATA_FILE_AUTHORITY)