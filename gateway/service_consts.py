
user_login = 'user_login'
user_register = 'user_register'
user_profile = 'user_profile'

doctor_add_prescription = 'doctor_add_prescription'
doctor_list_prescriptions = 'doctor_list_prescriptions'

patient_list_prescriptions = 'patient_list_prescriptions'

admin_list_prescriptions = 'admin_list_prescriptions'
admin_get_daily = 'admin_get_daily'


service_urls = {
    user_register: 'http://127.0.0.1:8000/api/profile/register/',
    user_login: 'http://127.0.0.1:8000/api/profile/login/',
    user_profile: 'http://127.0.0.1:8000/api/profile/',
    doctor_add_prescription: 'http://127.0.0.1:8000/api/prescription/add/',
    doctor_list_prescriptions: 'http://127.0.0.1:8000/api/prescripton/get_by_doctor',
    patient_list_prescriptions: 'http://127.0.0.1:8000/api/prescription/get_by_patient',
    admin_list_prescriptions: 'http://127.0.0.1:8000/api/prescription/get_by_admin',
    admin_get_daily: 'http://127.0.0.1:8000/api/admin/daily_stats',
}
