from notifications.signals import notify
from core.models import User,UserInterview

def notify_all_company_and_client_users(sender,message,interview_id):
    company_users = User.objects.filter(access_control ="CO").all()
    client_users = User.objects.filter(access_control="CL")
    interview_user = UserInterview.objects.filter(id__in=client_users.values_list('id'),interview_id = interview_id)
    notify.send(sender, recipient=company_users, verb=message)
    notify.send(sender, recipient=interview_user, verb=message)
