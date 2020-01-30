from Request import MyRequests

howe_mach_lagers = int(input("Сколько товаров? "))
howe_mach_orders = int(input("Сколько заказов? "))

MyRequests().create_order(howe_mach_lagers, howe_mach_orders)