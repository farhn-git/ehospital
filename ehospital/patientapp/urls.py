from django.contrib import admin
from django.urls import path
from patientapp import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('home/', views.patienthome, name='home'),
    path('register/', views.signup, name='register'),
    path('registerpost/', views.signuppost, name='registerpost'),
    path('bookings/', views.viewbookings, name='bookings'),
    path('addbookings/', views.addbookings, name='addbookings'),
    path('addbookingpost/', views.addbookingpost, name='addbookingpost'),
    path('editbooking/<int:id>/', views.editbookings, name='editbooking'),
    path('editbookingpost/<int:id>/', views.editbookingpost, name='editbookingpost'),
    path('delbooking/<int:id>/', views.delbookings, name='delbooking'),
    path('history/', views.history, name='history'),
    path('billing/', views.viewbilling, name='billing'),
    path('info/', views.health_info, name='info'),
    path('edit_patient/<int:id>/', views.edit_patient, name='edit_patient'),
    path('edit_patientpost/<int:id>/', views.edit_patientpost, name='edit_patientpost'),

    # # module2

    path('dochome/',views.dochome,name='dochome'),
    path('records/',views.records,name='records'),
    path('editrecords/<int:id>/',views.editrecords,name='editrecords'),
    path('editrecordspost/<int:id>/',views.editrecordpost,name='editrecordpost'),
    path('viewrecords/<int:id>/',views.viewrecords,name='viewrecords'),
    path('delrecord/<int:id>/', views.delrecords, name='delrecord'),
    path('appoint/',views.appointments,name='appoint'),
    path('approveappoint/<int:id>/', views.approveappoint, name='approveappoint'),
    path('cancelappoint/<int:id>/', views.cancelappoint, name='cancelappoint'),
    path('prescriptions/', views.prescriptions, name='prescriptions'),
    path('addprescription/', views.addprescription, name='addprescription'),
    path('addprescriptionpost/', views.addprescriptionpost, name='addprescriptionpost'),
    path('deleteprescription/<int:id>/', views.deleteprescription, name='deleteprescription'),
    path('logout/', views.logout, name='logout'),

    ################################################### module3

    path('adminhome/',views.adminhome,name='adminhome'),
    path('doctor/',views.doctor,name='doctor'),
    path('addoctor/',views.addoctor,name='adddoctor'),
    path('addoctorpost/',views.addoctorpost,name='adddoctorpost'),
    path('editdoctor/<int:id>/',views.editdoctor,name='editdoctor'),
    path('editdoctorpost/<int:id>/',views.editdoctorpost,name='editdoctorpost'),
    path('deldoc/<int:id>/',views.deldoc,name='deldoc'),
    path('patient/',views.patients,name='patient'),
    path('editpatient/<int:id>/',views.editpatient,name='editpatient'),
    path('editpatientpost/<int:id>/',views.editpatientpost,name='editpatientpost'),
    path('delpat/<int:id>/',views.delpat,name='delpat'),
    path('viewbookings/',views.view_booking,name='viewbook'),
    path('delbook/<int:id>/',views.delbook,name='delbook'),
    path('viewbilling/',views.viewbillings,name='viewbilling'),
    path('addbilling/',views.addbillings,name='addbilling'),
    path('addbillingpost/',views.addbillingpost,name='addbillingpost'),
    path('editbilling/<int:id>/',views.editbillings,name='editbilling'),
    path('editbillingpost/<int:id>/',views.editbillingpost,name='editbillingpost'),
    path('delbill/<int:id>/',views.delbillings,name='delbill'),



]