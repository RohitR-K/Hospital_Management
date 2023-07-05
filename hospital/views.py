from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages

# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/index.html')


#for showing signup/login button for admin(by  )
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/adminclick.html')


#for showing signup/login button for doctor(by  )
def doctorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/doctorclick.html')


#for showing signup/login button for patient(by  )
def fdoclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/fdo.html')

def deoclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/deo.html')


def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request,'hospital/adminsignup.html',{'form':form})


#-----------for checking user is doctor , patient or admin(by  )
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()


def is_fdo(user):
    return user.groups.filter(name='FDO').exists()
def is_deo(user):
    return user.groups.filter(name='DEO').exists()


#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_doctor(request.user):
        accountapproval=models.Doctor.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('doctor-dashboard')
        else:
            return render(request,'hospital/doctor_wait_for_approval.html')
    elif is_fdo(request.user):
        return redirect('fdo-dashboard')
    elif is_deo(request.user):
        return redirect('deo-dashboard')



#---------------------------------------------------------------------------------
#------------------------ DEO RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------

@login_required(login_url='deologin')
@user_passes_test(is_deo)
def deo_dashboard_view(request):
    #for both table in admin dashboard
    doctors=models.Doctor.objects.all().order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')
    #for three cards
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()

    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    mydict={
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'hospital/deo_dashboard.html',context=mydict)


@login_required(login_url='deologin')
@user_passes_test(is_deo)
def deo_patient_view(request):
    return render(request,'hospital/deo_patient.html')



@login_required(login_url='deologin')
@user_passes_test(is_deo)
def deo_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/deo_view_patient.html',{'patients':patients})

@login_required(login_url='deologin')
@user_passes_test(is_deo)
def deo_add_test_view(request):
    testForm=forms.TestForm()
    mydict={'testForm':testForm,}
    if request.method=='POST':
        testForm=forms.TestForm(request.POST)
        if testForm.is_valid():
            test=testForm.save(commit=False)
            test.doctorId=request.POST.get('doctorId')
            test.patientId=request.POST.get('patientId')
            test.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            test.patientName=models.User.objects.get(id=request.POST.get('patientId')).first_name
            
            test.save()
        return HttpResponseRedirect('deo-patient')
    return render(request,'hospital/deo_update_test.html',context=mydict)


@login_required(login_url='deologin')
@user_passes_test(is_deo)
def deo_add_treatment_view(request):
    treatmentForm=forms.TreatmentForm()
    mydict={'treatmentForm': treatmentForm}
    if request.method=='POST':
        treatmentForm=forms.TreatmentForm(request.POST)
        if treatmentForm.is_valid():
            treatment=treatmentForm.save(commit=False)
            treatment.doctorId=request.POST.get('doctorId')
            treatment.patientId=request.POST.get('patientId')
            treatment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            treatment.patientName=models.User.objects.get(id=request.POST.get('patientId')).first_name
            treatment.save()
        return HttpResponseRedirect('deo-patient')
    return render(request,'hospital/deo_update_treatment.html',context=mydict)


@login_required(login_url='deologin')
@user_passes_test(is_deo)
def deo_view_test_view(request):
    tests=models.Test.objects.all()
    return render(request,'hospital/deo_view_test.html',{'tests':tests})

@login_required(login_url='deologin')
@user_passes_test(is_deo)
def deo_view_treatment_view(request):
    treatments=models.Treatment.objects.all()
    return render(request,'hospital/deo_view_treatment.html',{'treatments':treatments})


@login_required(login_url='deologin')
@user_passes_test(is_deo)
def deo_update_test_view(request,pk):
    test = models.Test.objects.get(id=pk)
    testForm = forms.TestUpdateForm(instance=test)
    mydict={'testForm': testForm}
    if request.method=='POST':
        testForm=forms.TestUpdateForm(request.POST, instance = test)
        print(request.POST)
        if testForm.is_valid():
            test=testForm.save(commit=False)
            test.save()
            return redirect('deo-test')
    return render(request,'hospital/deo_update_test.html',context=mydict)

@login_required(login_url='deologin')
@user_passes_test(is_deo)
def deo_send_mail_view(request,pk):
    test = models.Test.objects.get(id=pk)
    doctor = models.User.objects.get(id=test.doctorId)
    receipent = [doctor.email,]
    subject = f'Health Information of your patient {test.patientName}'
    message = f'Hi {test.doctorName},\nThe following are the details of your patient {test.patientName}:\n\nTest Name: {test.testName}\nTest Date: {test.testDate}\nTest Result: {test.testResult}\n\nThank You\n'
    sender = settings.EMAIL_HOST_USER
    send_mail(subject, message, sender, receipent)
    return render(request,'hospital/deo_dashboard.html')

