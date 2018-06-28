# coding=utf-8
from aliyunsdkcore import client
from aliyunsdkcr.request.v20160607 import GetImageLayerRequest,DeleteNamespaceRequest,CreateNamespaceRequest,GetNamespaceListRequest,GetNamespaceRequest,GetRepoListRequest,GetRepoTagsRequest
import json
# 设置Client
# client.region_provider.add_endpoint("cr", "cn-beijing", "cr.cn-beijing.aliyuncs.com")
# apiClient = client.AcsClient('LTAILPtWDD74MNzv', 'ivWRuqRoCJAAnnUUSvoHNGWZJwAIGc', 'cn-beijing')
# # 获取所有的镜像列表并解析
# # request = GetRepoListRequest.GetRepoListRequest()
# # response = apiClient.do_action(request)
# # repos = json.loads(response)
# # # print(repos)
# # data = {}
# # repositories = []
# # for name in repos.get('data').get('repos'):
# #     repositories.append(name.get('repoName'))
# # data["repositories"] = repositories
#
# request = GetRepoTagsRequest.GetRepoTagsRequest()
# request.set_RepoName("django1.11")
# request.set_RepoNamespace('uhongedu')
# response = apiClient.do_action(request)
# print(json.loads(response))
a = {"a":1}
print(dir(a))
print(a.keys())