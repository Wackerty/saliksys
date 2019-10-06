from django.db import models

from dateutil.relativedelta import relativedelta

from datetime import datetime,timedelta
from django.db.models import Avg, Max, Min, Sum
import pytz
# Create your models here.

class Branch(models.Model):
    idBranch = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)


class Manager(models.Model):
    idManager = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    idBranch = models.ForeignKey(Branch, on_delete=models.CASCADE)


class Cashier(models.Model):
    idCashier = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    idBranch = models.ForeignKey(Branch, on_delete=models.CASCADE)


class Supplier(models.Model):
    idSupplier = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    contactNumber = models.CharField(max_length=45)
    emailAddress = models.CharField(max_length=45)
    website = models.CharField(max_length=45)
    address1 = models.CharField(max_length=45)
    address2 = models.CharField(max_length=45)
    city = models.CharField(max_length=45)
    province = models.CharField(max_length=45)
    country = models.CharField(max_length=45)
    postal = models.CharField(max_length=45)


class Category(models.Model):
    idCategory = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=45)

class Notifs(models.Model):
    notif_id = models.AutoField(primary_key=True)
    msg = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    viewed = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notifs'
    @property
    def get_time_ago(self):
        utc = pytz.UTC
        diff = relativedelta(datetime.now().replace(tzinfo=utc), self.timestamp.replace(tzinfo=utc), )
        if diff.months == 0:
            if diff.days == 0:
                if diff.hours == 0:
                    if diff.minutes == 0:
                        return "moments ago"
                    return str(diff.minutes) + " minutes ago"
                else:
                    return str(diff.hours) + " hours ago"
            else:
                return str(diff.days) + " days ago"
        else:
            return str(diff.months) + " months ago"
    @staticmethod
    def write(message):
        n = Notifs(msg=message,timestamp=datetime.now())
        n.save()

    @staticmethod
    def check_new_notif():
        for n in Notifs.objects.all():
            if n.viewed == 0:
                return True
        return False

    @staticmethod
    def check_num_new_notif():
        ctr=0
        for n in Notifs.objects.all():
            if n.viewed == 0:
                ctr+=1
        return ctr


class Product(models.Model):
    idProduct = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=45)
    suggestedUnitPrice = models.FloatField()
    reorderLevel = models.FloatField()
    unitOfMeasure = models.CharField(max_length=45)
    SKU = models.IntegerField()
    barcode = models.CharField(max_length=45)
    img_path = models.ImageField(upload_to="prod_img/")
    idCategory = models.ForeignKey(Category, on_delete=models.CASCADE,db_column='idCategory_id')
    expiration = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'salikneta_product'
    @property
    def get_product_code(self):
        return self.idProduct + 1000

    @property
    def get_ingredients(self):
        return IngredientsList.objects.filter(idProduct=self)

    @property
    def get_num_incoming(self):
        incoming = 0
        objs = OrderLines.objects.filter(idProduct_id=self.idProduct)
        for o in objs:
           incoming += o.qty - o.get_delivered_products_num
        return incoming

    @staticmethod
    def get_product_count(self, branchID):
        productCount = ProductCount.objects.get(idProduct=self.idProduct, idBranch=branchID).unitsInStock
        return productCount

    @staticmethod
    def get_amount_can_produce(self, branchID):
        i = IngredientsList.objects.filter(idProduct=self)
        canProduce = []
        for ingredient in i:
            ingredient.unitsInStock = ingredient.idrawmaterials.get_product_count(ingredient.idrawmaterials, branchID)
            ingredient.canProduce = ingredient.unitsInStock // ingredient.qtyneeded
            canProduce.append(ingredient.canProduce)

        print(min(canProduce))

        return min(canProduce)

    @staticmethod
    def get_end_inventory(self, ed, branch):
        deliveries = 0
        sales = 0
        backloads = 0
        tos = 0
        sals = SalesInvoice.objects.filter(invoiceDate__gt=ed)
        bload = BackLoad.objects.filter(backloadDate__gt=ed)
        to = TransferOrderProduct.objects.filter(transferDate__gt=ed)
        for s in sals:
            for il in InvoiceLines.objects.filter(idSales=s,idProduct_id=self.idProduct):
                sales += il.qty
        for b in bload:
            for bl in BackloadLines.objects.filter(idBackload=b, idProduct_id=self.idProduct):
              backloads += bl.qty
        for t in to:
          for tl in t.get_transfer_lines:
              if tl.idProduct_id == self.idProduct:
                  tos += tl.qty

        pc = ProductCount.objects.get(idProduct=self, idBranch=branch)
        ct = (pc.unitsInStock + deliveries)-(sales+backloads+tos)
        return ct

    @staticmethod
    def get_earliest_expiring_batch(self, branchID):
        productCount = ProductCount.objects.get(idProduct=self.idProduct, idBranch=branchID)
        try:
            earliestExpiringBatch = ProductBatch.objects.filter(idProductCount=productCount, currentCount__gt=0, status="In stock").order_by('manufacturedDate')[0]
        except:
            earliestExpiringBatch = None
        return earliestExpiringBatch


