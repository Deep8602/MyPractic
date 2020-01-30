from Request import MyRequests
#
# requested_date = input("Введите дату синхронизации в формате yyyy-mm-dd :" )
#
# order_num = int(input("Введите номер заказа: "))
MyRequests().get_all_order_with_status('2019-09-10')
# MyRequests().go_to_next_status(order_num, requested_date)
