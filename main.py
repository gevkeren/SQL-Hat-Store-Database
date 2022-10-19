
import sys


from DTO import Hats
from DTO import Suppliers
from Repository import Repository

repo = Repository(sys.argv[4])
repo.create_tables()
cursor = repo.conn.cursor()
#config = open('config.txt')
#orders_config = open('orders.txt')

# config file
with open(sys.argv[1]) as file:

    counter = 0
    # 0 - num of lines for each
    # 1 <= counter <= hats - hats
    # hats < counter <= suppliers - suppliers

    hats = 0
    suppliers = 0

    for line in file:
        array = []
        array = line.split(",")
        if counter == 0:
            hats = int(array[0])
            suppliers = int(array[1])

        elif 1 <= counter <= hats:
            quantity = array[3]
            quantity = quantity.replace("\n", "")
            int_quantity = int(quantity)
            hat = Hats(int(array[0]), array[1], int(array[2]), int_quantity)
            repo.hats.insert(hat)

        elif hats < counter <= hats + suppliers:
            sup_id = int(array[0])
            sup_name = array[1]
            sup_name = sup_name.replace("\n","")
            sup = Suppliers(sup_id, sup_name)
            repo.suppliers.insert(sup)

        counter= counter + 1

# orders file
with open(sys.argv[2]) as file:
    order_counter = 1
    for line in file:
        array = []
        array = line.split(",")
        location = array[0]
        topping = array[1]
        topping = topping.replace("\n", "")
        repo.deliver(location, topping, order_counter)
        order_counter = order_counter + 1
        if order_counter == 2:
            fo = open(sys.argv[3], 'a+')
            fo.truncate(0)
        else:
            fo = open(sys.argv[3], 'a+')
        with fo as output:
            hat_id = repo.hats.get_lowest_id_by_topping(topping)
            supplier_id = repo.hats.find_supplier_by_id(hat_id)
            supplier_name = repo.suppliers.find_name_by_id(supplier_id)
            supplier_name = supplier_name.replace("\n", "")
            myLine = ""
            myLine = str(topping) + ',' + str(supplier_name) + ',' + str(location)
            output.write(myLine + '\n')