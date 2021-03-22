from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'match', views.MatchView, basename='match')
urlpatterns = router.urls
