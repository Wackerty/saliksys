from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from salikneta.models import *
from django.urls import reverse
from django.contrib import messages
import calendar
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from statsmodels.tsa.ar_model import AR
from statsmodels.tsa.arima_model import ARMA, ARIMA
from random import random, randint

from django.db.models import Q
from datetime import datetime, timedelta, date
from dateutil.rrule import rrule, MONTHLY
import pandas as pd
import math


# Create your views here.

def index(request):
    return render(request, 'salikneta/login.html')


def log_in(request):
    return render(request, 'salikneta/login.html')


def log_in_validate(request):
    if request.method == "POST":

        user = request.POST.get('user')
        password = request.POST.get('password')
        try1 = Cashier.objects.filter(username=user, password=password).exists()
        try2 = Manager.objects.filter(username=user, password=password).exists()
        if try1:
            request.session['username'] = user
            request.session['usertype'] = "cashier"
            request.session['logged'] = True
            request.session['userID'] = Cashier.objects.get(username=user, password=password).idCashier
            request.session['firstname'] = Cashier.objects.get(username=user, password=password).firstname
            request.session['lastname'] = Cashier.objects.get(username=user, password=password).lastname
            request.session['branchID'] = Cashier.objects.get(username=user, password=password).idBranch.idBranch
            request.session['header'] = "salikneta/includes/cashier_header.html"
            return redirect('pos')
        elif try2:
            request.session['username'] = user

            request.session['logged'] = True

            request.session['userID'] = Manager.objects.get(username=user, password=password).idManager
            request.session['firstname'] = Manager.objects.get(username=user, password=password).firstname
            request.session['lastname'] = Manager.objects.get(username=user, password=password).lastname
            request.session['branchID'] = Manager.objects.get(username=user, password=password).idBranch.idBranch
            request.session['managerID'] = Manager.objects.get(username=user, password=password).idManager

            if request.session['branchID'] == 1:
                request.session['header'] = "salikneta/includes/marketing_header.html"
                request.session['usertype'] = "marketing"
            elif request.session['branchID'] == 2:
                request.session['header'] = "salikneta/includes/production_header.html"
                request.session['usertype'] = "production"
            elif request.session['branchID'] == 3 or request.session['branchID'] == 4:
                request.session['header'] = "salikneta/includes/animal_vegetable_header.html"
                request.session['usertype'] = "farm"
            elif request.session['branchID'] == 5 or request.session['branchID'] == 6:
                request.session['header'] = "salikneta/includes/manager_header.html"
                request.session['usertype'] = "manager"

            return redirect('home')
        else:
            messages.warning(request, 'Wrong credentials, please try again.')

    return render(request, 'salikneta/login.html')


def home(request):
    return render(request, 'salikneta/home.html', {"notifs": Notifs.objects.all().order_by("-notif_id")})


def notifications(request):
    return render(request, 'salikneta/notifications.html', {"notifs": Notifs.objects.all().order_by("-notif_id")})


def get_num_lowstock(request):
    return JsonResponse(
        {"numb": ProductCount.get_num_lowstock_items(Branch.objects.get(idBranch=request.session['branchID']))})


def get_invoice_by_id(request, idSales):
    data = []
    for il in SalesInvoice.objects.get(idSales=idSales).get_invoicelines:
        data.append({"unitPrice": il.unitPrice,
                     "qty": il.qty,
                     "disc": il.disc,
                     "net_price": il.get_net_price,
                     "productName": il.idProduct.name,
                     "uom": il.idProduct.unitOfMeasure})
    return JsonResponse({"data": data})


def sales(request):
    return render(request, 'salikneta/sales.html', {"sales_invoices": SalesInvoice.objects.all()})


def sales_report(request):
    return render(request, 'salikneta/reports/sales_report.html')


def sales_report_detail(request):
    if request.method == 'POST':
        report_data = []
        new_rd = []
        gen_info = {"message": "", "total_qty": 0, "total_sales": 0}
        products = Product.objects.all()
        for p in products:
            report_data.append({"id": p.idProduct,
                                "product": p.name,
                                "description": p.description,
                                "uom": p.unitOfMeasure,
                                "total_qty": 0,
                                "total_value": 0,
                                "sold_value": 0})
        if request.POST['type'] == "range":
            sd = request.POST["sd"].split("/")[2] + "-" + request.POST["sd"].split("/")[0] + "-" + \
                 request.POST["sd"].split("/")[1] + " 00:00:00"
            ed = request.POST["ed"].split("/")[2] + "-" + request.POST["ed"].split("/")[0] + "-" + \
                 request.POST["ed"].split("/")[1] + " 00:00:00"
            gen_info["message"] = "From " + sd + " to " + ed
            sd = datetime.strptime(sd, '%Y-%m-%d %H:%M:%S')
            ed = datetime.strptime(ed, '%Y-%m-%d %H:%M:%S')
            si = SalesInvoice.objects.filter(invoiceDate__gte=sd, invoiceDate__lte=ed)
            for r in report_data:
                for s in si:
                    for il in s.get_invoicelines:
                        if r["id"] == il.idProduct_id:
                            r["total_qty"] += il.qty
                            r["total_value"] += il.unitPrice * il.qty
                            r["sold_value"] += il.get_net_price

                            gen_info["total_sales"] += il.get_net_price
                            gen_info["total_qty"] += il.qty
            for r in report_data:
                if r["total_qty"] != 0:
                    new_rd.append(r)
        elif request.POST['type'] == "month":
            print(request.POST["month"])
            m = request.POST["month"].split("-")[1] + "-" + request.POST["month"].split("-")[0] + "-01 00:00:00"
            m = datetime.strptime(m, '%Y-%m-%d %H:%M:%S')
            si = SalesInvoice.objects.filter(invoiceDate__year=m.year)
            gen_info["message"] = "For the month of " + m.strftime('%B') + " " + str(m.year)
            for r in report_data:
                for s in si:
                    if m.month == s.invoiceDate.month:
                        for il in s.get_invoicelines:
                            if r["id"] == il.idProduct_id:
                                r["total_qty"] += il.qty
                                r["total_value"] += il.unitPrice * il.qty
                                r["sold_value"] += il.get_net_price
                                gen_info["total_sales"] += il.get_net_price
                                gen_info["total_qty"] += il.qty
            for r in report_data:
                if r["total_qty"] != 0:
                    new_rd.append(r)
        elif request.POST['type'] == "day":
            sd = request.POST["date"].split("-")[2] + "-" + request.POST["date"].split("-")[0] + "-" + \
                 request.POST["date"].split("-")[1] + " 00:00:00"
            ed = request.POST["date"].split("-")[2] + "-" + request.POST["date"].split("-")[0] + "-" + \
                 request.POST["date"].split("-")[1] + " 23:59:59"
            gen_info["message"] = "For " + request.POST["date"]
            sd = datetime.strptime(sd, '%Y-%m-%d %H:%M:%S')
            ed = datetime.strptime(ed, '%Y-%m-%d %H:%M:%S')
            si = SalesInvoice.objects.filter(invoiceDate__gte=sd, invoiceDate__lte=ed)
            for r in report_data:
                for s in si:
                    for il in s.get_invoicelines:
                        if r["id"] == il.idProduct_id:
                            r["total_qty"] += il.qty
                            r["total_value"] += il.unitPrice * il.qty
                            r["sold_value"] += il.get_net_price

                            gen_info["total_sales"] += il.get_net_price
                            gen_info["total_qty"] += il.qty
            for r in report_data:
                if r["total_qty"] != 0:
                    new_rd.append(r)
    else:
        return redirect('sales_report')
    return render(request, 'salikneta/reports/sales_report_detail.html', {"report_data": new_rd, "gen_info": gen_info})


def inventory_report(request):
    return render(request, 'salikneta/reports/inventory_report.html')


