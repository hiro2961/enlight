from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# .modelsからPhotoPost, Categoryをインポート
from .models import PhotoPost, Category
# .formsからPhotoPostForm, SearchFormをインポート
from .forms import PhotoPostForm, SearchForm


# =======================================================================
# 投稿関連ビュー
# =======================================================================

@method_decorator(login_required, name='dispatch')
class ActivityCreateView(CreateView):
    '''活動情報専用投稿ページのビュー (Category: 活動情報)'''
    form_class = PhotoPostForm
    template_name = "post_photo.html"
    success_url = reverse_lazy('enright:post_done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '活動情報' 
        return context

    def form_valid(self, form):
        postdata = form.save(commit=False)
        postdata.user = self.request.user
        
        try:
            activity_category = Category.objects.get(title='活動情報')
            postdata.category = activity_category
        except Category.DoesNotExist:
             # カテゴリが存在しない場合の処理を実装してください
             pass 
        
        postdata.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class LectureCreateView(CreateView):
    '''講義情報専用投稿ページのビュー (Category: 講義情報)'''
    form_class = PhotoPostForm
    template_name = "post_photo.html"
    success_url = reverse_lazy('enright:post_done')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '講義情報'
        return context

    def form_valid(self, form):
        postdata = form.save(commit=False)
        postdata.user = self.request.user
        try:
            lecture_category = Category.objects.get(title='講義情報')
            postdata.category = lecture_category
        except Category.DoesNotExist:
             pass 
             
        postdata.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class DisasterCreateView(CreateView):
    '''災害対策情報専用投稿ページのビュー (Category: 災害対策情報)'''
    form_class = PhotoPostForm
    template_name = "post_photo.html"
    success_url = reverse_lazy('enright:post_done')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '災害対策情報'
        return context

    def form_valid(self, form):
        postdata = form.save(commit=False)
        postdata.user = self.request.user
        try:
            disaster_category = Category.objects.get(title='災害対策情報')
            postdata.category = disaster_category
        except Category.DoesNotExist:
             pass 
             
        postdata.save()
        return super().form_valid(form)


class PostSuccessView(TemplateView):
    '''投稿完了ページのビュー'''
    template_name = 'post_success.html'

# ★★★ 修正箇所1: 削除完了ビューを追加 ★★★
class DeleteSuccessView(TemplateView):
    '''削除完了ページのビュー'''
    template_name = 'delete_success.html' 


# =======================================================================
# 一覧・詳細関連ビュー
# =======================================================================

class IndexView(ListView):
    '''トップページ(全投稿)のビュー'''
    model = PhotoPost
    template_name = 'index.html'
    paginate_by = 9 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET)
        context['activity_posts'] = PhotoPost.objects.filter(category__title='活動情報').order_by('-posted_at')[:3]
        context['lecture_posts'] = PhotoPost.objects.filter(category__title='講義情報').order_by('-posted_at')[:3]
        context['disaster_posts'] = PhotoPost.objects.filter(category__title='災害対策情報').order_by('-posted_at')[:3]
        context['page_title'] = 'トップページ'
        return context
    
    def get_queryset(self):
        queryset = PhotoPost.objects.order_by('-posted_at')
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(comment__icontains=keyword) 
            )
        return queryset


class CategoryView(ListView):
    '''カテゴリページのビュー'''
    template_name = 'index.html'
    paginate_by = 9
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET)
        return context

    def get_queryset(self):
        category_id = self.kwargs['category']
        categories = PhotoPost.objects.filter(
            category=category_id).order_by('-posted_at')
        return categories

class UserView(ListView):
    '''ユーザーの投稿一覧ページ'''
    template_name = 'index.html'
    paginate_by = 12
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET)
        return context

    def get_queryset(self):
        user_id = self.kwargs['user']
        user_list = PhotoPost.objects.filter(
            user=user_id).order_by('-posted_at')
        return user_list

class DetailView(DetailView):
    '''詳細ページのビュー'''
    template_name = 'detail.html'
    model = PhotoPost


class MypageView(ListView):
    '''マイページのビュー'''
    template_name = 'mypage.html'
    paginate_by = 9

    def get_queryset(self):
        queryset = PhotoPost.objects.filter(
            user=self.request.user).order_by('-posted_at')
        return queryset
    
class PhotoDeleteView(DeleteView):
    '''レコードの削除を行うビュー'''
    model = PhotoPost
    template_name = 'photo_delete.html'
    # ★★★ 修正箇所2: 削除完了ページにリダイレクトするよう変更 ★★★
    success_url = reverse_lazy('enright:delete_done')

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
class CategoryListView(ListView):
    '''カテゴリー一覧表示ページ'''
    template_name ='category.html'
    paginate_by = 12

    def get_queryset(self):
        queryset = PhotoPost.objects.filter(
            user=self.request.user).order_by('-posted_at')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Categoryモデルから全てのカテゴリーを取得し、コンテキストに追加
        context['categories'] = Category.objects.all().order_by('title') 
        return context

# ----------------------------------------------------
# カテゴリ別一覧ページ用ビュー
# ----------------------------------------------------
class ActivityIndexView(ListView): 
    model = PhotoPost
    template_name = 'cat_index.html'
    paginate_by = 9 

    def get_queryset(self):
        return PhotoPost.objects.filter(category__title='活動情報').order_by('-posted_at')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '活動情報' 
        context['form'] = SearchForm(self.request.GET) 
        return context


class LectureIndexView(ListView):
    model = PhotoPost
    template_name = 'cat_index.html'
    paginate_by = 9 

    def get_queryset(self):
        return PhotoPost.objects.filter(category__title='講義情報').order_by('-posted_at')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '講義情報'
        context['form'] = SearchForm(self.request.GET)
        return context


class DisasterIndexView(ListView):
    model = PhotoPost
    template_name = 'cat_index.html'
    paginate_by = 9 

    def get_queryset(self):
        return PhotoPost.objects.filter(category__title='災害対策情報').order_by('-posted_at')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '災害対策情報'
        context['form'] = SearchForm(self.request.GET)
        return context