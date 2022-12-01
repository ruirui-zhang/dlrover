# Copyright 2022 The DLRover Authors. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from abc import ABCMeta, abstractmethod

from typing import List, Dict
from dlrover.python.common.node import NodeGroupResource, NodeResource


class LaunchNode(object):
    def __init__(self, type, node_id, task_id, resource: NodeResource):
        self.type = type
        self.node_id = node_id
        self.task_id = task_id
        self.resource = resource


class ScalePlan(object):
    """The plan to scaler to adjust nodes.
    Attrbutes:
        ndoe_group_resource: the resoruce configuration of a group node.
        launch_nodes: a scaler to launch nodes.
        remove_nodes: a scaler to remove nodes.
        ps_addrs: all add addresses of PS nodes.
    """

    def __init__(self):
        self.node_group_resources: Dict[str, NodeGroupResource] = {}
        self.launch_nodes: List[LaunchNode] = {}
        self.remove_nodes: List[str] = []
        self.ps_addrs: List[str] = []

    def empty(self):
        return len(self.node_group_resources) + len(self.node_resources) == 0

    def merge(self, plan):
        self.node_group_resources.update(plan.node_group_resources)
        self.launch_nodes.extend(plan.launch_nodes)
        self.remove_nodes.extend(plan.remove_nodes)


class Scaler(metaclass=ABCMeta):
    """Scaler is to call cluster scheduler to scale up/down nodes of a job.
    Attributes:
        job_name: string, the name of job.
    """

    def __init__(self, job_name):
        self._job_name = job_name

    @abstractmethod
    def scale(self, plan: ScalePlan):
        """Scale the job with the plan"""
        pass
