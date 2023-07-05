from django import forms
from django.contrib.auth.models import User
from . import models
from django.db.models import Q


#for admin signup
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }



class DoctorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password', 'email']
        widgets = {
        'password': forms.PasswordInput()
        }
class DoctorForm(forms.ModelForm):
    class Meta:
        model=models.Doctor
        fields=['address','mobile','department','status','profile_pic']

class FDOSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password', 'email']
        widgets = {
        'password': forms.PasswordInput()
        }

class DEOSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

# for teacher related form
class PatientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class PatientForm(forms.ModelForm):
    assignedDoctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Name and Department", to_field_name="user_id")
    class Meta:
        model=models.Patient
        fields=['address','mobile','status','symptoms','profile_pic']



class TestForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    patientId=forms.ModelChoiceField(queryset=models.Patient.objects.all().filter(status=True),empty_label="Patient Name and Symptoms", to_field_name="user_id")
    class Meta:
        model=models.Test
        fields=['testName','testResult']

class TestUpdateForm(forms.ModelForm):
    # doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    # patientId=forms.ModelChoiceField(queryset=models.Patient.objects.all().filter(status=True),empty_label="Patient Name and Symptoms", to_field_name="user_id")
    class Meta:
        model=models.Test
        fields=['doctorId', 'patientId', 'testName','testResult']

class TreatmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    patientId=forms.ModelChoiceField(queryset=models.Patient.objects.all().filter(status=True),empty_label="Patient Name and Symptoms", to_field_name="user_id")
    class Meta:
        model=models.Treatment
        fields=['treatmentName','description']

class TreatmentUpdateForm(forms.ModelForm):
    # doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    # patientId=forms.ModelChoiceField(queryset=models.Patient.objects.all().filter(status=True),empty_label="Patient Name and Symptoms", to_field_name="user_id")
    class Meta:
        model=models.Treatment
        fields=['doctorId', 'patientId', 'treatmentName','description']

# class dateinput(forms.DateTimeInput):
#     input_type= ['%d/%m/%Y %H:%M']

class AppointmentForm(forms.ModelForm):
    
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    patientId=forms.ModelChoiceField(queryset=models.Patient.objects.all().filter(status=True),empty_label="Patient Name and Symptoms", to_field_name="user_id", required=False)
    room = forms.ModelChoiceField(queryset=models.Room.objects.all().filter(~Q(curr_availability = 0)),empty_label="Room for Appointment", to_field_name="room_no", required=False)
    priority=forms.ChoiceField(choices=models.Appointment.PRIOR)
    appointmentDate = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'],
                                           widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    class Meta:
        model=models.Appointment
        fields=['description','status','appointmentDate', 'priority']

class AppointmentUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Appointment
        fields=['doctorId', 'patientId', 'room', 'priority', 'appointmentDate','description','status' ]
        
class AcceptAppoitmentForm(AppointmentForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.filter(
        status=True), empty_label="Doctor Name and Department", to_field_name="user_id", required=False)

class RoomForm(forms.ModelForm):
    room_no=forms.CharField(max_length=10)
    max_capacity=forms.IntegerField()
    curr_availability=forms.IntegerField()

    class Meta:
        model=models.Room
        fields=['room_no','max_capacity','curr_availability']

#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))



