from django.urls import path
from . import views
from django.views.generic import TemplateView
# URLパターンを逆引きできるように名前を付ける
app_name = 'enright'

# URLパターンを登録する変数
urlpatterns = [
    # トップページ
    path('', views.IndexView.as_view(), name='index'),

    # 写真投稿ページへのアクセスはviewsモジュールCreatePhotoViewを実行
    path('post/', views.CreatePhotoView.as_view(), name='post'),

    # 投稿完了ページへのアクセスはviewsモジュールのPostSuccessViewを実行
    path('post_done/',
         views.PostSuccessView.as_view(),
         name='post_done'),
    
    # 削除完了ページ
    path('delete_done/',
         views.DeleteSuccessView.as_view(),
         name='delete_done'),
    
    # カテゴリ一覧ページ (IDによる絞り込み)
    # ★★★ 修正箇所1: スラッシュを追加
    path('photos/<int:category>/', 
         views.CategoryView.as_view(),
         name='photos_cat' 
         ),

    # ユーザーの投稿一覧ページ
    # ★★★ 修正箇所2: スラッシュを追加
    path('user-list/<int:user>/', 
         views.UserView.as_view(),
         name='user_list' 
         ),

    # 詳細ページ
    path('photo-detail/<int:pk>/', # 元々スラッシュがありましたが、念のため確認
         views.DetailView.as_view(),
         name='photo_detail' 
         ),
    
    # マイページ
    path('mypage/',
         views.MypageView.as_view(),
         name='mypage' 
         ),
      
    # 投稿写真の削除
    path('photo/<int:pk>/delete/',
         views.PhotoDeleteView.as_view(),
         name='photo_delete' 
         ),
     path('category/', views.CategoryListView.as_view(), name = 'category'),

# enright/urls.py のurlpatternsに追加

# ... (既存のurlpatterns) ...

# ----------------------------------------------------
# ★コンテンツ別一覧ページ
# ----------------------------------------------------
path('activity/list/', views.ActivityIndexView.as_view(), name='activity_index'),
path('lecture/list/', views.LectureIndexView.as_view(), name='lecture_index'),
path('disaster/list/', views.DisasterIndexView.as_view(), name='disaster_index'),

] # urlpatterns の閉じカッコ


