from rest_framework.routers import SimpleRouter
from rest_framework.urls import app_name
from materials.apps import MaterialsConfig

from materials.views import CourseViewSet
app_name = 'materials'

router = SimpleRouter()
router.register('',CourseViewSet, basename='courses')

urlpatterns = []
urlpatterns += router.urls