@login_required(login_url='deologin')
@user_passes_test(is_deo)
def deo_update_treatment_view(request,pk):
    treatment = models.Treatment.objects.get(id=pk)
    treatmentForm = forms.TreatmentUpdateForm(instance=treatment)
    mydict={'treatmentForm': treatmentForm}
    if request.method=='POST':
        treatmentForm=forms.TreatmentUpdateForm(request.POST, instance = treatment)
        print(request.POST)
        if treatmentForm.is_valid():
            treatment=treatmentForm.save(commit=False)
            treatment.save()
            return redirect('deo-treatment')
    return render(request,'hospital/deo_update_treatment.html',context=mydict)

#---------------------------------------------------------------------------------
#------------------------ FDO RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------

@login_required(login_url='fdologin')
@user_passes_test(is_fdo)
def fdo_dashboard_view(request):
    #for both table in admin dashboard
    doctors=models.Doctor.objects.all().order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')
    #for three cards
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()

    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    mydict={
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'hospital/fdo_dashboard.html',context=mydict)



@login_required(login_url='fdologin')
@user_passes_test(is_fdo)
def fdo_patient_view(request):
    return render(request,'hospital/fdo_patient.html')



@login_required(login_url='fdologin')
@user_passes_test(is_fdo)
def fdo_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/fdo_view_patient.html',{'patients':patients})


@login_required(login_url='fdologin')
@user_passes_test(is_fdo)
def delete_patient_from_hospital_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    appoint = models.Appointment.objects.get(patientId=patient.user_id)
    user.delete()
    appoint.delete()
    patient.delete()
    return redirect('fdo-view-patient')



@login_required(login_url='fdologin')
@user_passes_test(is_fdo)
def update_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)

    userForm=forms.PatientUserForm(instance=user)
    patientForm=forms.PatientForm(request.FILES,instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST,instance=user)
        patientForm=forms.PatientForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()
            return redirect('fdo-view-patient')
    return render(request,'hospital/fdo_update_patient.html',context=mydict)


@login_required(login_url='fdologin')
@user_passes_test(is_fdo)
def fdo_add_patient_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            patient=patientForm.save(commit=False)
            patient.user=user
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)

        return HttpResponseRedirect('fdo-view-patient')
    return render(request,'hospital/fdo_add_patient.html',context=mydict)



#------------------FOR APPROVING PATIENT BY FDO----------------------

@login_required(login_url='fdologin')
@user_passes_test(is_fdo)
def fdo_approve_patient_view(request):
    #those whose approval are needed
    patients=models.Patient.objects.all().filter(status=False)
    return render(request,'hospital/fdo_approve_patient.html',{'patients':patients})



@login_required(login_url='fdologin')
@user_passes_test(is_fdo)
def approve_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    patient.status=True
    patient.save()
    return redirect(reverse('admin-approve-patient'))



@login_required(login_url='fdologin')
@user_passes_test(is_fdo)
def reject_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-approve-patient')



#--------------------- FOR DISCHARGING PATIENT BY FDO START-------------------------

@login_required(login_url='fdologin')
@user_passes_test(is_fdo)
def fdo_discharge_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/fdo_discharge_patient.html',{'patients':patients})


