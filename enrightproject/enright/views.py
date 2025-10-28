from django.shortcuts import render
# django.views.genericからTemplateView、ListViewをインポート
from django.views.generic import TemplateView, ListView

# django.views.genericからCreateViewをインポート
from django.views.generic import CreateView

# django.urlsからreverse_lazyをインポート
from django.urls import reverse_lazy

# formsモジュールからPhotoPostFormをインポート
from .forms import PhotoPostForm

# method_decoratorをインポート
from django.utils.decorators import method_decorator

# login_requiredをインポート
from django.contrib.auth.decorators import login_required

# modelsモジュールからモデルPhotoPostをインポート
from .models import PhotoPost

# django.views.genericからDetailViewをインポート
from django.views.generic import DetailView

# django.views.genericからDeleteViewをインポート
from django.views.generic import DeleteView

from django.db.models import Q
from .forms import SearchForm
from .models import Category


class IndexView(ListView):
    '''トップページ(全投稿)のビュー
    '''
    # モデルの定義
    model = PhotoPost
    # レンダリングするテンプレート
    template_name = 'index.html'
    # 1ページに表示するレコードの件数
    paginate_by = 9 

    # テンプレートに渡すデータ（コンテキスト）をオーバーライド
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 検索フォームをコンテキストに追加 (既存のロジック)
        context['form'] = SearchForm(self.request.GET)
        
        # ★★★ 各カテゴリの最新投稿を3件ずつ取得 ★★★
        
        # 1. 活動情報
        context['activity_posts'] = PhotoPost.objects.filter(
            category__title='活動情報'
        ).order_by('-posted_at')[:3]

        # 2. 講義情報
        context['lecture_posts'] = PhotoPost.objects.filter(
            category__title='講義情報'
        ).order_by('-posted_at')[:3]

        # 3. 災害対策情報
        context['disaster_posts'] = PhotoPost.objects.filter(
            category__title='災害対策情報'
        ).order_by('-posted_at')[:3]
        
        context['page_title'] = 'トップページ'

        return context
    
    # トップページでの検索を可能にするため
    def get_queryset(self):
        queryset = PhotoPost.objects.order_by('-posted_at')
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(comment__icontains=keyword) 
            )
        return queryset


# デコレーターにより、CreatePhotoViewへのアクセスはログインユーザに限定される
@method_decorator(login_required, name='dispatch')
class CreatePhotoView(CreateView):
    '''写真投稿ページのビュー'''
    # forms.pyのPhotoPostFormをフォームクラスとして登録
    form_class = PhotoPostForm
    # レンダリングするテンプレート
    template_name = "post_photo.html"
    # フォームデータ登録完了後のリダイレクト先
    success_url = reverse_lazy('enright:post_done')

    def form_valid(self, form):
        '''CreateViewクラスのform_valid()をオーバーライド'''
        # commit=FalseにしてPOSTされたデータを取得
        postdata = form.save(commit=False)
        # 投稿ユーザーのidを取得してモデルのuserフィールドに格納
        postdata.user = self.request.user
        # 投稿データをデータベースに登録
        postdata.save()
        return super().form_valid(form)

class PostSuccessView(TemplateView):
    '''投稿完了ページのビュー'''
    # post_success.htmlをレンダリングする
    template_name = 'post_success.html'

class CategoryView(ListView):
    '''カテゴリページのビュー (単一のカテゴリIDによる絞り込み)'''
    # index.htmlをレンダリングする
    template_name = 'index.html'
    # 1ページに表示するレコードの件数
    paginate_by = 9
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET)
        return context

    def get_queryset(self):
        '''クエリを実行する (カテゴリIDによる絞り込み)'''
        category_id = self.kwargs['category']
        categories = PhotoPost.objects.filter(
            category=category_id).order_by('-posted_at')
        return categories

class UserView(ListView):
    '''ユーザーの投稿一覧ページ'''
    # index.htmlをレンダリングする
    template_name = 'index.html'
    # 1ページに表示するレコードの件数
    paginate_by = 12
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET)
        return context


    def get_queryset(self):
        '''クエリを実行する (ユーザーIDによる絞り込み)'''
        user_id = self.kwargs['user']
        user_list = PhotoPost.objects.filter(
            user=user_id).order_by('-posted_at')
        return user_list

class DetailView(DetailView):
    '''詳細ページのビュー'''
    # detail.htmlをレンダリングする
    template_name = 'detail.html'
    # クラス変数modelにモデルBlogPostを設定
    model = PhotoPost


class MypageView(ListView):
    '''マイページのビュー'''
    # mypage.htmlをレンダリングする
    template_name = 'mypage.html'
    # 1ページに表示するレコードの件数
    paginate_by = 9

    def get_queryset(self):
        '''クエリを実行する (ログインユーザーによる絞り込み)'''
        # ufilter(userフィールド=userオブジェクト)で絞り込む
        queryset = PhotoPost.objects.filter(
            user=self.request.user).order_by('-posted_at')
        return queryset
    
class PhotoDeleteView(DeleteView):
    '''レコードの削除を行うビュー'''
    #　操作の対象はPhotoPostモデル
    model = PhotoPost
    # photo_delete.htmlをレンダリングする
    template_name = 'photo_delete.html'
    # 処理完了後にマイページにリダイレクト
    success_url = reverse_lazy('enright:mypage')

    def delete(self, request, *args, **kwargs):
        '''レコードの削除を実行'''
        return super().delete(request, *args, **kwargs)
    
class CategoryListView(ListView):
    '''カテゴリー一覧表示ページ (Categoryモデルの一覧)'''
    template_name ='category.html'
    paginate_by = 12

    def get_queryset(self):
        # CategoryListViewで投稿をフィルタリングするロジックは通常不要だが、既存コードを保持
        # ただし、CategoryListViewでPhotoPostをフィルタリングするのは一般的ではない
        queryset = PhotoPost.objects.filter(
            user=self.request.user).order_by('-posted_at')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Categoryモデルから全てのカテゴリーを取得し、コンテキストに追加
        context['categories'] = Category.objects.all().order_by('title') 
        return context

# ----------------------------------------------------
# ★カテゴリ別一覧ページ用ビュー (テンプレート名を 'cat_index.html' に修正)
# ----------------------------------------------------
class ActivityIndexView(ListView): 
    model = PhotoPost
    template_name = 'cat_index.html' # ★★★ 修正済み ★★★
    paginate_by = 9 

    def get_queryset(self):
        # '活動情報'カテゴリの投稿のみをフィルタリング
        return PhotoPost.objects.filter(category__title='活動情報').order_by('-posted_at')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '活動情報' 
        context['form'] = SearchForm(self.request.GET) 
        return context


class LectureIndexView(ListView):
    model = PhotoPost
    template_name = 'cat_index.html' # ★★★ 修正済み ★★★
    paginate_by = 9 

    def get_queryset(self):
        # '講義情報'カテゴリの投稿のみをフィルタリング
        return PhotoPost.objects.filter(category__title='講義情報').order_by('-posted_at')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '講義情報'
        context['form'] = SearchForm(self.request.GET)
        return context


class DisasterIndexView(ListView):
    model = PhotoPost
    template_name = 'cat_index.html' # ★★★ 修正済み ★★★
    paginate_by = 9 

    def get_queryset(self):
        # '災害対策情報'カテゴリの投稿のみをフィルタリング
        return PhotoPost.objects.filter(category__title='災害対策情報').order_by('-posted_at')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '災害対策情報'
        context['form'] = SearchForm(self.request.GET)
        return context