# coding=utf-8

import random
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
# l = int(request.GET.get('l','1'))
n = 10
ziyuan = [(u'赢',u'羸'),(u'未',u'末'),(u'暧',u'暖'),(u'肓',u'盲'),(u'夭',u'天')]
obj = random.choice(ziyuan)
grx = list(obj[0]*n)
right = obj[-1]
m = random.randint(1,n)

grx[m-1] = right


print ''.join(grx),len(grx),grx.index(right)+1