@login_required(login_url='fdologin')
@user_passes_test(is_fdo)
def discharge_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    days=(date.today()-patient.admitDate) #2 days, 0:00:00
    assignedDoctor=models.User.objects.all().filter(id=patient.assignedDoctorId)
    d=days.days # only how many day that is 2
    patientDict={
        'patientId':pk,
        'name':patient.get_name,
        'mobile':patient.mobile,
        'address':patient.address,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'todayDate':date.today(),
        'day':d,
        'assignedDoctorName':assignedDoctor[0].first_name,
    }
    
    if request.method == 'POST':
        feeDict ={
            'roomCharge':int(request.POST['roomCharge'])*int(d),
            'doctorFee':request.POST['doctorFee'],
            'medicineCost' : request.POST['medicineCost'],
            'OtherCharge' : request.POST['OtherCharge'],
            'total':(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        }
        patientDict.update(feeDict)
        #for updating to database patientDischargeDetails (pDD)
        pDD=models.PatientDischargeDetails()
        pDD.patientId=pk
        pDD.patientName=patient.get_name
        pDD.assignedDoctorName=assignedDoctor[0].first_name
        pDD.address=patient.address
        pDD.mobile=patient.mobile
        pDD.symptoms=patient.symptoms
        pDD.admitDate=patient.admitDate
        pDD.releaseDate=date.today()
        pDD.daySpent=int(d)
        pDD.medicineCost=int(request.POST['medicineCost'])
        pDD.roomCharge=int(request.POST['roomCharge'])*int(d)
        pDD.doctorFee=int(request.POST['doctorFee'])
        pDD.OtherCharge=int(request.POST['OtherCharge'])
        pDD.total=(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        pDD.save()
        appointment = models.Appointment.objects.get(patientId=patient.user_id)
        user=models.User.objects.get(id=patient.user_id)
        room = models.Room.objects.get(room_no = appointment.room)
        room.curr_availability = room.curr_availability + 1
        room.save() 
        appointment.delete()
        user.delete()
        patient.delete()
        return render(request,'hospital/patient_final_bill.html',context=patientDict)
    
    return render(request,'hospital/patient_generate_bill.html',context=patientDict)



#--------------for discharge patient bill (pdf) download and printing-----------------------
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return


def download_pdf_view(request,pk):
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=pk).order_by('-id')[:1]
    dict={
        'patientName':dischargeDetails[0].patientName,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':dischargeDetails[0].address,
        'mobile':dischargeDetails[0].mobile,
        'symptoms':dischargeDetails[0].symptoms,
        'admitDate':dischargeDetails[0].admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
    }
    return render_to_pdf('hospital/download_bill.html',dict)



#-----------------APPOINTMENT START--------------------------------------------------------------------

@login_required(login_url='fdologin')
@user_passes_test(is_fdo)
def fdo_appointment_view(request):
    return render(request,'hospital/fdo_appointment.html')



@login_required(login_url='fdologin')
@user_passes_test(is_fdo)
def fdo_view_appointment_view(request):
    appointments=models.Appointment.objects.all().filter(status=True)
    return render(request,'hospital/fdo_view_appointment.html',{'appointments':appointments})


@login_required(login_url='fdologin')
@user_passes_test(is_fdo)
def fdo_add_appointment_view(request):
    appointmentForm = forms.AcceptAppoitmentForm()
    mydict = {'appointmentForm': appointmentForm, }

    if request.method == 'POST':
        print("hello")
        if 'action' in request.POST and request.POST['action'] == 'check':
            print("im in!!!!!!!!!!")
            appointment_time_temp = request.POST.get('appointmentDate')
            appointment_time = timezone.make_aware(
                datetime.strptime(appointment_time_temp, '%Y-%m-%dT%H:%M'))
            print(appointment_time)
            busy_doctors = models.Appointment.objects.filter(
                appointmentDate=appointment_time).values_list('doctorId', flat=True).distinct()

            free_doctors = models.Doctor.objects.filter(~Q(user_id__in = busy_doctors))
            print(free_doctors)

            print(f"The following doctors are busy at {appointment_time}: {list(busy_doctors)}")
            print(f"The following doctors are free at {appointment_time}: {list(free_doctors.values_list('user_id', flat=True))}")

            appointmentForm.fields['doctorId'].queryset = free_doctors

            context = {
                'appointmentForm': appointmentForm,
                'free_doctors': free_doctors,
            }

            return render(request, 'hospital/fdo_add_appointment.html', context)

        else:
            appointmentForm = forms.AppointmentForm()
            mydict = {'appointmentForm': appointmentForm, }
            if request.method == 'POST':
                appointmentForm = forms.AppointmentForm(request.POST)
                if appointmentForm.is_valid():
                    doctor_id = request.POST.get('doctorId')
                    appointment_time = appointmentForm.cleaned_data.get(
                        'appointmentDate')
                    if request.POST.get('priority') == '2':
                        d = models.User.objects.get(id = doctor_id)
                        p = models.User.objects.get(id = request.POST.get('patientId'))
                        subject = f'Appointment Cancelled due to Emergency'
                        content = f'Hi! {d.first_name}, \n The appointment for the patient {p.first_name} on {appointment_time} is cancelled due to another Emergency appointment.\n Kindly order the Front Desk operator to reschedule. \n Thank you'
                        sender = settings.EMAIL_HOST_USER
                        receipient = [d.email,]
                        send_mail(subject, content, sender, receipient)
                        models.Appointment.objects.filter(
                            doctorId=doctor_id, appointmentDate=appointment_time).delete()
                        print('High')
                    
                    # Check if the selected doctor already has an appointment at the same time
                    elif request.POST.get('priority') == '1':
                        if models.Appointment.objects.filter(doctorId=doctor_id, appointmentDate=appointment_time).exists():
                            messages.error(
                                request, 'The selected doctor already has an appointment scheduled at the same time.')
                            return redirect('admin-add-appointment')
                    appointment = appointmentForm.save(commit=False)
                    appointment.doctorId = doctor_id


                    room_no = request.POST.get('room')
                    appointment.room = room_no
                    room_temp = models.Room.objects.get(room_no = room_no)
                    room_temp.curr_availability = room_temp.curr_availability - 1
                    room_temp.save()
                    
                    d = models.User.objects.get(id = doctor_id)
                    p = models.User.objects.get(id = request.POST.get('patientId'))
                    subject = f'New Appointment Received {d.first_name} | {p.first_name} {p.last_name}'
                    content = f'Hi! {d.first_name}, \n A new appointment for the patient {p.first_name} has been recevied on {appointment_time} in the room {room_no}. \n Kindly consider his/her case. \n Thank you'
                    sender = settings.EMAIL_HOST_USER
                    receipient = [d.email,]
                    send_mail(subject, content, sender, receipient)

                    appointment.patientId = request.POST.get('patientId')
                    print(doctor_id, appointment.patientId)
                    # doc_userid = models.Doctor.objects.get(
                    #     id=doctor_id).user_id
                    # print(doc_userid)
                    appointment.doctorName = models.User.objects.get(
                        id=doctor_id).first_name
                 
                    appointment.patientName=models.User.objects.get(id=request.POST.get('patientId')).first_name
                    # print(appointment.patientName, appointment.doctorName)

                    appointment.status = True
                    appointment.save()
                    messages.success(
                        request, 'Appointment added successfully!')
                    return redirect('fdo-view-appointment')
            else:
                messages.error(
                    request, 'Invalid form submission. Please correct the errors below.')
    return render(request, 'hospital/fdo_add_appointment.html', context=mydict)



#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    #for both table in admin dashboard
    doctors=models.Doctor.objects.all().order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')
    #for three cards
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()

    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    mydict={
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'hospital/admin_dashboard.html',context=mydict)


# this view for sidebar click on admin page
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request,'hospital/admin_doctor.html')

