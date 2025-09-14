from django.core.management.base import BaseCommand
from booklib.utils import send_debt_email

class Command(BaseCommand):
    help = 'Send email notifications to users with overdue debts'

    def handle(self, *args, **options):
        send_debt_email()
        self.stdout.write(self.style.SUCCESS('Debt notifications sent successfully'))