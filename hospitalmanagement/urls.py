from django.contrib import admin
from django.urls import path
from hospital import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    # path('admin', admin.site.urls),
    path('',views.home_view,name=''),
    
    path('contactus', views.contactus_view),


    path('adminclick', views.adminclick_view),
    path('doctorclick', views.doctorclick_view),
    path('fdo', views.fdoclick_view),
    path('deo', views.deoclick_view),


    path('adminsignup', views.admin_signup_view),

    
    path('adminlogin', LoginView.as_view(template_name='hospital/adminlogin.html')),
    path('doctorlogin', LoginView.as_view(template_name='hospital/doctorlogin.html')),
    path('fdologin', LoginView.as_view(template_name='hospital/fdologin.html')),
    path('deologin', LoginView.as_view(template_name='hospital/deologin.html')),


    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='hospital/index.html'),name='logout'),


    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('fdo-dashboard', views.fdo_dashboard_view,name='fdo-dashboard'),
    path('deo-dashboard', views.deo_dashboard_view,name='deo-dashboard'),

    path('admin-doctor', views.admin_doctor_view,name='admin-doctor'),
    path('admin-view-doctor', views.admin_view_doctor_view,name='admin-view-doctor'),
    path('delete-doctor-from-hospital/<int:pk>', views.delete_doctor_from_hospital_view,name='delete-doctor-from-hospital'),
    path('update-doctor/<int:pk>', views.update_doctor_view,name='update-doctor'),
    path('admin-add-doctor', views.admin_add_doctor_view,name='admin-add-doctor'),
    path('admin-approve-doctor', views.admin_approve_doctor_view,name='admin-approve-doctor'),
    path('approve-doctor/<int:pk>', views.approve_doctor_view,name='approve-doctor'),
    path('reject-doctor/<int:pk>', views.reject_doctor_view,name='reject-doctor'),
    path('admin-view-doctor-specialisation',views.admin_view_doctor_specialisation_view,name='admin-view-doctor-specialisation'),

    path('admin-fdo', views.admin_fdo_view,name='admin-fdo'),
    path('admin-view-fdo', views.admin_view_fdo_view,name='admin-view-fdo'),
    path('admin-add-fdo', views.admin_add_fdo_view,name='admin-add-fdo'),
    path('delete-fdo-from-hospital/<int:pk>', views.delete_fdo_from_hospital_view,name='delete-fdo-from-hospital'),
    path('fdo-patient', views.fdo_patient_view,name='fdo-patient'),
    path('fdo-view-patient', views.fdo_view_patient_view,name='fdo-view-patient'),
    path('delete-patient-from-hospital/<int:pk>', views.delete_patient_from_hospital_view,name='delete-patient-from-hospital'),
    path('update-patient/<int:pk>', views.update_patient_view,name='update-patient'),
    path('fdo-add-patient', views.fdo_add_patient_view,name='fdo-add-patient'),
    path('fdo-discharge-patient', views.fdo_discharge_patient_view,name='fdo-discharge-patient'),
    path('discharge-patient/<int:pk>', views.discharge_patient_view,name='discharge-patient'),
    path('download-pdf/<int:pk>', views.download_pdf_view,name='download-pdf'),


    path('fdo-appointment', views.fdo_appointment_view,name='fdo-appointment'),
    path('fdo-view-appointment', views.fdo_view_appointment_view,name='fdo-view-appointment'),
    path('fdo-add-appointment', views.fdo_add_appointment_view,name='fdo-add-appointment'),

    path('admin-deo', views.admin_deo_view,name='admin-deo'),
    path('admin-view-deo', views.admin_view_deo_view,name='admin-view-deo'),
    path('admin-add-deo', views.admin_add_deo_view,name='admin-add-deo'),
    path('delete-deo-from-hospital/<int:pk>', views.delete_deo_from_hospital_view,name='delete-deo-from-hospital'),
    path('deo-treatment', views.deo_view_treatment_view,name='deo-treatment'),
    path('deo-test', views.deo_view_test_view,name='deo-test'),
    path('deo-update-test/<int:pk>', views.deo_update_test_view,name='deo-update-test'),
    path('deo-send-mail/<int:pk>', views.deo_send_mail_view,name='deo-send-mail'),
    path('deo-update-treatment/<int:pk>', views.deo_update_treatment_view,name='deo-update-treatment'),

    path('admin-room', views.admin_room_view,name='admin-room'),
    path('admin-view-room', views.admin_view_room_view,name='admin-view-room'),
    path('admin-add-room', views.admin_add_room_view,name='admin-add-room'),
]


#---------FOR DOCTOR RELATED URLS-------------------------------------
urlpatterns +=[
    path('doctor-dashboard', views.doctor_dashboard_view,name='doctor-dashboard'),
    path('search', views.search_view,name='search'),

    path('doctor-patient', views.doctor_patient_view,name='doctor-patient'),
    path('doctor-view-patient', views.doctor_view_patient_view,name='doctor-view-patient'),
    path('doctor-view-discharge-patient',views.doctor_view_discharge_patient_view,name='doctor-view-discharge-patient'),

    path('doctor-appointment', views.doctor_appointment_view,name='doctor-appointment'),
    path('doctor-view-appointment', views.doctor_view_appointment_view,name='doctor-view-appointment'),
    path('doctor-delete-appointment',views.doctor_delete_appointment_view,name='doctor-delete-appointment'),
    path('doctor-update-appointment/<int:pk>', views.doctor_update_appointment_view,name='doctor-update-appointment'),
    path('delete-appointment/<int:pk>', views.delete_appointment_view,name='delete-appointment'),

    path('doctor-add-test', views.doctor_add_test_view,name='doctor-add-test'),
    path('doctor-add-treatment', views.doctor_add_treatment_view,name='doctor-add-treatment'),
]