# this view for sidebar click on admin page
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_fdo_view(request):
    return render(request,'hospital/admin_fdo.html')

# this view for sidebar click on admin page
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_deo_view(request):
    return render(request,'hospital/admin_deo.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_doctor.html',{'doctors':doctors})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_fdo_view(request):
    fdo = models.User.objects.all().filter(groups=3)
    return render(request,'hospital/admin_view_fdo.html',{'fdo':fdo})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_deo_view(request):
    deo = models.User.objects.all().filter(groups=4)
    return render(request,'hospital/admin_view_deo.html',{'deo':deo})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-view-doctor')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_fdo_from_hospital_view(request,pk):
    user=models.User.objects.get(id=pk)
    user.delete()
    return redirect('admin-view-fdo')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_deo_from_hospital_view(request,pk):
    user=models.User.objects.get(id=pk)
    user.delete()
    return redirect('admin-view-deo')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)

    userForm=forms.DoctorUserForm(instance=user)
    doctorForm=forms.DoctorForm(request.FILES,instance=doctor)
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST,instance=user)
        doctorForm=forms.DoctorForm(request.POST,request.FILES,instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.status=True
            doctor.save()
            return redirect('admin-view-doctor')
    return render(request,'hospital/admin_update_doctor.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor.status=True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-doctor')
    return render(request,'hospital/admin_add_doctor.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_fdo_view(request):
    form=forms.FDOSigupForm()
    if request.method=='POST':
        form=forms.FDOSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='FDO')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('admin-dashboard')
    return render(request,'hospital/admin_add_fdo.html',{'form':form})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_deo_view(request):
    form=forms.DEOSigupForm()
    if request.method=='POST':
        form=forms.DEOSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='DEO')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('admin-dashboard')
    return render(request,'hospital/admin_add_deo.html',{'form':form})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_room_view(request):
    print('abc')
    roomForm=forms.RoomForm()
    mydict={'roomForm':roomForm,}
    print('dsa')

    if request.method=='POST':
        roomForm=forms.RoomForm(request.POST)
        if roomForm.is_valid():
            room=roomForm.save(commit=False)
            room.room_no=request.POST.get('room_no')
            room.max_capacity=request.POST.get('max_capacity')
            room.curr_availability=request.POST.get('curr_availability')
            
            room.save()
        return HttpResponseRedirect('admin-view-room')
    return render(request,'hospital/admin_add_room.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_room_view(request):
    return render(request,'hospital/admin_room.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_room_view(request):
    room = models.Room.objects.all()
    return render(request,'hospital/admin_view_room.html',{'room':room})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_doctor_view(request):
    #those whose approval are needed
    doctors=models.Doctor.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_doctor.html',{'doctors':doctors})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    return redirect(reverse('admin-approve-doctor'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-approve-doctor')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_specialisation_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_doctor_specialisation.html',{'doctors':doctors})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_patient_view(request):
    return render(request,'hospital/admin_patient.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_patient.html',{'patients':patients})




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_patient_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            patient=patientForm.save(commit=False)
            patient.user=user
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-patient')
    return render(request,'hospital/admin_add_patient.html',context=mydict)



#------------------FOR APPROVING PATIENT BY ADMIN----------------------

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_patient_view(request):
    #those whose approval are needed
    patients=models.Patient.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    patient.status=True
    patient.save()
    return redirect(reverse('admin-approve-patient'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-approve-patient')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('admin-approve-appointment')

#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    #for three cards
    patientcount=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).count()
    appointmentcount=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).count()
    patientdischarged=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()

    #for  table in doctor dashboard
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).order_by('-id')
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid).order_by('-id')
    appointments=zip(appointments,patients)
    mydict={
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    'patientdischarged':patientdischarged,
    'appointments':appointments,
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_dashboard.html',context=mydict)

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict={
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_patient.html',context=mydict)

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_patient.html',{'patients':patients,'doctor':doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def search_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    # whatever user write in search box we get in query
    query = request.GET['query']
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).filter(Q(symptoms__icontains=query)|Q(user__first_name__icontains=query))
    return render(request,'hospital/doctor_view_patient.html',{'patients':patients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_discharge_patient_view(request):
    dischargedpatients=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_appointment.html',{'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_view_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def delete_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_add_test_view(request):
    testForm=forms.TestForm()
    mydict={'testForm':testForm,}
    if request.method=='POST':
        testForm=forms.TestForm(request.POST)
        if testForm.is_valid():
            test=testForm.save(commit=False)
            test.doctorId=request.POST.get('doctorId')
            test.patientId=request.POST.get('patientId')
            test.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            test.patientName=models.User.objects.get(id=request.POST.get('patientId')).first_name
            
            test.save()
        return HttpResponseRedirect('doctor-view-patient')
    return render(request,'hospital/doctor_test_patient.html',context=mydict)


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_add_treatment_view(request):
    treatmentForm=forms.TreatmentForm()
    mydict={'treatmentForm': treatmentForm}
    if request.method=='POST':
        treatmentForm=forms.TreatmentForm(request.POST)
        if treatmentForm.is_valid():
            treatment=treatmentForm.save(commit=False)
            treatment.doctorId=request.POST.get('doctorId')
            treatment.patientId=request.POST.get('patientId')
            treatment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            treatment.patientName=models.User.objects.get(id=request.POST.get('patientId')).first_name
            treatment.save()
        return HttpResponseRedirect('doctor-view-patient')
    return render(request,'hospital/doctor_treatment_patient.html',context=mydict)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_update_appointment_view(request,pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointmentForm = forms.AppointmentUpdateForm(instance=appointment)
    mydict={'appointmentForm': appointmentForm}
    if request.method=='POST':
        appointmentForm=forms.AppointmentUpdateForm(request.POST, instance = appointment)
        print(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.status=True
            appointment.save()
            return redirect('doctor-appointment')
    return render(request,'hospital/doctor_prescribe.html',context=mydict)

#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US VIEWS START --------------------
#---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request,'hospital/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'hospital/contactussuccess.html')
    return render(request, 'hospital/contactus.html', {'form':sub})


#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------