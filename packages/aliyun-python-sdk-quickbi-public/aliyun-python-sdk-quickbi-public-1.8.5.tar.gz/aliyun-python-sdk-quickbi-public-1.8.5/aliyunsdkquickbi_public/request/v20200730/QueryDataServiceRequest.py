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
from aliyunsdkquickbi_public.endpoint import endpoint_data

class QueryDataServiceRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'quickbi-public', '2020-07-30', 'QueryDataService','quickbi')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_ReturnFields(self):
		return self.get_query_params().get('ReturnFields')

	def set_ReturnFields(self,ReturnFields):
		self.add_query_param('ReturnFields',ReturnFields)

	def get_Conditions(self):
		return self.get_query_params().get('Conditions')

	def set_Conditions(self,Conditions):
		self.add_query_param('Conditions',Conditions)

	def get_ApiId(self):
		return self.get_query_params().get('ApiId')

	def set_ApiId(self,ApiId):
		self.add_query_param('ApiId',ApiId)