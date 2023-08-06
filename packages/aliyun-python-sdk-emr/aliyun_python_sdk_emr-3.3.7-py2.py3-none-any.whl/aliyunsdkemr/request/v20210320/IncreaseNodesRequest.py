# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdkemr.endpoint import endpoint_data

class IncreaseNodesRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Emr', '2021-03-20', 'IncreaseNodes','emr')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_AutoPayOrder(self):
		return self.get_query_params().get('AutoPayOrder')

	def set_AutoPayOrder(self,AutoPayOrder):
		self.add_query_param('AutoPayOrder',AutoPayOrder)

	def get_NodeGroupList(self):
		return self.get_query_params().get('NodeGroupList')

	def set_NodeGroupList(self,NodeGroupList):
		self.add_query_param('NodeGroupList',NodeGroupList)

	def get_NodeGroups(self):
		return self.get_query_params().get('NodeGroups')

	def set_NodeGroups(self,NodeGroups):
		self.add_query_param('NodeGroups',NodeGroups)

	def get_ApplicationConfigs(self):
		return self.get_query_params().get('ApplicationConfigs')

	def set_ApplicationConfigs(self,ApplicationConfigs):
		self.add_query_param('ApplicationConfigs',ApplicationConfigs)

	def get_ClusterId(self):
		return self.get_query_params().get('ClusterId')

	def set_ClusterId(self,ClusterId):
		self.add_query_param('ClusterId',ClusterId)

	def get_Promotions(self):
		return self.get_query_params().get('Promotions')

	def set_Promotions(self,Promotions):
		self.add_query_param('Promotions',Promotions)