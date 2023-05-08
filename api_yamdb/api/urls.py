from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import reviews, users

router = DefaultRouter()

router.register('users', users.UserViewSet)
router.register('titles', reviews.TitleViewSet)
router.register('genres', reviews.GenreViewSet)
router.register('categories', reviews.CategoryViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews',
                reviews.ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    reviews.CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/auth/signup/', users.SignupView.as_view(), name='signup'),
    path('v1/auth/token/', users.CustomJWT.as_view(), name='token'),
    path('v1/', include(router.urls), name='api_v1'),
]