class ProductCount(models.Model):
    idProductCount = models.AutoField(db_column='productCountID', primary_key=True)  # Field name made lowercase.
    idProduct = models.ForeignKey(Product, models.CASCADE, db_column='idProduct_id')  # Field name made lowercase.
    idBranch = models.ForeignKey(Branch, models.CASCADE, db_column='idBranch_id')  # Field name made lowercase.
    unitsInStock = models.FloatField(db_column='unitsInStock')  # Field name made lowercase.
    unitsReserved = models.IntegerField(db_column='unitsReserved', default=0)  # Field name made lowercase.


    class Meta:
        managed = False
        db_table = 'salikneta_productcount'

    @staticmethod
    def get_num_lowstock_items(branch):
        ct = 0
        for p in ProductCount.objects.filter(idBranch=branch):
            if p.unitsInStock < p.idProduct.reorderLevel:
                ct += 1
        return ct

    @staticmethod
    def add_stocks(self, amount):
        i = IngredientsList.objects.filter(idProduct=self.idProduct)

        for ingredient in i:
            rc = RawMaterialCount.objects.get(idrawmaterial=ingredient.idrawmaterials, idBranch=self.idBranch)
            rc.deduct_stock(rc, ingredient.qtyneeded*int(amount))

        self.unitsInStock = self.unitsInStock + int(amount)

        self.save()

        print("added: "+str(amount)+" stocks to " + str(self.idProduct.name))

    @staticmethod
    def receive_stocks(self, amount):
        self.unitsInStock = self.unitsInStock + int(amount)

        self.save()

        print("added: " + str(amount) + " stocks to " + str(self.idProduct.name))


class RawMaterials(models.Model):
    idrawmaterials = models.AutoField(db_column='idRawMaterials', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=45)
    unitOfMeasure = models.CharField(db_column='unitOfMeasure', max_length=45)  # Field name made lowercase.
    idSupplier = models.ForeignKey(Supplier, on_delete=models.CASCADE,db_column='idSupplier_id')


    class Meta:
        managed = False
        db_table = 'salikneta_rawmaterials'

    @property
    def get_material_code(self):
        return self.idrawmaterials + 1000

    @staticmethod
    def get_product_count(self, branchID):
        print(self)
        rawMaterialCount = RawMaterialCount.objects.get(idrawmaterial=self.idrawmaterials, idBranch=branchID).unitsinstock
        return rawMaterialCount

    @property
    def get_num_incoming(self):
        incoming = 0
        objs = OrderLines.objects.filter(idRawMaterial_id=self.idrawmaterials)
        for o in objs:
            incoming += o.qty - o.get_delivered_products_num
        return incoming


