from patientapp.models import *
from django.shortcuts import render, redirect

################################################################### login

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = login.objects.get(username=username, password=password)
            request.session['user_id'] = user.id
            request.session['usertype'] = user.usertype

            if user.usertype == 'patient':
                return redirect('home')
            elif user.usertype == 'doctor':
                return redirect('dochome')
            elif user.usertype == 'admin':
                return redirect('adminhome')
            else:
                return render(request, 'login/login.html', {'error': 'Invalid user type'})
        except login.DoesNotExist:
            return render(request, 'login/login.html', {'error': 'Invalid username or password'})

    return render(request, 'login/login.html')


def signup(request):
    res = patient.objects.all()
    return render(request, 'login/register.html', {'data': res})


def signuppost(request):
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        gender = request.POST['gender']
        phone = request.POST['phone']
        address = request.POST['address']
        bloodgroup = request.POST['blood']
        username = request.POST['username']
        password = request.POST['password']
        usertype = 'patient'

        login_instance = login.objects.create(
            username=username,
            password=password,
            usertype=usertype
        )

        patient.objects.create(
            name=name,
            age=age,
            gender=gender,
            phone=phone,
            address=address,
            bloodgroup=bloodgroup,
            LOGIN=login_instance
        )

        return redirect('login')

    return redirect('signup')

############################################################################## module 1

def patienthome(request):
    return render(request, 'patient/patienthome.html')

def viewbookings(request):
    patient_id = request.session.get('user_id')
    if not patient_id:
        return redirect('login')

    res = booking.objects.filter(PATIENTS__LOGIN_id=patient_id)
    return render(request, 'patient/booking.html', {'data': res})

def addbookings(request):
    if not request.session.get('user_id'):
        return redirect('login')

    doctors_list = doctors.objects.all()
    return render(request, 'patient/addbooking.html', {'data': doctors_list})

