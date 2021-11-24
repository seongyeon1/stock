from django.views.generic import ListView, DetailView
from .models import News

#-- ListView
class NewsList(ListView):
    model = News
    paginate_by = 4
    template_name = 'news/news_list.html'  # DEFAULT : <app_label>/<model_name>_list.html
    context_object_name = 'news_list'  # DEFAULT : <app_label>_list

    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        news_list = News.objects.order_by('-id')

        if search_keyword:
            if len(search_keyword) > 1:
                if search_type == 'all':
                    search_news_list = news_list.filter(
                        Q(title__icontains=search_keyword) | Q(content__icontains=search_keyword) | Q(
                            ticker__icontains=search_keyword))
                elif search_type == 'title_content':
                    search_news_list = news_list.filter(
                        Q(title__icontains=search_keyword) | Q(content__icontains=search_keyword))
                elif search_type == 'title':
                    search_news_list = news_news.filter(title__icontains=search_keyword)
                elif search_type == 'content':
                    search_news_list = news_list.filter(content__icontains=search_keyword)
                elif search_type == 'ticker':
                    search_news_list = news_list.filter(ticker__icontains=search_keyword)

                if not search_news_list :
                    messages.error(self.request, '일치하는 검색 결과가 없습니다.')
                return search_news_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return news_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        news_fixed = News.objects.filter().order_by('-released_date')

        if len(search_keyword) > 1:
            context['q'] = search_keyword
        context['type'] = search_type
        context['notice_fixed'] = news_fixed

        return context

#-- DetailView
class NewsDetail(DetailView):
    model = News
    template_name = 'news/news_detail.html'