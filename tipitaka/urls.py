from django.urls import path

from . import views

urlpatterns = [
    path('digital-archive', views.DigitalArchiveView.as_view(), name='digital_archive'),
    path('digital-archive/<int:pk>', views.DigitalArchiveDetialsView.as_view(), name='digital_archive'),
    path('toc/', views.TocView.as_view(), name='toc'),
    path('structure/<slug:slug>/', views.StructureView.as_view(), name='structure'),
    path('structure/<slug:slug>/common-reference/', views.CommonReferenceSubformView.as_view(), name='common_reference_subform'),
]
