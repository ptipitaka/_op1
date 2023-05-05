from django.urls import path

from . import views

urlpatterns = [
     path('digital-archive/', views.DigitalArchiveView.as_view(), name='digital_archive'),
     path('digital-archive/<int:pk>/', views.DigitalArchiveDetialsView.as_view(), name='digital_archive'),
     path('toc/', views.TocView.as_view(), name='toc'),
     path('toc/<slug:slug>/structure/', views.StructureView.as_view(), name='structure'),
     path('toc/<slug:slug>/structure/<int:structure_id>/common-reference/',
          views.CommonReferenceSubformView.as_view(), name='common_reference_subform'),
     path('toc/<slug:slug>/structure/<int:structure_id>/common-reference/<int:pk>/',
          views.CommonReferenceSubformDetailView.as_view(), name='common_reference_subform_detail'),
     path('toc/<slug:slug>/structure/<int:structure_id>/common-reference/<int:pk>/delete',
          views.CommonReferenceSubformDeleteView.as_view(), name='common_reference_subform_delete'),
]
