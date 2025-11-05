from django.urls import path,include
from . import views
from django.views.generic import TemplateView
# URLパターンを逆引きできるように名前を付ける
app_name = 'enright'

# URLパターンを登録する変数
urlpatterns = [
    # photoアプリへのアクセスはviewsモジュールのIndexViewを実行
    path('',views.IndexView.as_view(), name='index'),

    # 写真投稿ページへのアクセスはviewsモジュールCreatePhotoViewを実行
    path('post/', views.CreatePhotoView.as_view(), name='post'),

    # ★★★ 追加：カテゴリ名をURLに含める投稿ページ ★★★
    # <str:category_title>でカテゴリタイトルをviewsに渡す
    path('post/<str:category_title>/', views.CreatePhotoView.as_view(), name='post_by_title'),

    # 投稿完了ページへのアクセスはviewsモジュールのPostSuccessViewを実行
    path('post_done/',
         views.PostSuccessView.as_view(),
         name='post_done'),
    
    # カテゴリ一覧ページ
    # photos/<Categoryテーブルのid値>にマッチング
    # <int:category>は辞書{category: id値(int)}としてCaregoryViewに渡される
    path('photos/<int:category>',
         views.CategoryView.as_view(),
         name='photos_cat' 
         ),

    # ユーザーの投稿一覧ページ
    # photos/<ユーザーテーブルのid値>にマッチング
    # <int:user>は辞書{user: id値(int)}としてCaregoryViewに渡される
    path('user-list/<int:user>',
         views.UserView.as_view(),
         name='user_list' 
         ),

    # 詳細ページ
    # photos/<Photo postsテーブルのid値>にマッチング
    # <int:pk>は辞書{pk: id値(int)}としてDeteilViewに渡される
    path('photo-detail/<int:pk>',
         views.DetailView.as_view(),
         name='photo_detail' 
         ),
    
    # マイページ
    # mypage/へのアクセスはMypageViewを実行
    path('mypage/',
         views.MypageView.as_view(),    
         name='mypage' 
         ),
     
    # 投稿写真の削除
    # photo/<Photo postsテーブルのid値>/delete/にマッチング
    # <int:pk>は辞書{pk: id値(int)}としてDeteilViewに渡される
    path('photo/<int:pk>/delete/',
         views.PhotoDeleteView.as_view(),
         name='photo_delete' 
         ),
     path('category/', views.CategoryListView.as_view(), name = 'category'),
     path('delete_success/', 
     views.DeleteSuccessView.as_view(), 
     name='delete_success'),

# ----------------------------------------------------
# ★コンテンツ別一覧ページ
# ----------------------------------------------------
path('activity/list/', views.ActivityIndexView.as_view(), name='activity_index'),
path('lecture/list/', views.LectureIndexView.as_view(), name='lecture_index'),
path('disaster/list/', views.DisasterIndexView.as_view(), name='disaster_index'),

] 