def inventory_report_detail(request):
    if request.method == 'POST':
        report_data = []
        gen_info = {"message": "", "total_sales_ct": 0,
                    "total_deliveries": 0,
                    "total_backloads": 0,
                    "transfer_in": 0,
                    "transfer_out": 0}
        products = Product.objects.all()
        branch = Branch.objects.get(pk=request.session['branchID'])

        for p in products:
            report_data.append({"id": p.idProduct,
                                "product": p.name,
                                "uom": p.unitOfMeasure,
                                "unit_price": p.suggestedUnitPrice,
                                "beg_inv": 0,
                                "transfer_in": 0,
                                "transfer_out": 0,
                                "returns": 0,
                                "sales": 0,
                                "end_inv": 0})

        if request.POST['type'] == "range":
            sd = request.POST["sd"].split("/")[2] + "-" + request.POST["sd"].split("/")[0] + "-" + \
                 request.POST["sd"].split("/")[1] + " 00:00:00"
            ed = request.POST["ed"].split("/")[2] + "-" + request.POST["ed"].split("/")[0] + "-" + \
                 request.POST["ed"].split("/")[1] + " 00:00:00"
            gen_info["message"] = "From " + sd + " to " + ed
            sd = datetime.strptime(sd, '%Y-%m-%d %H:%M:%S')
            ed = datetime.strptime(ed, '%Y-%m-%d %H:%M:%S')

            si = SalesInvoice.objects.filter(invoiceDate__gte=sd, invoiceDate__lte=ed)
            bload = BackLoad.objects.filter(backloadDate__gte=sd, backloadDate__lte=ed)
            deliv = Delivery.objects.filter(deliveryDate__gte=sd, deliveryDate__lte=ed)
            toTransferedIn = TransferOrderProduct.objects.filter(transferDate__gte=sd, transferDate__lte=ed,
                                                                 destination=branch)
            toTransferedOut = TransferOrderProduct.objects.filter(transferDate__gte=sd, transferDate__lte=ed,
                                                                  source=branch)
            for r in report_data:
                sl = 0
                backloads = 0
                deliveries = 0
                toout = 0
                toin = 0
                r["end_inv"] = Product.get_end_inventory(Product.objects.get(idProduct=r["id"]), ed, branch)
                for s in si:
                    for il in InvoiceLines.objects.filter(idSales=s, idProduct_id=r["id"]):
                        sl += il.qty
                        gen_info["total_sales_ct"] += il.qty
                for b in bload:
                    for bl in BackloadLines.objects.filter(idBackload=b, idProduct_id=r["id"]):
                        backloads += bl.qty
                        gen_info["total_backloads"] += bl.qty
                for t in toTransferedOut:
                    for tl in t.get_transfer_lines:
                        if tl.idProduct_id == r["id"]:
                            gen_info["transfer_out"] += tl.qty
                            toout += tl.qty
                for t in toTransferedIn:
                    for tl in t.get_transfer_lines:
                        if tl.idProduct_id == r["id"]:
                            gen_info["transfer_in"] += tl.qty
                            toin += tl.qty

                r["beg_inv"] = (r["end_inv"] + sl + backloads + toout) - toin
                r["deliveries"] = deliveries
                r["returns"] = backloads
                r["transfer_out"] = toout
                r["transfer_in"] = toin
                r["sales"] = sl

        elif request.POST['type'] == "month":
            m = request.POST["month"].split("-")[1] + "-" + request.POST["month"].split("-")[0] + "-01 00:00:00"
            m = datetime.strptime(m, '%Y-%m-%d %H:%M:%S')
            sd = request.POST["month"].split("-")[1] + "-" + request.POST["month"].split("-")[0] + "-01"
            ed = request.POST["month"].split("-")[1] + "-" + request.POST["month"].split("-")[0] + "-" + str(
                calendar.monthrange(m.year, m.month)[1])

            si = SalesInvoice.objects.filter(invoiceDate__gte=sd, invoiceDate__lte=ed)
            bload = BackLoad.objects.filter(backloadDate__gte=sd, backloadDate__lte=ed)
            deliv = Delivery.objects.filter(deliveryDate__gte=sd, deliveryDate__lte=ed)

            toTransferedIn = TransferOrderProduct.objects.filter(transferDate__gte=sd, transferDate__lte=ed,
                                                                 destination=branch)
            toTransferedOut = TransferOrderProduct.objects.filter(transferDate__gte=sd, transferDate__lte=ed,
                                                                  source=branch)

            gen_info["message"] = "For the month of " + m.strftime('%B') + " " + str(m.year)
            for r in report_data:
                sl = 0
                backloads = 0
                deliveries = 0
                toout = 0
                toin = 0
                r["end_inv"] = Product.get_end_inventory(Product.objects.get(idProduct=r["id"]), ed, branch)
                for t in toTransferedOut:
                    for tl in t.get_transfer_lines:
                        if tl.idProduct_id == r["id"]:
                            gen_info["transfer_out"] += tl.qty
                            toout += tl.qty
                for t in toTransferedIn:
                    for tl in t.get_transfer_lines:
                        if tl.idProduct_id == r["id"]:
                            gen_info["transfer_in"] += tl.qty
                            toin += tl.qty
                for s in si:
                    for il in InvoiceLines.objects.filter(idSales=s):
                        if il.idProduct_id == r["id"]:
                            sl += il.qty
                            gen_info["total_sales_ct"] += il.qty
                for b in bload:
                    for bl in BackloadLines.objects.filter(idBackload=b):
                        if bl.idProduct_id == r["id"]:
                            backloads += bl.qty
                        gen_info["total_backloads"] += bl.qty

                r["beg_inv"] = (r["end_inv"] + sl + backloads + toout) - toin
                r["deliveries"] = deliveries
                r["returns"] = backloads
                r["transfer_out"] = toout
                r["transfer_in"] = toin
                r["sales"] = sl
    else:
        return redirect('inventory_report')
    return render(request, 'salikneta/reports/inventory_report_detail.html',
                  {"report_data": report_data, "gen_info": gen_info})


def editItemPrice(request):
    if request.method == 'POST':
        print("waaat", request.POST['item_price'])
        print("waaat", request.POST['item_id'])
        p = Product.objects.get(idProduct=request.POST['item_id'])
        print("waaat", request.POST['item_price'])
        p.suggestedUnitPrice = float(request.POST['item_price'])
        p.save()
        Notifs.write("Price for " + p.name + " has been updated.")
    return HttpResponseRedirect(reverse('manageItems'))


def editMaterialStock(request):
    if request.method == 'POST':
        print("waaat", request.POST['item_id'])
        rc = RawMaterialCount.objects.get(idrawmaterial_id=request.POST['item_id'],
                                          idBranch__idBranch=request.session['branchID'])
        print("waaat", request.POST['e_stocks'])
        rcl = RawMaterialCountLog(fromCount=rc.unitsinstock, toCount=float(request.POST['e_stocks']),
                                  timestamp=datetime.now(),
                                  idManager=Manager.objects.get(pk=request.session['managerID']), idRawMaterialCount=rc)
        rc.unitsinstock = float(request.POST['e_stocks'])
        rc.save()
        rcl.save()
        Notifs.write(
            "Raw Material Stocks for " + rc.idrawmaterial.name + " in " + rc.idBranch.name + " branch has been updated.")
    return HttpResponseRedirect(reverse('manageRawMaterials'))


def open_notif(request):
    notifs = Notifs.objects.all()
    for n in notifs:
        n.viewed = 1
        n.save()
    return JsonResponse({"data": 'ok'})


def check_notif(request):
    notifs = Notifs.objects.all().order_by("-timestamp")[0:5]
    chk = Notifs.check_num_new_notif()
    data = []
    for n in notifs:
        data.append({"num_notif": chk,
                     "msg": n.msg
                        , "timestamp": n.get_time_ago})
    return JsonResponse({"data": data})


def pos(request):
    if request.method == 'POST':
        b = Branch.objects.get(idBranch=request.session['branchID'])
        # create Sales invoice
        si = SalesInvoice(invoiceDate=datetime.now(),
                          customer="WALK-IN",
                          idCashier_id=request.session['userID'])  # will replace to request.session['userID']
        ils = []
        itms = []
        itms_dict = {}
        pazucc = True
        items = request.POST.getlist('prod_codes[]')
        qtys = request.POST.getlist('qty[]')
        discs = request.POST.getlist('disc[]')
        for i, item in enumerate(items, 0):
            if item not in itms:
                itms.append(item)
                itms_dict[item] = 0

            prod = Product.objects.get(idProduct=item)
            il = InvoiceLines(qty=float(qtys[i]),
                              unitPrice=prod.suggestedUnitPrice,
                              disc=float(discs[i]),
                              idProduct_id=item
                              )
            itms_dict[item] += float(qtys[i])
            ils.append(il)
        for i in itms_dict:
            prod = ProductCount.objects.get(idProduct=i, idBranch=b)
            if prod.unitsInStock - itms_dict[i] < 0:
                pazucc = False
                messages.warning(request, 'Account Created.')
        if pazucc:
            for i in itms_dict:
                # prod = ProductCount.objects.get(idProduct=i, idBranch=b)
                # prod.unitsInStock = prod.unitsInStock - itms_dict[i]
                # prod.save()

                product = Product.objects.get(idProduct=i)
                # pb = product.get_earliest_expiring_batch(product, b)
                # pb.currentCount = pb.currentCount - float(itms_dict[i])
                # pb.save()

                product.deduct_stock(product, b, itms_dict[i])

            si.save()
            for i in ils:
                i.idSales = si
                i.save()
        return HttpResponseRedirect(reverse('pos'))
        # loop the arrays
    p = Product.objects.all()
    b = Branch.objects.get(pk=request.session['branchID'])

    for product in p:
        unitsInStock = product.get_product_count(product, b)
        product.unitsInStock = unitsInStock
    return render(request, 'salikneta/pos/pos.html', {'products': p,
                                                      'si_num': SalesInvoice.get_latest_invoice_num(),
                                                      'date': datetime.now(),
                                                      'categories': Category.objects.all()})


def signout(request):
    return redirect('index')


