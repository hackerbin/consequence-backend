from django.core.management.base import BaseCommand, CommandError
from users.models import NatureOfBusiness


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        NatureOfBusiness.objects.all().delete()
        business_natures = [
            'Architecture and engineering',
            'Arts, culture and entertainment',
            'Business, management and administration',
            'Communications',
            'Community and social services'
            'Education',
            'Science and technology',
            'Installation, repair and maintenance',
            'Farming, fishing and forestry',
            'Government',
            'Health and medicine',
            'Law and public policy',
            'Sales and Marketing'
        ]
        for business_nature in business_natures:
            _obj = NatureOfBusiness.objects.create(title=business_nature)
            self.stdout.write(
                self.style.SUCCESS('created nature of business id: {} , title: {}'.format(_obj.pk, _obj.title))
            )
        self.stdout.write(self.style.SUCCESS('Successfully created nature of businesses'))