class RawMaterialCount(models.Model):
    rawmaterialcountid = models.AutoField(db_column='rawmaterialCountID', primary_key=True)  # Field name made lowercase.
    idrawmaterial = models.ForeignKey(RawMaterials, models.CASCADE, db_column='idRawmaterial_id')  # Field name made lowercase.
    idBranch = models.ForeignKey(Branch, models.CASCADE, db_column='idBranch_id')  # Field name made lowercase.
    unitsinstock = models.FloatField(db_column='unitsInStock', blank=True, null=True)  # Field name made lowercase.
    unitsreserved = models.IntegerField(db_column='unitsReserved', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'salikneta_rawmaterialcount'

    @staticmethod
    def deduct_stock(self, amount):
        self.unitsinstock = self.unitsinstock - amount

        self.save()

        print("deducted: " + str(amount) + " stocks to " + str(self.idrawmaterial.name))


class PurchaseOrder(models.Model):
    idPurchaseOrder = models.AutoField(primary_key=True)
    idManager = models.ForeignKey(Manager, models.CASCADE, db_column='idManager_id')
    idSupplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    orderDate = models.DateField()
    expectedDate = models.DateField()
    status = models.CharField(max_length=45)
    @property
    def get_delivery(self):
        return Delivery.objects.get(idPurchaseOrder=self.idPurchaseOrder)
    @property
    def get_orderLines(self):
        return OrderLines.objects.filter(idPurchaseOrder_id=self.pk).select_related('idRawMaterial')


class OrderLines(models.Model):
    idOrderLines = models.AutoField(primary_key=True)
    idPurchaseOrder = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    idRawMaterial = models.ForeignKey(RawMaterials, models.DO_NOTHING, db_column='idRawMaterial_id')  # Field name made lowercase.
    qty = models.FloatField()

    @property
    def get_pending(self):
        return self.qty - self.get_delivered_products_num

    @property
    def get_delivered_products_num(self):
        qty = 0
        for d in DeliveredProducts.objects.filter(idOrderLines=self.idOrderLines):
            qty += d.qty
        return qty


class Delivery(models.Model):
    idDelivery = models.AutoField(primary_key=True)
    deliveryDate = models.DateField()
    idPurchaseOrder = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    @property
    def get_delivered_products(self):
        return DeliveredProducts.objects.filter(idDelivery=self)


class DeliveredProducts(models.Model):
    idDeliveredProducts = models.AutoField(primary_key=True)
    idOrderLines = models.ForeignKey(OrderLines, on_delete=models.CASCADE)
    idDelivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    qty = models.FloatField()
    @property
    def product(self):
        return self.idOrderLines.idProduct
    @property
    def date_delivered(self):
        return self.idDelivery.deliveryDate


class SalesInvoice(models.Model):
    idSales = models.AutoField(primary_key=True)
    idCashier = models.ForeignKey(Cashier, on_delete=models.CASCADE)
    invoiceDate = models.DateTimeField(db_column='invoiceDate')
    customer = models.CharField(max_length=45)

    @staticmethod
    def get_latest_invoice_num():
        try:
            si = SalesInvoice.objects.all().order_by("-idSales")[0]
            return si.idSales + 100000
        except:
            return 100000

    @staticmethod
    def get_latest_invoice_id():
        try:
            si = SalesInvoice.objects.all().order_by("-idSales")[0]
            return si.idSales + 1
        except:
            return 1
    @property
    def get_invoice_id(self):
        return 100000 + self.idSales
    @property
    def get_invoicelines(self):
        return InvoiceLines.objects.filter(idSales=self.idSales)
    @property
    def get_invoice_qty(self):
        invoices = InvoiceLines.objects.filter(idSales=self.idSales)
        qty = 0
        for i in invoices:
            qty += i.qty
        return qty
    @property
    def get_gross_invoice_amount(self):
        invoices = InvoiceLines.objects.filter(idSales=self.idSales)
        amt = 0
        for i in invoices:
            amt += i.qty * i.unitPrice
        return amt
    @property
    def get_net_invoice_amount(self):
        invoices = InvoiceLines.objects.filter(idSales=self.idSales)
        amt = 0
        for i in invoices:
            amt += i.get_net_price
        return amt

class InvoiceLines(models.Model):
    idInvoiceLines = models.AutoField(db_column='idInvoiceLines', primary_key=True)  # Field name made lowercase.
    idProduct = models.ForeignKey(Product, on_delete=models.CASCADE)
    unitPrice = models.FloatField()
    qty = models.FloatField()
    idSales = models.ForeignKey(SalesInvoice, models.DO_NOTHING, db_column='idSales')  # Field name made lowercase.
    disc = models.FloatField(blank=True, null=True)

    @property
    def get_net_price(self):
        g_amt = (self.qty * self.unitPrice)
        return g_amt - (g_amt * (self.disc / 100))


class BackLoad(models.Model):
    idBackload = models.AutoField(primary_key=True)
    idCashier = models.ForeignKey(Cashier, on_delete=models.CASCADE)
    backloadDate = models.DateField()
    @property
    def get_backload_lines(self):
        return BackloadLines.objects.filter(idBackload=self.pk)



class BackloadLines(models.Model):
    idBackloadLines = models.AutoField(primary_key=True)
    idProduct = models.ForeignKey(Product, on_delete=models.CASCADE)
    idBackload = models.ForeignKey(BackLoad, models.DO_NOTHING, db_column='idBackload', null=True)
    qty = models.FloatField()
    reason = models.CharField(max_length=45, default="Expired")


class TransferOrderProduct(models.Model):
    idTransferOrderProduct = models.AutoField(primary_key=True)
    idManager = models.ForeignKey(Manager, models.DO_NOTHING, db_column='idManager_id')  # Field name made lowercase.
    transferDate = models.DateField()
    expectedDate = models.DateField()
    source = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="sourceProduct")
    destination = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="destinationProduct")
    status = models.CharField(max_length=50)
    receivedDate = models.DateField(db_column='receivedDate', blank=True, null=True)  # Field name made lowercase.


    @property
    def get_transfer_lines(self):
        return TransferLinesProduct.objects.filter(idTransferOrderProduct=self.pk)