def purchaseOrder(request):
    s = Supplier.objects.all()
    i = RawMaterials.objects.all()

    b = Branch.objects.get(idBranch=request.session['branchID'])
    i = i.order_by("name")
    for rawmaterial in i:
        unitsInStock = rawmaterial.get_product_count(rawmaterial, b)
        rawmaterial.unitsInStock = unitsInStock

    purchaseOrders = PurchaseOrder.objects.filter().select_related("idSupplier").order_by('-idPurchaseOrder')

    context = {
        "suppliers": s, "branch": b, "rawmaterials": i, "purchaseOrders": purchaseOrders,
    }
    return render(request, 'salikneta/purchaseOrder.html', context)


def register(request):
    branches = Branch.objects.all()
    context = {
        "branches": branches
    }
    return render(request, 'salikneta/register.html', context)


def register_validate(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('password')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        usertype = request.POST.get('usertype')
        branch = request.POST.get('branch')
        print(branch)
        print(usertype)
        if usertype == "manager":
            manager = Manager(firstname=fname, lastname=lname, username=username, password=password, idBranch_id=branch)
            manager.save()
        if usertype == "cashier":
            cashier = Cashier(firstname=fname, lastname=lname, username=username, password=password, idBranch_id=branch)
            cashier.save()
        print("done")

        # if usertype == "os":
        #     group = Group.objects.get(name="Operations Supervisor")
        #     user.groups.add(group)
        # elif usertype == "gk":
        #     group = Group.objects.get(name="Gamekeeper")
        #     user.groups.add(group)
        # elif usertype == "own":
        #     group = Group.objects.get(name="Owner")
        #     user.groups.add(group)

        # user.save()
        messages.warning(request, 'Account Created.')
        return render(request, 'salikneta/login.html')
    return render(request, 'salikneta/register.html')


def manageCategories(request):
    c = Category.objects.all()
    context = {
        "categories": c,
    }

    return render(request, 'salikneta/manageCategories.html', context)


def manageSuppliers(request):
    s = Supplier.objects.all()
    context = {
        "suppliers": s,
    }
    return render(request, 'salikneta/manageSuppliers.html', context)


def manageItems(request, id):
    b = Branch.objects.get(idBranch=id)
    c = Category.objects.all()
    i = Product.objects.all()

    for product in i:
        unitsInStock = product.get_product_count(product, b)
        earliestExpiringBatch = product.get_earliest_expiring_batch(product, b)
        product.unitsInStock = unitsInStock
        product.earliestExpiringBatch = earliestExpiringBatch

    context = {
        "categories": c,
        "products": i,
        "branch": b,
    }
    if request.method == 'POST':
        c = Product(name=request.POST['itemName'], description=request.POST['description'],
                    suggestedUnitPrice=request.POST['price'], img_path=request.FILES['image'],
                    reorderLevel=request.POST['reorder'],
                    unitOfMeasure=request.POST['unitsOfMeasure'], SKU=request.POST['SKU'],
                    idCategory_id=request.POST['category'], expiration=request.POST['expiration'])
        c.save()

        branches = Branch.objects.all()
        currentBranch = Branch.objects.get(idBranch=request.session['branchID'])
        for branch in branches:
            if currentBranch == b:
                cc = ProductCount(idProduct=c, idBranch=branch, unitsInStock=request.POST['startStock'])
            else:
                cc = ProductCount(idProduct=c, idBranch=branch, unitsInStock=0)

            cc.save()

        Notifs.write("New Item -" + c.name + "- has been added.")
        return HttpResponseRedirect(reverse('manageItems', kwargs={'id': b.idBranch}))
    return render(request, 'salikneta/manageItems.html', context)


def manageRawMaterials(request):
    b = Branch.objects.get(idBranch=request.session['branchID'])
    r = RawMaterials.objects.all()
    s = Supplier.objects.all()

    for rawMaterial in r:
        unitsInStock = rawMaterial.get_product_count(rawMaterial, b)
        rawMaterial.unitsInStock = unitsInStock
        rawMaterial.rawMaterialCountID = RawMaterialCount.objects.get(idBranch=b,
                                                                      idrawmaterial=rawMaterial).rawmaterialcountid

    context = {
        "rawmaterials": r,
        "suppliers": s,
        "branch": b,
    }

    if request.method == 'POST':
        r = RawMaterials(name=request.POST['rawMaterialName'], unitOfMeasure=request.POST['unitsOfMeasure'],
                         idSupplier_id=request.POST['supplier'])
        r.save()

        branches = Branch.objects.all()

        for branch in branches:
            if branch == b:
                rr = RawMaterialCount(idrawmaterial=r, idBranch=branch, unitsinstock=request.POST['startStock'],
                                      unitsreserved=0)
            else:
                rr = RawMaterialCount(idrawmaterial=r, idBranch=branch, unitsinstock=0, unitsreserved=0)

            rr.save()

        Notifs.write("New Raw Material -" + r.name + "- has been added.")
        return HttpResponseRedirect(reverse('manageRawMaterials'))

    return render(request, 'salikneta/manageRawMats.html', context)


def manageIngredients(request, id):
    b = Branch.objects.get(idBranch=request.session['branchID'])
    r = RawMaterials.objects.all()
    c = Category.objects.all()
    i = Product.objects.all().order_by("name")

    #    for rawMaterial in r:
    #        unitsInStock = rawMaterial.get_product_count(rawMaterial, b)
    #        rawMaterial.unitsInStock = unitsInStock

    context = {
        "rawmaterials": r,
        "categories": c,
        "products": i,
        "productID": id
    }
    if request.method == 'POST':
        c = Product(name=request.POST['itemName'], description=request.POST['description'],
                    suggestedUnitPrice=request.POST['price'], unitsInStock=request.POST['startStock'],
                    img_path=request.FILES['image'], reorderLevel=request.POST['reorder'],
                    unitOfMeasure=request.POST['unitsOfMeasure'],
                    SKU=request.POST['SKU'], idCategory_id=request.POST['category'])
        c.save()

        Notifs.write("New Item -" + c.name + "- has been added.")
        return HttpResponseRedirect(reverse('manageIngredients'))
    return render(request, 'salikneta/manageIngredients.html', context)


def produceItems(request, id):
    r = RawMaterials.objects.all()
    c = Category.objects.all()
    i = Product.objects.all().order_by("name")
    b = Branch.objects.get(idBranch=request.session['branchID'])

    context = {
        "rawmaterials": r,
        "categories": c,
        "products": i,
        "branch": b,
        "productID": id
    }
    if request.method == 'POST':
        c = Product(name=request.POST['itemName'], description=request.POST['description'],
                    suggestedUnitPrice=request.POST['price'], unitsInStock=request.POST['startStock'],
                    img_path=request.FILES['image'], reorderLevel=request.POST['reorder'],
                    unitOfMeasure=request.POST['unitsOfMeasure'],
                    SKU=request.POST['SKU'], idCategory_id=request.POST['category'])
        c.save()

        Notifs.write("New Item -" + c.name + "- has been added.")
        return HttpResponseRedirect(reverse('manageIngredients'))
    return render(request, 'salikneta/produceItems.html', context)


def backload(request):
    branch = Branch.objects.get(pk=request.session['branchID'])
    b = BackLoad.objects.all()

    i = Product.objects.all().order_by('name')
    for product in i:
        unitsInStock = product.get_product_count(product, branch)
        product.unitsInStock = unitsInStock

    expiringProducts = ProductBatch.objects.filter(idProductCount__idBranch=branch, currentCount__gt=0)

    today = date.today()
    for product in expiringProducts:
        expiringDate = product.expiringDate
        gap = expiringDate - today
        product.daysTilExpiring = gap.days


    context = {
        "products": i, "backloads": b,
        "expiringProducts": expiringProducts,
    }
    return render(request, 'salikneta/backloads.html', context)


def transferOrderProducts(request):
    idUser = request.session['userID']
    usertype = request.session['usertype']
    branch = Branch.objects.get(pk=request.session['branchID'])

    destination = Branch.objects.filter(~Q(pk=branch.pk) & ~Q(pk=3))

    p = Product.objects.all().order_by('name')
    r = RawMaterials.objects.all()

    for product in p:
        unitsInStock = product.get_product_count(product, branch)
        product.unitsInStock = unitsInStock

    if branch.idBranch != 1:
        to = TransferOrderProduct.objects.filter(Q(source=branch) | Q(destination=branch))
    else:
        to = TransferOrderProduct.objects.all()

    to = to.order_by("-idTransferOrderProduct")

    context = {
        "source": branch,
        "destination": destination,
        "products": p,
        "transferOrders": to,
    }

    return render(request, 'salikneta/transferOrderProducts.html', context)


def transferOrderRawMaterials(request):
    idUser = request.session['userID']
    usertype = request.session['usertype']
    branch = Branch.objects.get(pk=request.session['branchID'])

    destination = Branch.objects.filter(~Q(pk=branch.pk) & ~Q(pk=5) & ~Q(pk=6))

    p = Product.objects.all().order_by('name')
    r = RawMaterials.objects.all().order_by('name')

    for product in p:
        unitsInStock = product.get_product_count(product, branch)
        product.unitsInStock = unitsInStock

    if branch.pk == 1 or branch.pk == 2 or branch.pk == 3:
        for rawMaterial in r:
            unitsInStock = rawMaterial.get_product_count(rawMaterial, branch)
            rawMaterial.unitsInStock = unitsInStock

    if branch.idBranch != 1:
        to = TransferOrderRawMaterial.objects.filter(Q(source=branch) | Q(destination=branch))
    else:
        to = TransferOrderRawMaterial.objects.all()

    to = to.order_by("-idTransferOrderRawMaterial")

    context = {
        "source": branch,
        "destination": destination,
        "products": p,
        "transferOrders": to,
        "rawMaterials": r,
    }

    return render(request, 'salikneta/transferOrderRawMaterials.html', context)


def ajaxAddCategory(request):
    print("AW")
    name = request.GET.get('categoryName')
    desc = request.GET.get('description')
    print("WEW")
    c = Category(name=name, description=desc)
    c.save()

    return HttpResponse()


def ajaxAddItem(request):
    print("AW")
    itemName = request.GET.get('itemName')
    category = request.GET.get('category')
    price = request.GET.get('price')
    SKU = request.GET.get('SKU')
    reorder = request.GET.get('reorder')
    unitsOfMeasure = request.GET.get('unitsOfMeasure')
    description = request.GET.get('description')
    print("WEW")
    c = Product(name=itemName, description=description, suggestedUnitPrice=price, unitsInStock=0,
                img_path=request.FILES['image'], reorderLevel=reorder, unitOfMeasure=unitsOfMeasure, SKU=SKU,
                idCategory_id=category)
    c.save()

    return HttpResponse()


def ajaxAddSupplier(request):
    supplierName = request.GET.get('supplierName')
    contactNumber = request.GET.get('contactNumber')
    emailAddress = request.GET.get('emailAddress')
    website = request.GET.get('website')
    address1 = request.GET.get('address1')
    address2 = request.GET.get('address2')
    city = request.GET.get('city')
    province = request.GET.get('province')
    country = request.GET.get('country')
    postal = request.GET.get('postal')

    s = Supplier(name=supplierName, contactNumber=contactNumber, emailAddress=emailAddress, website=website,
                 address1=address1, address2=address2, city=city, province=province,
                 country=country, postal=postal)
    s.save()

    return HttpResponse()


def ajaxGetUpdatedCategories(request):
    print("WaaaaaE")
    c = Category.objects.all()
    categories = []
    for x in range(0, len(c)):
        categories.append({"name": c[x].name, "description": c[x].description})

    return JsonResponse(categories, safe=False)


def ajaxGetUpdatedSuppliers(request):
    print("Waa2aaaE")
    c = Supplier.objects.all()
    suppliers = []
    for x in range(0, len(c)):
        suppliers.append({"name": c[x].name, "contactNumber": c[x].contactNumber, "emailAddress": c[x].emailAddress,
                          "address1": c[x].address1, "city": c[x].city, "country": c[x].country})

    return JsonResponse(suppliers, safe=False)


def ajaxGetUpdatedItems(request):
    print("Waa2aaaE")
    c = Product.objects.all()
    products = []
    for x in range(0, len(c)):
        products.append(
            {"name": c[x].name, "category": c[x].idCategory.name, "price": c[x].suggestedUnitPrice, "SKU": c[x].SKU,
             "reorder": c[x].reorderLevel})

    return JsonResponse(products, safe=False)


def ajaxGetDestinationStock(request):
    pk = request.GET.get('idProduct')
    branch = request.GET.get('idBranch')
    c = Product.objects.get(pk=pk)
    b = Branch.objects.get(pk=branch)
    products = []


    products.append({"idProduct": c.pk, "unitsInStock": c.get_product_count(c, b), "uom": c.unitOfMeasure})

    return JsonResponse(products, safe=False)


def ajaxGetInStockProduct(request):
    pk = request.GET.get('idProduct')
    c = Product.objects.get(pk=pk)
    b = Branch.objects.get(pk=request.session['branchID'])
    products = []

    products.append({"idProduct": c.pk, "unitsInStock": c.get_product_count(c, b), "uom": c.unitOfMeasure})

    return JsonResponse(products, safe=False)


def ajaxGetInStock(request):
    pk = request.GET.get('idProduct')
    c = RawMaterials.objects.get(pk=pk)
    b = Branch.objects.get(pk=request.session['branchID'])
    products = []

    products.append({"idProduct": c.pk, "unitsInStock": c.get_product_count(c, b), "incoming": c.get_num_incoming})

    return JsonResponse(products, safe=False)


def ajaxGetInStockRawMaterials(request):
    pk = request.GET.get('idRawMaterial')
    c = RawMaterials.objects.get(pk=pk)
    b = Branch.objects.get(pk=request.session['branchID'])
    rawmaterials = []

    rawmaterials.append({"idProduct": c.pk, "unitsInStock": c.get_product_count(c, b), "uom": c.unitOfMeasure})

    return JsonResponse(rawmaterials, safe=False)


def ajaxAddPurchaseOrder(request):
    products = request.GET.getlist('products[]')
    quantity = request.GET.getlist('quantity[]')
    supplier = request.GET.get('supplier')
    shipTo = request.GET.get('shipTo')
    orderDate = request.GET.get('orderDate')
    expectedDate = request.GET.get('expectedDate')

    po = PurchaseOrder(orderDate=datetime.strptime(orderDate, '%d-%m-%Y').strftime('%Y-%m-%d')
                       , expectedDate=datetime.strptime(expectedDate, '%d-%m-%Y').strftime('%Y-%m-%d')
                       , idManager_id=request.session['userID'], idSupplier_id=supplier, status="In Transit")
    po.save()

    for x in range(0, len(products)):
        orderLine = OrderLines(qty=quantity[x], idRawMaterial_id=products[x], idPurchaseOrder_id=po.pk)
        orderLine.save()

    Notifs.write("New PO" + str(po.pk) + " has been added.")
    print("Success")

    return JsonResponse([], safe=False)


def ajaxAddBackload(request):
    products = request.GET.getlist('products[]')
    quantity = request.GET.getlist('quantity[]')
    reasons = request.GET.getlist('reasons[]')

    backloadDate = datetime.now().strftime("%Y-%m-%d")
    b = BackLoad(backloadDate=backloadDate, idCashier_id=request.session['userID'])
    b.save()

    for x in range(0, len(products)):
        b1 = BackloadLines(qty=quantity[x], idProduct_id=products[x], reason=reasons[x], idBackload_id=b.pk)
        b1.save()
        p = Product.objects.get(pk=products[x])
        p.deduct_stock(p, b.idCashier.idBranch, int(quantity[x]))
        # pc = ProductCount.objects.get(idProduct=p, idBranch=b.idCashier.idBranch)
        # pc.unitsInStock = pc.unitsInStock - int(quantity[x])
        # pc.save()
        # pb = p.get_earliest_expiring_batch(p, branchID=b.idCashier.idBranch)
        # pb.currentCount = pb.currentCount - int(quantity[x])
        # pb.save()

    Notifs.write("Products have been backloaded.")
    # po = PurchaseOrder(orderDate=datetime.datetime.strptime(orderDate, '%d-%m-%Y').strftime('%Y-%m-%d')
    # ,expectedDate=datetime.datetime.strptime(expectedDate, '%d-%m-%Y').strftime('%Y-%m-%d')
    # , idCashier_id=request.session['userID'], idSupplier_id = supplier,status="In Transit")
    # po.save()

    # for x in range(0, len(products)):
    #     orderLine = OrderLines(qty=quantity[x],idProduct_id=products[x],idPurchaseOrder_id=po.pk)
    #     orderLine.save()

    return JsonResponse([], safe=False)


def ajaxSaveDelivery(request):
    print("WEW")
    products = request.GET.getlist('products[]')
    quantity = request.GET.getlist('quantity[]')
    ordered = request.GET.getlist('ordered[]')
    lines = request.GET.getlist('lines[]')
    idPurchaseOrder = request.GET.get('idPurchaseOrder')
    b = Branch.objects.get(pk=request.session['branchID'])

    deliveryDate = datetime.now().strftime("%Y-%m-%d")

    d = Delivery(deliveryDate=deliveryDate, idPurchaseOrder_id=idPurchaseOrder)
    d.save()

    isOkay = True
    hasExcess = False
    # print(len(ordered))
    # print(len(quantity))
    # print(len(products))
    for x in range(0, len(products)):
        d1 = DeliveredProducts(qty=quantity[x], idDelivery_id=d.pk, idOrderLines_id=lines[x])
        d1.save()
        p = RawMaterials.objects.get(pk=products[x])
        pc = RawMaterialCount.objects.get(idrawmaterial=p, idBranch=b)
        if float(ordered[x]) != float(quantity[x]) and float(ordered[x]) > float(quantity[x]):
            # print(float(p.unitsInStock))
            # print(float(quantity[x]))
            isOkay = False

        pc.unitsinstock = int(pc.unitsinstock) + int(quantity[x])
        pc.save()

    qwe = PurchaseOrder.objects.get(pk=idPurchaseOrder)

    orderLines = qwe.get_orderLines

    for orderLine in orderLines:
        if orderLine.get_pending < 0:
            hasExcess = True

    if isOkay == True and hasExcess == False:
        qwe.status = "RECEIVED"
        qwe.save()
    elif isOkay == True and hasExcess == True:
        qwe.status = "RECEIVED WITH EXCESS"
        qwe.save()
    else:
        qwe.status = "PARTIALLY RECEIVED"
        qwe.save()

    return JsonResponse([], safe=False)


def ajaxTransferOrder(request):
    products = request.GET.getlist('products[]')
    quantity = request.GET.getlist('quantity[]')

    source = request.GET.get('source')
    destination = request.GET.get('destination')
    transferDate = request.GET.get('transferDate')
    expectedDate = request.GET.get('expectedDate')

    to = TransferOrderProduct(transferDate=datetime.strptime(transferDate, '%d-%m-%Y').strftime('%Y-%m-%d'),
                              expectedDate=datetime.strptime(expectedDate, '%d-%m-%Y').strftime('%Y-%m-%d'),
                              idManager=Manager.objects.get(pk=request.session['userID']), source_id=source,
                              destination_id=destination, status="Pending for Request")
    b = to.source
    to.save()

    if to.destination.pk != 1 and to.source.pk != 1:
        for x in range(0, len(products)):
            tl = TransferLinesProduct(qty=quantity[x], idProduct_id=products[x], idTransferOrderProduct_id=to.pk)
            tl.save()
            p = Product.objects.get(pk=products[x])
            p.transfer_stock(p, b, quantity[x], to)
            pc = ProductCount.objects.get(idProduct=p, idBranch=b)
            pc.unitsReserved = int(pc.unitsReserved) + int(quantity[x])
            pc.save()

            # toTransfer = float(quantity[x])
            #
            # p.transfer_stock(p, b, quantity[x], to)
            # #while toTransfer >= 0:
            # pb = p.get_earliest_expiring_batch(p, b)
            # #if (pb.currentCount-toTransfer) >= 0:
            # pb.currentCount = pb.currentCount - toTransfer
            # pb.save()
            #
            # destinationPC = ProductCount.objects.get(idProduct=p, idBranch=to.destination)
            # newPb = ProductBatch(idProductCount=destinationPC,
            #                      manufacturedDate=pb.manufacturedDate,
            #                      currentCount=float(quantity[x]), expiringDate=pb.expiringDate, status="Transit", idTransferOrderProduct=to)
            #
            # newPb.save()

            tl.save()

        Notifs.write("Transfer Order for Products (TO# " + str(
            to.idTransferOrderProduct) + ") from " + to.source.name + " to " + to.destination.name + " has been made.")
    else:
        for x in range(0, len(products)):
            tl = TransferLinesProduct(qty=quantity[x], idProduct_id=products[x], idTransferOrderProduct_id=to.pk)
            tl.save()
            p = Product.objects.get(pk=products[x])
            p.transfer_stock(p, b, quantity[x], to)
            pc = ProductCount.objects.get(idProduct=p, idBranch=b)
            pc.unitsReserved = int(pc.unitsReserved) + int(quantity[x])
            pc.save()
            to.status = "In Transit"
            to.save()
            # pb = p.get_earliest_expiring_batch(p, b)
            # pb.currentCount = pb.currentCount - float(quantity[x])
            # pb.save()
            #
            # destinationPC = ProductCount.objects.get(idProduct=p, idBranch=to.destination)
            # newPb = ProductBatch(idProductCount=destinationPC,
            #                      manufacturedDate=pb.manufacturedDate,
            #                      currentCount=float(quantity[x]), expiringDate=pb.expiringDate, status="Transit", idTransferOrderProduct=to)
            # newPb.save()

            tl.save()

        Notifs.write("Transfer Order for Products (TO# " + str(
            to.idTransferOrderProduct) + ") from " + to.source.name + " to " + to.destination.name + " has been made and is in transit.")

    return JsonResponse([], safe=False)


def ajaxTransferOrderRawMaterials(request):
    products = request.GET.getlist('products[]')
    quantity = request.GET.getlist('quantity[]')

    source = request.GET.get('source')
    destination = request.GET.get('destination')
    transferDate = request.GET.get('transferDate')
    expectedDate = request.GET.get('expectedDate')

    to = TransferOrderRawMaterial(transferDate=datetime.strptime(transferDate, '%d-%m-%Y').strftime('%Y-%m-%d'),
                                  expectedDate=datetime.strptime(expectedDate, '%d-%m-%Y').strftime('%Y-%m-%d'),
                                  idManager=Manager.objects.get(pk=request.session['userID']), source_id=source,
                                  destination_id=destination, status="Pending for Request")
    b = to.source
    to.save()

    if to.destination.pk != 1:
        for x in range(0, len(products)):
            tl = TransferLinesRawMaterial(qty=quantity[x], idRawMaterial_id=products[x],
                                          idTransferOrderRawMaterial_id=to.pk)
            tl.save()
            p = RawMaterials.objects.get(pk=products[x])
            pc = RawMaterialCount.objects.get(idrawmaterial=p, idBranch=b)
            pc.unitsinstock = int(pc.unitsinstock) - int(quantity[x])
            pc.unitsreserved = int(pc.unitsreserved) + int(quantity[x])
            pc.save()

        Notifs.write("Transfer Order for Raw Materials (TO# " + str(
            to.idTransferOrderRawMaterial) + ") from " + to.source.name + " to " + to.destination.name + " has been made.")
    else:
        for x in range(0, len(products)):
            tl = TransferLinesRawMaterial(qty=quantity[x], idRawMaterial_id=products[x],
                                          idTransferOrderRawMaterial_id=to.pk)
            tl.save()
            p = RawMaterials.objects.get(pk=products[x])
            pc = RawMaterialCount.objects.get(idrawmaterial=p, idBranch=b)
            pc.unitsinstock = int(pc.unitsinstock) - int(quantity[x])
            pc.save()
            to.status = "In Transit"
            to.save()

        Notifs.write("Transfer Order for Raw Materials (TO# " + str(
            to.idTransferOrderRawMaterial) + ") from " + to.source.name + " to " + to.destination.name + " has been made and is in transit.")

    return JsonResponse([], safe=False)


def ajaxInTransitTO(request):
    idTO = request.GET.get('idTransferOrder')
    to = TransferOrderProduct.objects.get(pk=int(idTO))
    b = to.source
    wew = to.get_transfer_lines
    for x in range(0, len(wew)):
        aw = wew[x].idProduct
        pc = ProductCount.objects.get(idProduct=aw, idBranch=b)
        pc.unitsReserved = pc.unitsReserved - int(wew[x].qty)
        pc.save()

    to.status = "In Transit"
    to.save()
    Notifs.write(
        "Transfer Order for Products (TO# " + str(
            to.idTransferOrderProduct) + ") from " + to.source.name + " to " + to.destination.name + " is in transit.")
    return JsonResponse([], safe=False)


def ajaxInTransitTORawMaterial(request):
    idTO = request.GET.get('idTransferOrder')
    to = TransferOrderRawMaterial.objects.get(pk=int(idTO))
    b = to.source
    wew = to.get_transfer_lines
    for x in range(0, len(wew)):
        aw = wew[x].idRawMaterial
        pc = RawMaterialCount.objects.get(idrawmaterial=aw, idBranch=b)
        pc.unitsreserved = pc.unitsreserved - int(wew[x].qty)
        pc.save()

    to.status = "In Transit"
    to.save()
    Notifs.write(
        "Transfer Order for Raw Materials (TO# " + str(
            to.idTransferOrderRawMaterial) + ") from " + to.source.name + " to " + to.destination.name + " is in transit.")
    return JsonResponse([], safe=False)


def ajaxFinishedTO(request):
    idTO = request.GET.get('idTransferOrder')
    to = TransferOrderProduct.objects.get(pk=int(idTO))
    b = to.destination
    wew = to.get_transfer_lines

    for x in range(0, len(wew)):
        aw = wew[x].idProduct
        pc = ProductCount.objects.get(idProduct=aw, idBranch=b)
        print(pc.unitsInStock)
        pc.unitsInStock = pc.unitsInStock + int(wew[x].qty)
        print(pc.unitsInStock)
        pc.save()

    pb = ProductBatch.objects.filter(idTransferOrderProduct=to)

    for batch in pb:
        if ProductBatch.objects.filter(idProductCount=batch.idProductCount, manufacturedDate=batch.manufacturedDate, status="In stock").exists():
            check = ProductBatch.objects.get(idProductCount=batch.idProductCount,
                                             manufacturedDate=batch.manufacturedDate, status="In stock")
            check.currentCount = check.currentCount + batch.currentCount
            check.status = "In stock"
            check.save()
            batch.delete()
        else:
            batch.status = "In stock"
            batch.save()



    to.status = "Received"
    to.receivedDate = date.today()
    to.save()
    Notifs.write(
        "Transfer Order for Products (TO# " + str(
            to.idTransferOrderProduct) + ") from " + to.source.name + " to " + to.destination.name + " is received.")
    return JsonResponse([], safe=False)


def ajaxFinishedTORawMaterial(request):
    idTO = request.GET.get('idTransferOrder')
    to = TransferOrderRawMaterial.objects.get(pk=int(idTO))
    b = to.destination
    wew = to.get_transfer_lines

    for x in range(0, len(wew)):
        aw = wew[x].idRawMaterial
        pc = RawMaterialCount.objects.get(idrawmaterial=aw, idBranch=b)
        print(pc.unitsinstock)
        pc.unitsinstock = pc.unitsinstock + int(wew[x].qty)
        print(pc.unitsinstock)
        pc.save()

    to.status = "Received"
    to.receivedDate = date.today()
    to.save()
    Notifs.write(
        "Transfer Order for Raw Materials (TO# " + str(
            to.idTransferOrderRawMaterial) + ") from " + to.source.name + " to " + to.destination.name + " is received.")
    return JsonResponse([], safe=False)


def ajaxCancelTO(request):
    idTO = request.GET.get('idTransferOrder')
    to = TransferOrderProduct.objects.get(pk=int(idTO))
    b = to.source
    wew = to.get_transfer_lines
    for x in range(0, len(wew)):
        aw = wew[x].idProduct
        pc = ProductCount.objects.get(idProduct=aw, idBranch=b)
        pc.unitsReserved = pc.unitsReserved - int(wew[x].qty)
        print(pc.unitsInStock)
        pc.unitsInStock = pc.unitsInStock + int(wew[x].qty)
        print(pc.unitsInStock)
        pc.save()

    pb = ProductBatch.objects.filter(idTransferOrderProduct=to)

    for batch in pb:
        batch.status = "Cancelled"
        batch.save()

    to.status = "Cancelled"
    to.save()
    Notifs.write(
        "Transfer Order for Products (TO# " + str(
            to.idTransferOrderProduct) + ") from " + to.source.name + " to " + to.destination.name + " is cancelled.")
    return JsonResponse([], safe=False)


def ajaxCancelTORawMaterial(request):
    idTO = request.GET.get('idTransferOrder')
    to = TransferOrderRawMaterial.objects.get(pk=int(idTO))
    b = to.source
    wew = to.get_transfer_lines
    for x in range(0, len(wew)):
        aw = wew[x].idRawMaterial
        pc = RawMaterialCount.objects.get(idrawmaterial=aw, idBranch=b)
        pc.unitsreserved = pc.unitsreserved - int(wew[x].qty)
        print(pc.unitsinstock)
        pc.unitsinstock = pc.unitsinstock + int(wew[x].qty)
        print(pc.unitsinstock)
        pc.save()
    to.status = "Cancelled"
    to.save()
    Notifs.write(
        "Transfer Order for Raw Materials (TO# " + str(
            to.idTransferOrderRawMaterial) + ") from " + to.source.name + " to " + to.destination.name + " is cancelled.")
    return JsonResponse([], safe=False)


def ajaxGetIngredients(request):
    pk = request.GET.get('productPk')
    print(pk)
    i = IngredientsList.objects.filter(idProduct=pk).order_by('idProduct__name')
    b = Branch.objects.get(idBranch=request.session['branchID'])
    ingredients = []

    for ingredient in i:
        if b.idBranch == 5 or b.idBranch == 6:
            ingredients.append({"pk": ingredient.pk, "rawMaterialName": ingredient.idrawmaterials.name,
                                "qtyneeded": ingredient.qtyneeded, "uom": ingredient.idrawmaterials.unitOfMeasure})
        else:
            ingredients.append({"pk": ingredient.pk, "rawMaterialName": ingredient.idrawmaterials.name,
                                "qtyneeded": ingredient.qtyneeded, "uom": ingredient.idrawmaterials.unitOfMeasure,
                                "unitsInStock": ingredient.idrawmaterials.get_product_count(ingredient.idrawmaterials,
                                                                                            b)})

    return JsonResponse(ingredients, safe=False)


def ajaxGetBatches(request):
    pk = request.GET.get('productPk')
    b = Branch.objects.get(idBranch=request.session['branchID'])
    pc = ProductCount.objects.get(idProduct= pk, idBranch=b)
    pb = ProductBatch.objects.filter(idProductCount=pc, status="In stock", currentCount__gt=0).order_by('manufacturedDate')

    batches = []

    for batch in pb:
        batches.append({
            "manufacturedDate": batch.manufacturedDate,
            "currentCount": batch.currentCount,
            "expiringDate": batch.expiringDate,
        })

    return JsonResponse(batches, safe=False)


def ajaxGetRawMaterialCountLogs(request):
    pk = request.GET.get('rawMaterialCountID')
    print(pk)

    r = RawMaterialCountLog.objects.filter(idRawMaterialCount=pk).order_by('-timestamp')

    logs = []

    for log in r:
        logs.append({"fromCount": log.fromCount,
                     "toCount": log.toCount,
                     "timestamp": log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                     "manager": log.idManager.firstname + " " + log.idManager.lastname,
                     })

    return JsonResponse(logs, safe=False)


def ajaxGetAmountCanProduce(request):
    pk = request.GET.get('productPk')
    b = Branch.objects.get(idBranch=request.session['branchID'])
    ingredients = []

    p = Product.objects.get(idProduct=pk)

    ingredients.append({"amount": p.get_amount_can_produce(p, b),
                        "unitsInStock": ProductCount.objects.get(idProduct=p, idBranch=b).unitsInStock,
                        "uom": p.unitOfMeasure
                        })

    return JsonResponse(ingredients, safe=False)


def ajaxGetUOM(request):
    pk = request.GET.get('productPk')
    i = RawMaterials.objects.get(idrawmaterials=pk)
    uom = []

    uom.append({"uom": i.unitOfMeasure})

    return JsonResponse(uom, safe=False)


def ajaxAddIngredient(request):
    productPK = request.GET.get('productPK')
    rawMaterialPK = request.GET.get('rawMaterialPK')
    qtyNeeded = request.GET.get('qtyNeeded')

    product = Product.objects.get(idProduct=productPK)
    rawmaterial = RawMaterials.objects.get(idrawmaterials=rawMaterialPK)

    i = IngredientsList(idProduct=product, idrawmaterials=rawmaterial,
                        qtyneeded=qtyNeeded)
    i.save()

    Notifs.write("New Ingredient -" + i.idrawmaterials.name + "- for -" + i.idProduct.name + "- has been added.")

    i = IngredientsList.objects.filter(idProduct=productPK)
    ingredients = []

    for ingredient in i:
        ingredients.append({"rawMaterialName": ingredient.idrawmaterials.name, "qtyneeded": ingredient.qtyneeded,
                            "uom": ingredient.idProduct.unitOfMeasure, "pk": ingredient.ingredientslistid})

    return JsonResponse(ingredients, safe=False)


def ajaxRemoveIngredient(request):
    ingredientID = request.GET.get('ingredientID')

    ingredient = IngredientsList.objects.get(ingredientslistid=ingredientID)

    productPK = ingredient.idProduct

    Notifs.write(
        "Ingredient -" + ingredient.idrawmaterials.name + "- for -" + ingredient.idProduct.name + "- has been removed.")

    ingredient.delete()

    i = IngredientsList.objects.filter(idProduct=productPK)
    ingredients = []

    for ingredient in i:
        ingredients.append({"rawMaterialName": ingredient.idrawmaterials.name, "qtyneeded": ingredient.qtyneeded,
                            "uom": ingredient.idProduct.unitOfMeasure})

    return JsonResponse(ingredients, safe=False)


def ajaxProduceItems(request):
    pk = request.GET.get('productPK')
    amount = request.GET.get('amount')
    b = Branch.objects.get(idBranch=request.session['branchID'])

    p = Product.objects.get(idProduct=pk)
    pc = ProductCount.objects.get(idProduct=p, idBranch=b)

    pc.add_stocks(pc, amount)

    i = IngredientsList.objects.filter(idProduct=p)
    ingredients = []

    for ingredient in i:
        ingredients.append({"rawMaterialName": ingredient.idrawmaterials.name,
                            "qtyneeded": ingredient.qtyneeded,
                            "uom": ingredient.idProduct.unitOfMeasure,
                            "unitsInStock": ingredient.idrawmaterials.get_product_count(ingredient.idrawmaterials, b),
                            "unitsInStockProduct": pc.unitsInStock,
                            "amount": p.get_amount_can_produce(p, b)})

    Notifs.write("Produced " + amount + " stocks for product: " + p.name)

    batch = ProductBatch(idProductCount=pc, manufacturedDate=date.today(),
                         currentCount=amount, expiringDate=date.today()+timedelta(days=p.expiration), status="In stock")

    if ProductBatch.objects.filter(idProductCount=batch.idProductCount, manufacturedDate=batch.manufacturedDate).exists():
        check = ProductBatch.objects.filter(idProductCount=batch.idProductCount, manufacturedDate=batch.manufacturedDate)[0]
        check.currentCount = check.currentCount + float(batch.currentCount)
        check.save()
    else:
        batch.save()

    return JsonResponse(ingredients, safe=False)


def get(request):
    si = SalesInvoice.objects.earliest('invoiceDate')
    bload = BackLoad.objects.earliest('backloadDate')
    deliv = Delivery.objects.earliest('deliveryDate')
    to = TransferOrderProduct.objects.earliest('transferDate')
    earliestDate = min([si.invoiceDate.date(), bload.backloadDate, deliv.deliveryDate, to.transferDate])

    monthYear = str(earliestDate.month) + "-" + str(earliestDate.year)

    print(monthYear)

    report_data = []
    gen_info = {"message": "", "total_sales_ct": 0,
                "total_deliveries": 0,
                "total_backloads": 0,
                "transfer_out": 0}
    products = Product.objects.all()
    branch = Branch.objects.get(pk=request.session['branchID'])

    for p in products:
        report_data.append({"id": p.idProduct,
                            "product": p.name,
                            "uom": p.unitOfMeasure,
                            "unit_price": p.suggestedUnitPrice,
                            "beg_inv": 0,
                            "transfer_out": 0,
                            "deliveries": 0,
                            "returns": 0,
                            "sales": 0,
                            "end_inv": 0})

    m = monthYear.split("-")[1] + "-" + monthYear.split("-")[0] + "-01 00:00:00"
    m = datetime.strptime(m, '%Y-%m-%d %H:%M:%S')
    sd = monthYear.split("-")[1] + "-" + monthYear.split("-")[0] + "-01"
    ed = monthYear.split("-")[1] + "-" + monthYear.split("-")[0] + "-" + str(
        calendar.monthrange(m.year, m.month)[1])

    si = SalesInvoice.objects.filter(invoiceDate__gte=sd, invoiceDate__lte=ed)
    bload = BackLoad.objects.filter(backloadDate__gte=sd, backloadDate__lte=ed)
    deliv = Delivery.objects.filter(deliveryDate__gte=sd, deliveryDate__lte=ed)

    to = TransferOrderProduct.objects.filter(transferDate__gte=sd, transferDate__lte=ed)
    gen_info["message"] = "For the month of " + m.strftime('%B') + " " + str(m.year)
    for r in report_data:
        sl = 0
        backloads = 0
        deliveries = 0
        tos = 0
        r["end_inv"] = Product.get_end_inventory(Product.objects.get(idProduct=r["id"]), ed, branch)
        for d in deliv:
            for del_prods in d.get_delivered_products:
                if del_prods.product.idProduct == r["id"]:
                    deliveries += del_prods.qty
                    gen_info["total_deliveries"] += del_prods.qty
        for t in to:
            for tl in t.get_transfer_lines:
                if tl.idProduct_id == r["id"]:
                    gen_info["transfer_out"] += tl.qty
                    tos += tl.qty

        for s in si:
            for il in InvoiceLines.objects.filter(idSales=s):
                if il.idProduct_id == r["id"]:
                    sl += il.qty
                    gen_info["total_sales_ct"] += il.qty
        for b in bload:
            for bl in BackloadLines.objects.filter(idBackload=b):
                if bl.idProduct_id == r["id"]:
                    backloads += bl.qty
                gen_info["total_backloads"] += bl.qty

        r["beg_inv"] = (r["end_inv"] + sl + backloads + tos) - deliveries
        r["deliveries"] = deliveries
        r["returns"] = backloads
        r["transfer_out"] = tos
        r["sales"] = sl

    return render(request, 'salikneta/reports/inventory_report_detail.html',
                  {"report_data": report_data, "gen_info": gen_info})


def inventory_report_per_month(dates, branchPK):
    needed_info = []
    for d in dates:
        monthYear = str(d.month) + "-" + str(d.year)
        report_data = []
        gen_info = {"message": "",
                    "total_sales_ct": 0,
                    "total_deliveries": 0,
                    "total_backloads": 0,
                    "transfer_out": 0,
                    "report_data": []}
        products = Product.objects.all()
        branch = Branch.objects.get(idBranch=branchPK)

        m = monthYear.split("-")[1] + "-" + monthYear.split("-")[0] + "-01 00:00:00"
        m = datetime.strptime(m, '%Y-%m-%d %H:%M:%S')
        sd = monthYear.split("-")[1] + "-" + monthYear.split("-")[0] + "-01"
        ed = monthYear.split("-")[1] + "-" + monthYear.split("-")[0] + "-" + str(
            calendar.monthrange(m.year, m.month)[1])

        for p in products:
            report_data.append({"id": p.idProduct,
                                "product": p.name,
                                "uom": p.unitOfMeasure,
                                "unit_price": p.suggestedUnitPrice,
                                "beg_inv": 0,
                                "transfer_out": 0,
                                "deliveries": 0,
                                "returns": 0,
                                "sales": 0,
                                "end_inv": 0,
                                "when": m.strftime('%B') + " " + str(m.year)})

        si = SalesInvoice.objects.filter(invoiceDate__gte=sd, invoiceDate__lte=ed)
        bload = BackLoad.objects.filter(backloadDate__gte=sd, backloadDate__lte=ed)
        deliv = Delivery.objects.filter(deliveryDate__gte=sd, deliveryDate__lte=ed)

        to = TransferOrderProduct.objects.filter(transferDate__gte=sd, transferDate__lte=ed)
        gen_info["message"] = "For the month of " + m.strftime('%B') + " " + str(m.year)
        for r in report_data:
            sl = 0
            backloads = 0
            deliveries = 0
            tos = 0
            r["end_inv"] = Product.get_end_inventory(Product.objects.get(idProduct=r["id"]), ed, branch)
            for d in deliv:
                for del_prods in d.get_delivered_products:
                    if del_prods.product.idProduct == r["id"]:
                        deliveries += del_prods.qty
                        gen_info["total_deliveries"] += del_prods.qty
            for t in to:
                for tl in t.get_transfer_lines:
                    if tl.idProduct_id == r["id"]:
                        gen_info["transfer_out"] += tl.qty
                        tos += tl.qty

            for s in si:
                for il in InvoiceLines.objects.filter(idSales=s):
                    if il.idProduct_id == r["id"]:
                        sl += il.qty
                        gen_info["total_sales_ct"] += il.qty
            for b in bload:
                for bl in BackloadLines.objects.filter(idBackload=b):
                    if bl.idProduct_id == r["id"]:
                        backloads += bl.qty
                    gen_info["total_backloads"] += bl.qty

            r["beg_inv"] = (r["end_inv"] + sl + backloads + tos) - deliveries
            r["deliveries"] = deliveries
            r["returns"] = backloads
            r["transfer_out"] = tos
            r["sales"] = randint(1, 101)
            # r["sales"] = sl

        gen_info["report_data"] = report_data
        needed_info.append(gen_info)

    return needed_info


def inventory_sales_per_month(dates, productPK):
    needed_info = []
    for d in dates:
        monthYear = str(d.month) + "-" + str(d.year)
        report_data = []
        gen_info = {"report_data": []}
        products = Product.objects.filter(idProduct=productPK)

        m = monthYear.split("-")[1] + "-" + monthYear.split("-")[0] + "-01 00:00:00"
        m = datetime.strptime(m, '%Y-%m-%d %H:%M:%S')
        sd = monthYear.split("-")[1] + "-" + monthYear.split("-")[0] + "-01"
        ed = monthYear.split("-")[1] + "-" + monthYear.split("-")[0] + "-" + str(
            calendar.monthrange(m.year, m.month)[1]) + " 23:59:59"

        endMonthDate = datetime.strptime(monthYear.split("-")[1] + "-" + monthYear.split("-")[0] + "-" + str(
            calendar.monthrange(m.year, m.month)[1]) + " 23:59:59", '%Y-%m-%d %H:%M:%S').date()

        for p in products:
            report_data.append({"id": p.idProduct,
                                "product": p.name,
                                "uom": p.unitOfMeasure,
                                "sales_marketing": 0,
                                "sales_taft": 0,
                                "sales_malabon": 0,
                                "total_sales": 0,
                                "end_inv": 0,
                                "when": m.strftime('%B') + " " + str(m.year),
                                "date": endMonthDate})

        si = SalesInvoice.objects.filter(invoiceDate__gte=sd, invoiceDate__lte=ed)

        for r in report_data:
            sl = 0
            sales_marketing = 0
            sales_taft = 0
            sales_malabon = 0
            for s in si:
                for il in InvoiceLines.objects.filter(idSales=s):
                    if il.idProduct_id == r["id"]:
                        if il.idSales.idCashier.idBranch.idBranch == 1:
                            sales_marketing += il.qty
                        elif il.idSales.idCashier.idBranch.idBranch == 5:
                            sales_taft += il.qty
                        else:
                            sales_malabon += il.qty
                        sl += il.qty

            # r["sales_marketing"] = randint(1,101)
            # r["sales_taft"] = randint(1,101)
            # r["sales_malabon"] = randint(1,101)

            r["sales_marketing"] = sales_marketing
            r["sales_taft"] = sales_taft
            r["sales_malabon"] = sales_malabon
            r["total_sales"] = sl

        gen_info["report_data"] = report_data
        needed_info.append(gen_info)

    return needed_info


def forecasting_detail(request, id, method):
    si = SalesInvoice.objects.earliest('invoiceDate')
    earliestDate = min([si.invoiceDate.date()])
    today = date.today()

    three_months = date.today() + relativedelta(months=+3)

    next_three_month_dates = [dt for dt in rrule(MONTHLY, dtstart=today + relativedelta(months=+1), until=three_months)]

    dates = [dt for dt in rrule(MONTHLY, dtstart=earliestDate, until=today)]

    if id == 0:
        awit = inventory_sales_per_month(dates, Product.objects.first().pk)
        productID = Product.objects.first().pk
        productName = Product.objects.first().name
        ingredients = IngredientsList.objects.filter(idProduct=productID)
        product = Product.objects.first()
    else:
        awit = inventory_sales_per_month(dates, Product.objects.get(idProduct=id).pk)
        productID = Product.objects.get(idProduct=id).idProduct
        productName = Product.objects.get(idProduct=id).name
        ingredients = IngredientsList.objects.filter(idProduct=productID)
        product = Product.objects.get(idProduct=id)

    product_inventory_sales = []
    for row in awit:
        product_inventory_sales.append(row['report_data'][0])

    productMarketingSales = []
    productTaftSales = []
    productMalabonSales = []
    for row in product_inventory_sales:
        productMarketingSales.append(row['sales_marketing'])
        productTaftSales.append(row['sales_taft'])
        productMalabonSales.append(row['sales_malabon'])

    forecast_next_three_months = []

    for x in next_three_month_dates:
        forecast_next_three_months.append({
            "date": x.date(),
            "forecast_marketing": 0,
            "forecast_taft": 0,
            "forecast_malabon": 0,
        })

    temp1 = productMarketingSales
    temp2 = productTaftSales
    temp3 = productMalabonSales

    if method == "ar":
        marketingProductForecast = abs(int(forecast_autoregression(productMarketingSales)))
        taftProductForecast = abs(int(forecast_autoregression(productTaftSales)))
        malabonProductForecast = abs(int(forecast_autoregression(productMalabonSales)))

        for y in forecast_next_three_months:
            yes1 = abs(int(forecast_autoregression(temp1)))
            yes2 = abs(int(forecast_autoregression(temp2)))
            yes3 = abs(int(forecast_autoregression(temp3)))

            y['forecast_marketing'] = yes1
            y['forecast_taft'] = yes2
            y['forecast_malabon'] = yes3

            temp1.append(yes1)
            temp2.append(yes2)
            temp3.append(yes3)

        forecastingMethod = "Autoregression"

    elif method == "ma":
        marketingProductForecast = abs(int(forecast_moving_average(productMarketingSales)))
        taftProductForecast = abs(int(forecast_moving_average(productTaftSales)))
        malabonProductForecast = abs(int(forecast_moving_average(productMalabonSales)))

        for y in forecast_next_three_months:
            yes1 = abs(int(forecast_moving_average(temp1)))
            yes2 = abs(int(forecast_moving_average(temp2)))
            yes3 = abs(int(forecast_moving_average(temp3)))

            y['forecast_marketing'] = yes1
            y['forecast_taft'] = yes2
            y['forecast_malabon'] = yes3

            temp1.append(yes1)
            temp2.append(yes2)
            temp3.append(yes3)

        forecastingMethod = "Moving Average"

    marketingProductInStock = product.get_product_count(product, Branch.objects.get(idBranch=1))
    taftProductInStock = product.get_product_count(product, Branch.objects.get(idBranch=5))
    malabonProductInStock = product.get_product_count(product, Branch.objects.get(idBranch=6))

    marketingActualNeed = marketingProductForecast - marketingProductInStock
    taftActualNeed = taftProductForecast - taftProductInStock
    malabonActualNeed = malabonProductForecast - malabonProductInStock

    for i in ingredients:
        i.totalneeded = 0

    for i in ingredients:
        i.qtyneededmarketing = i.qtyneeded * marketingActualNeed
        i.qtyneededtaft = i.qtyneeded * taftActualNeed
        i.qtyneededmalabon = i.qtyneeded * malabonActualNeed
        i.totalneeded += i.qtyneededmarketing + i.qtyneededtaft + i.qtyneededmalabon

    products = Product.objects.all().order_by('name')

    context = {
        "marketingProductForecast": marketingProductForecast,
        "taftProductForecast": taftProductForecast,
        "malabonProductForecast": malabonProductForecast,
        "totalForecast": marketingProductForecast + taftProductForecast + malabonProductForecast,
        "productSales": product_inventory_sales,
        "products": products,
        "productID": productID,
        "productName": productName,
        "product": product,
        "method": method,
        "ingredients": ingredients,
        "marketingProductInStock": marketingProductInStock,
        "taftProductInStock": taftProductInStock,
        "malabonProductInStock": malabonProductInStock,
        "marketingActualNeed": marketingActualNeed,
        "taftActualNeed": taftActualNeed,
        "malabonActualNeed": malabonActualNeed,
        "forecastingMethod": forecastingMethod,
        'forecast_next_three_months': forecast_next_three_months
    }

    return render(request, 'salikneta/forecasting_detail.html', context)


def forecasting(request, method):
    si = SalesInvoice.objects.earliest('invoiceDate')
    earliestDate = si.invoiceDate.date()
    today = date.today()

    dates = [dt for dt in rrule(MONTHLY, dtstart=earliestDate, until=today)]

    forecast = []

    products = Product.objects.all()
    for p in products:
        awit = inventory_sales_per_month(dates, p.pk)
        product_inventory_sales = []
        for row in awit:
            product_inventory_sales.append(row['report_data'][0])
        productMarketingSales = []
        productTaftSales = []
        productMalabonSales = []

        for row in product_inventory_sales:
            productMarketingSales.append(row['sales_marketing'])
            productTaftSales.append(row['sales_taft'])
            productMalabonSales.append(row['sales_malabon'])

        if method == "ar":
            marketingProductForecast = abs(int(forecast_autoregression(productMarketingSales)))
            taftProductForecast = abs(int(forecast_autoregression(productTaftSales)))
            malabonProductForecast = abs(int(forecast_autoregression(productMalabonSales)))
        elif method == "ma":
            marketingProductForecast = abs(int(forecast_moving_average(productMarketingSales)))
            taftProductForecast = abs(int(forecast_moving_average(productTaftSales)))
            malabonProductForecast = abs(int(forecast_moving_average(productMalabonSales)))

        total = marketingProductForecast + taftProductForecast + malabonProductForecast

        forecast.append({"id": p.idProduct,
                         "product": p.name,
                         "description": p.description,
                         "uom": p.unitOfMeasure,
                         "marketing_branch": marketingProductForecast,
                         "taft_branch": taftProductForecast,
                         "malabon_branch": malabonProductForecast,
                         "total": total})

    if method == "ar":
        forecastingMethod = "Autoregression"
    elif method == "ma":
        forecastingMethod = "Moving Average"

    context = {
        "forecast": forecast,
        "forecastingMethod": forecastingMethod,
        "method": method,
    }

    return render(request, 'salikneta/forecasting.html', context)


def forecast_autoregression(data):
    try:
        model = AR(data)
        model_fit = model.fit()
        # make prediction
        yhat = model_fit.predict(len(data), len(data))
    except:
        yhat = forecast_moving_average(data)

    """
        try:
            model = ARIMA(data, order=(1, 1, 1))
            model_fit = model.fit()
            # make prediction
            yhat = model_fit.predict(len(data), len(data), typ='levels')
        except:
            yhat = forecast_moving_average(data)

        return yhat
    """
    return yhat


def forecast_moving_average(data):
    dataFrame = {"data": data}
    df = pd.DataFrame(dataFrame)
    movingAverage = df.rolling(window=3).mean()

    if math.isnan(movingAverage["data"].iloc[-1]):
        forecast = df["data"].iloc[-1]
        print('awit')
    else:
        forecast = round(movingAverage["data"].iloc[-1])
    """
    try:
        model = ARMA(data, order=(0, 1))
        model_fit = model.fit(disp=False)
        # make prediction
        yhat = model_fit.predict(len(data), len(data))
    except:
        yhat = 0
    """
    return forecast