def addbookingpost(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        date = request.POST.get('date')
        time = request.POST.get('time')
        status = 'Pending'

        try:
            doctor_instance = doctors.objects.get(id=doctor_id)
        except doctors.DoesNotExist:
            return redirect('addbookings')

        login_id = request.session.get('user_id')
        patient_instance = patient.objects.get(LOGIN_id=login_id)

        booking.objects.create(
            date=date,
            time=time,
            status=status,
            DOCTORS=doctor_instance,
            PATIENTS=patient_instance
        )

        return redirect('bookings')
    return redirect('addbookings')

def editbookings(request, id):
    booking_instance = booking.objects.get(id=id)
    doctors_list = doctors.objects.all()
    return render(request, 'patient/editbookings.html', {'data': booking_instance, 'doctors': doctors_list})

def editbookingpost(request, id):
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        doctor_id = request.POST.get('doctor')

        update_data = {'date': date, 'time': time}

        if doctor_id:
            doctor_instance = doctors.objects.get(id=doctor_id)
            update_data['DOCTORS'] = doctor_instance

        booking.objects.filter(id=id).update(**update_data)
        return redirect('bookings')
    return redirect('editbookings', id=id)

def delbookings(request, id):
    res = booking.objects.get(id=id)
    res.delete()
    return redirect('bookings')

def history(request):
    patient_id = request.session.get('user_id')
    if not patient_id:
        return redirect('login')

    try:
        patient_instance = patient.objects.get(LOGIN_id=patient_id)
        history_data = medicalhistory.objects.filter(PATIENT=patient_instance).order_by('-date')
    except patient.DoesNotExist:
        return redirect('login')

    context = {
        'patient': patient_instance,
        'data': history_data
    }
    return render(request, 'patient/history.html', context)

def viewbilling(request):
    patient_id = request.session.get('user_id')
    if not patient_id:
        return redirect('login')

    patient_instance = patient.objects.get(LOGIN_id=patient_id)
    bills = billing.objects.filter(PATIENT=patient_instance).order_by('-date')
    total_amount = sum([float(b.amount) for b in bills if b.status != 'Paid'])

    context = {
        'patient': patient_instance,
        'bills': bills,
        'total_amount': total_amount
    }
    return render(request, 'patient/payments.html', context)

def health_info(request):
    patient_id = request.session.get('user_id')
    if not patient_id:
        return redirect('login')

    patient_instance = patient.objects.get(LOGIN_id=patient_id)
    info_list = healthinfo.objects.all().order_by('-id')
    medications = prescription.objects.filter(PATIENT=patient_instance).order_by('-date')

    context = {
        'patient': patient_instance,
        'info_list': info_list,
        'medications': medications
    }
    return render(request, 'patient/info.html', context)

def edit_patient(request, id):
    patient_instance = patient.objects.get(id=id)
    return render(request, 'patient/editpatient.html', {'data': patient_instance})

def edit_patientpost(request, id):
    if request.method == 'POST':
        res = patient.objects.get(id=id)
        res.name = request.POST['name']
        res.age = request.POST['age']
        res.gender = request.POST['gender']
        res.phone = request.POST['phone']
        res.address = request.POST['address']
        res.bloodgroup = request.POST['blood']
        res.save()

        return redirect('history')
    return redirect('edit_patient', id=id)

############################################################################# module2

def dochome(request):
    return render(request, 'doctor/dochome.html')

def records(request):
    res = medicalhistory.objects.all()
    return render(request, 'doctor/records.html', {'data': res})

def editrecords(request, id):
    records_instance = medicalhistory.objects.get(id=id)
    patient_list = patient.objects.all()
    return render(request, 'doctor/editrecord.html', {'data': records_instance, 'patients': patient_list})

def editrecordpost(request, id):
    if request.method == 'POST':
        diagnosis = request.POST.get('diagnosis')
        medication = request.POST.get('medication')
        allergies = request.POST.get('allergies')
        treatments = request.POST.get('treatments')
        date = request.POST.get('date')
        PATIENT_id = request.POST.get('PATIENT')

        update_data = {
            'date': date,
            'diagnosis': diagnosis,
            'medication': medication,
            'allergies': allergies,
            'treatments': treatments
        }

        if PATIENT_id:
            patient_instance = patient.objects.get(id=PATIENT_id)
            update_data['PATIENT'] = patient_instance

        medicalhistory.objects.filter(id=id).update(**update_data)
        return redirect('viewrecords', id=PATIENT_id)
    return redirect('editrecords', id=id)

def viewrecords(request, id):
    patient_records = medicalhistory.objects.filter(PATIENT__id=id)
    patient_info = patient.objects.get(id=id)

    context = {
        'data': patient_records,
        'patient': patient_info
    }
    return render(request, 'doctor/viewrecords.html', context)

def delrecords(request, id):
    res = medicalhistory.objects.get(id=id)
    res.delete()
    return redirect('records')


def appointments(request):
    doctor_id = request.session.get('user_id')
    if not doctor_id:
        return redirect('login')

    res = booking.objects.filter(DOCTORS__LOGIN_id=doctor_id)
    return render(request, 'doctor/appointments.html', {'data': res})

def approveappoint(request, id):
    booking.objects.filter(id=id).update(status='Approved')
    return redirect('appoint')

def cancelappoint(request, id):
    booking.objects.filter(id=id).update(status='Cancelled')
    return redirect('appoint')

def prescriptions(request):
    doctor_id = request.session.get('user_id')
    if not doctor_id:
        return redirect('login')

    res = prescription.objects.filter(DOCTORS__LOGIN_id=doctor_id)
    return render(request, 'doctor/presription.html', {'data': res})

def addprescription(request):
    patients_list = patient.objects.all()
    return render(request, 'doctor/addprescription.html', {'patients': patients_list})

def addprescriptionpost(request):
    if request.method == 'POST':
        name = request.POST['name']
        dosage = request.POST['dosage']
        instruction = request.POST['instruction']
        date = request.POST['date']
        patient_id = request.POST['patient']

        patient_instance = patient.objects.get(id=patient_id)
        doctor_id = request.session.get('user_id')
        doctor_instance = doctors.objects.get(LOGIN_id=doctor_id)

        prescription.objects.create(
            name=name,
            dosage=dosage,
            instruction=instruction,
            date=date,
            PATIENT=patient_instance,
            DOCTORS=doctor_instance
        )
        return redirect('prescriptions')

def deleteprescription(request, id):
    prescription_instance = prescription.objects.get(id=id)
    prescription_instance.delete()
    return redirect('prescriptions')

################################################################## logout

def logout(request):
    request.session.flush()
    return redirect('login')

################################################################### module3

def adminhome (request):
    return render(request ,'admin/adminhome.html')

def doctor (request):
    res=doctors.objects.all()
    return render(request,'admin/doctor.html',{'data':res})

def addoctor(request):
    res = doctors.objects.all()
    return render(request, 'admin/adddoctor.html', {'data': res})


def addoctorpost(request):
    if request.method == 'POST':
        name = request.POST['name']
        specialization = request.POST['specialization']
        department = request.POST['department']
        phone = request.POST['phone']
        schedule = request.POST['schedule']
        username = request.POST['username']
        password = request.POST['password']
        usertype = 'doctor'

        login_instance = login.objects.create(
            username=username,
            password=password,
            usertype=usertype
        )

        doctors.objects.create(
            name=name,
            specialization=specialization,
            department=department,
            phone=phone,
            schedule=schedule,
            LOGIN=login_instance
        )

        return redirect('doctor')

    return redirect('adddoctor')

def editdoctor(request, id):
    doctor_instance = doctors.objects.get(id=id)
    login_list = login.objects.all()
    return render(request, 'admin/editdoctors.html', {'data': doctor_instance, 'login': login_list})

def editdoctorpost(request, id):
    if request.method == 'POST':
        res = doctors.objects.get(id=id)
        login_instance = res.LOGIN

        login_instance.username = request.POST['username']
        login_instance.password = request.POST['password']
        login_instance.usertype = 'doctor'
        login_instance.save()

        #
        res.name = request.POST['name']
        res.specialization = request.POST['specialization']
        res.department = request.POST['department']
        res.phone = request.POST['phone']
        res.schedule = request.POST['schedule']
        res.save()

        return redirect('doctor')

    return redirect('editdoctor', id=id)


def deldoc(request, id):
    res = doctors.objects.get(id=id)
    res.delete()
    return redirect('doctor')

def patients(request):
    res=patient.objects.all()
    return render(request,'admin/patient.html',{'data':res})


def editpatient(request, id):
    patient_instance = patient.objects.get(id=id)
    login_list = login.objects.all()
    return render(request, 'admin/editpatient.html', {'data': patient_instance, 'login': login_list})

def editpatientpost(request, id):
    if request.method == 'POST':
        res = patient.objects.get(id=id)
        login_instance = res.LOGIN

        login_instance.username = request.POST['username']
        login_instance.password = request.POST['password']
        login_instance.usertype = 'patient'
        login_instance.save()


        res.name = request.POST['name']
        res.age = request.POST['age']
        res.gender = request.POST['gender']
        res.phone = request.POST['phone']
        res.address = request.POST['address']
        res.bloodgroup = request.POST['blood']
        res.save()

        return redirect('patient')

    return redirect('editpatient', id=id)


def delpat(request, id):
    res = patient.objects.get(id=id)
    res.delete()
    return redirect('patient')

def view_booking(request):
    res=booking.objects.all()
    return render(request,'admin/appointments.html',{'data':res})

def delbook(request,id):
    res=booking.objects.get(id=id)
    res.delete()
    return redirect('viewbook')

def viewbillings(request):
    res=billing.objects.all()
    return render (request,'admin/viewbilling.html',{'data':res})

def addbillings(request):
    patients_list = patient.objects.all()  # get all patients for the dropdown
    return render(request, 'admin/addbilling.html', {'patients': patients_list})


def addbillingpost(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        amount = request.POST.get('amount')
        invoice = request.POST.get('invoice')
        service = request.POST.get('service')
        status = request.POST.get('status')
        insurance = request.POST.get('insurance')
        date = request.POST.get('date')
        paymentdate = request.POST.get('paymentdate') or None  # optional

        try:
            patient_instance = patient.objects.get(id=patient_id)
        except patient.DoesNotExist:
            return redirect('addbilling')

        billing.objects.create(
            amount=amount,
            invoice=invoice,
            service=service,
            status=status,
            insurance=insurance,
            date=date,
            paymentdate=paymentdate,
            PATIENT=patient_instance
        )
        return redirect('viewbilling')

    return redirect('addbilling')


def editbillings(request, id):
    res = billing.objects.get(id=id)
    res2 = patient.objects.all()
    return render(request, 'admin/editbilling.html', {'data': res, 'patient': res2})

def editbillingpost(request, id):
    if request.method == 'POST':
        bill = billing.objects.get(id=id)
        patient_id = request.POST.get('patient')
        amount = request.POST.get('amount')
        invoice = request.POST.get('invoice')
        service = request.POST.get('service')
        status = request.POST.get('status')
        insurance = request.POST.get('insurance')
        date = request.POST.get('date')  # YYYY-MM-DD
        paymentdate = request.POST.get('paymentdate')

        update_data = {
            'amount': amount,
            'invoice': invoice,
            'service': service,
            'status': status,
            'insurance': insurance,
            'date': date,
            'paymentdate': paymentdate
        }

        if patient_id:
            patient_instance = patient.objects.get(id=patient_id)
            update_data['PATIENT'] = patient_instance

        billing.objects.filter(id=id).update(**update_data)
        return redirect('viewbilling')
    return redirect('editbillings', id=id)

def delbillings(request, id):
    res = billing.objects.get(id=id)
    res.delete()
    return redirect('viewbilling')

############################################################# the end


