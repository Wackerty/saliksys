from django.core.management.base import BaseCommand, CommandError
from salikneta.models import *
from datetime import date
from django.utils import timezone

class Command(BaseCommand):
    help = 'Gets the expiring/expired products'

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)

        products = ProductBatch.objects.all()

        expiringProducts = "Inventory products near expiration:\n"
        today = date.today()

        for product in products:
            if product.currentCount > 0:
                expiringDate = product.expiringDate
                gap = expiringDate - today
                if gap.days <= 14:
                    productName = product.idProductCount.idProduct.name
                    productBranch = product.idProductCount.idBranch.name
                    productCount = int(product.currentCount)
                    expiringProducts += (str(productCount) + " " + productName + " in " + productBranch + " branch will expire in: " +
                                         str(gap.days) + " days (" + str(product.expiringDate) + ")\n")
                    #print(str(productCount) + " " + productName + " in " + productBranch + " branch will expire in: " +
                    #      str(gap.days) + " days (" + str(product.expiringDate) + ")")
        Notifs.write(expiringProducts, -1)
        print(expiringProducts)

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)
    #
    # def handle(self, *args, **options):
    #     for poll_id in options['poll_ids']:
    #         try:
    #             poll = Poll.objects.get(pk=poll_id)
    #         except Poll.DoesNotExist:
    #             raise CommandError('Poll "%s" does not exist' % poll_id)
    #
    #         poll.opened = False
    #         poll.save()
    #
    #         self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))




# import os
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SaliknetaPOSIS.settings")
# import django
# django.setup()
#
# from salikneta.models import *
# from datetime import date
#
# products = ProductBatch.objects.all()
# expiringProducts = []
# today = date.today()
#
# for product in products:
#     expiringDate = product.expiringDate
#     print(today - expiringDate)