class TransferLinesProduct(models.Model):
    idTransferLinesProduct = models.AutoField(primary_key=True)
    idProduct = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.FloatField()
    idTransferOrderProduct = models.ForeignKey(TransferOrderProduct, on_delete=models.CASCADE)

    @property
    def get_product(self):
        return Product.objects.get(pk=int(self.idProduct.pk))


class TransferOrderRawMaterial(models.Model):
    idTransferOrderRawMaterial = models.AutoField(db_column='idTransferOrderRawMaterial', primary_key=True)  # Field name made lowercase.
    idManager = models.ForeignKey(Manager, models.CASCADE, db_column='idManager_id', blank=True, null=True)  # Field name made lowercase.
    transferDate = models.DateField(db_column='transferDate', blank=True, null=True)  # Field name made lowercase.
    expectedDate = models.DateField(db_column='expectedDate', blank=True, null=True)  # Field name made lowercase.
    source = models.ForeignKey(Branch, models.CASCADE, related_name="sourceRawMaterial")
    destination = models.ForeignKey(Branch, models.CASCADE, related_name="destinationRawMaterial")
    status = models.CharField(max_length=50, blank=True, null=True)
    receivedDate = models.DateField(db_column='receivedDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'salikneta_transferorderrawmaterial'


    @property
    def get_transfer_lines(self):
        return TransferLinesRawMaterial.objects.filter(idTransferOrderRawMaterial=self.pk)


class TransferLinesRawMaterial(models.Model):
    idTransferLinesRawMaterial = models.AutoField(db_column='idTransferLinesRawMaterial', primary_key=True)  # Field name made lowercase.
    qty = models.FloatField(blank=True, null=True)
    idRawMaterial = models.ForeignKey(RawMaterials, models.DO_NOTHING, db_column='idRawMaterial_id', blank=True, null=True)  # Field name made lowercase.
    idTransferOrderRawMaterial = models.ForeignKey(TransferOrderRawMaterial, models.DO_NOTHING, db_column='idTransferOrderRawMaterial_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '\x7fsalikneta_transferlinesrawmaterial'

    @property
    def get_raw_material(self):
        return RawMaterials.objects.get(pk=int(self.idRawMaterial.pk))


class IngredientsList(models.Model):
    ingredientslistid = models.AutoField(db_column='ingredientslistId', primary_key=True)  # Field name made lowercase.
    idProduct = models.ForeignKey(Product, on_delete=models.CASCADE)
    idrawmaterials = models.ForeignKey(RawMaterials, models.DO_NOTHING)  # Field name made lowercase.
    qtyneeded = models.FloatField(db_column='qtyNeeded')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'salikneta_ingredientlist'


class RawMaterialCountLog(models.Model):
    idRawMaterialCountLog = models.AutoField(db_column='rawMaterialCountLogID', primary_key=True)  # Field name made lowercase.
    fromCount = models.FloatField(db_column='fromCount', blank=True, null=True)  # Field name made lowercase.
    toCount = models.FloatField(db_column='toCount', blank=True, null=True)  # Field name made lowercase.
    timestamp = models.DateTimeField(blank=True, null=True)
    idManager = models.ForeignKey(Manager, models.DO_NOTHING, db_column='idManager_id', blank=True, null=True)  # Field name made lowercase.
    idRawMaterialCount = models.ForeignKey(RawMaterialCount, models.DO_NOTHING, db_column='idRawMaterialCount_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'salikneta_rawmaterialcountlog'


class ProductBatch(models.Model):
    idProductBatch = models.AutoField(db_column='idProductBatch', primary_key=True)  # Field name made lowercase.
    idProductCount = models.ForeignKey(ProductCount, models.DO_NOTHING, db_column='idProductCount_id')  # Field name made lowercase.
    manufacturedDate = models.DateField(db_column='manufacturedDate')  # Field name made lowercase.
    currentCount = models.FloatField(db_column='currentCount')  # Field name made lowercase.
    expiringDate = models.DateField(db_column='expiringDate')  # Field name made lowercase.
    status = models.CharField(max_length=45)
    idTransferOrderProduct = models.ForeignKey(TransferOrderProduct, models.DO_NOTHING,
                                               db_column='idTransferOrderProduct_id', blank=True,
                                               null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'salikneta_productbatch'