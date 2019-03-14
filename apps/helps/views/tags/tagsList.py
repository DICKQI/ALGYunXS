from apps.helps.models import Tag
from rest_framework.views import APIView
from operator import itemgetter
from ALGCommon.dictInfo import model_to_dict
from django.http import JsonResponse
from django.db.models import Count


class TagsListView(APIView):

    def get(self, request):
        '''
        获取文章标签列表(热度排名前十的标签)
        :param request:
        :return:
        '''
        tags_all = Tag.objects.annotate(Count('article'))
        tag_count = []
        for i in range(tags_all.count()):
            tag_count.append({'id': tags_all[i].id, 'count': tags_all[i].article__count})

        id = []
        for i in sorted(tag_count, key=itemgetter('count'), reverse=True):
            id.append(i.get('id'))

        tags = [model_to_dict(Tag.objects.get(id=tid), exclude='create_time') for tid in id]

        return JsonResponse({
            'status': True,
            'tags': tags
        })
