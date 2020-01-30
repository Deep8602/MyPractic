import random

import requests
import json


class MyRequests:
    get_time_url = "http://s-kv-center-v20:44330/api/FreeTime?FilialId=1998&TicketToken=ODNjMjVhYTgyMmRlN2NmYjNjNDViNjIxNWZlYjMzYWE6eyJpZCI6MzV9"
    get_lagers_url = "http://s-kv-center-v20:44330/api/Lager?filialId=2382&ticketToken=56"
    create_lagers_in_basket_url = "http://s-kv-center-v20:44330/api/Lager"
    create_order_url = "http://s-kv-center-v20:44330/api/Orders"

    request_data = {
        "filial_id": 2382,
        "tiket_token": "ODNjMjVhYTgyMmRlN2NmYjNjNDViNjIxNWZlYjMzYWE6eyJpZCI6MzV9",
        "user_id": "56"
    }

    def get_free_time(self):
        response = requests.get(self.get_time_url, self.request_data)
        free_time_dict = response.json()
        free_time_list = []
        for free_time in free_time_dict:
            free_time_list.append(free_time["begin"])
        # print(free_time_list)
        return free_time_list

    def get_lagers_id(self):
        get_lager_request = {
            'filial_id': self.request_data['filial_id'],
            'user_id': self.request_data['user_id']
        }

        my_response = requests.get(self.get_lagers_url, get_lager_request)
        lager_dict = my_response.json()
        lager_id_list = []
        for lager in lager_dict['lagers']:
            if lager['remnant'] > 1:
                for items in lager['items']:
                    if items['count'] > 1:
                        lager_id = (items['id'])
                        lager_id_list.append(lager_id)
        # print(lager_id_list)
        return lager_id_list

    def create_lagers_in_basket(self, howe_mach_lagers):
        lager_id_list = self.get_lagers_id()
        lagers = lager_id_list[0:howe_mach_lagers + 1]

        headers = {
            "accept": "text/plain",
            "Content-Type": "application/json-patch+json"
        }

        for lager_id in lagers:
            lager_dict = {
                "ticketToken": self.request_data['user_id'],
                "filialId": self.request_data['filial_id'],
                "lager": {
                    "id": lager_id,
                    "count": 1
                }
            }
            # print(lager_id)
            requests_lager = requests.post(self.create_lagers_in_basket_url, json.dumps(lager_dict), headers=headers)
            # print(requests_lager.json())

    def create_order(self, howe_mach_lagers=0, howe_mach_order=0):

        for i in range(howe_mach_order):
            self.create_lagers_in_basket(howe_mach_lagers)
            free_time = random.choice(self.get_free_time())

            headers = {
                "accept": "text/plain",
                "Content-Type": "application/json-patch+json"
            }

            order_field = {
                'customerPhone': "+380777777777",
                'ticketToken': self.request_data['user_id'],
                'filialId': self.request_data['filial_id'],
                'readyDate': free_time
            }

            response = requests.post(self.create_order_url, json.dumps(order_field), headers=headers)
            print(response.json())
            print(response)

    #
    # """________________________________________My_practice_____________________________________"""

    status_dict = {
        "0995336d-8483-46c7-a012-437df3cd40ab": "Нове",
        "2f916855-834b-47c0-bd26-c615a411dfdf": "Підтверджене",
        "acd8914b-11c6-43fb-9cbd-deddb9a220aa": "Скасоване",
        "2f257b3f-89cc-4e7e-8aec-cef9700034b6": "Прострочене",
        "f9e38007-b27c-409f-8ff7-b2c7c39eb294": "Готове",
        "15225f94-ad0e-4a8a-a04d-ac83ac41d23d": "Утилізований",
        "07baae3c-cff6-424a-a455-470909e70fe2": "Розукомплектований",
        "f1a67b87-fbd2-4f91-97eb-1764c42dc39e": "Видане"
    }

    headers = {
        "accept": "text/plain",
        "Content-Type": "application/json-patch+json"
    }

    def get_all_order_with_status(self, date):

        """Return all orders and they statuses for chosen date (date in format - yyyy-mm-dd)"""

        created_orders_url = "http://s-kv-center-v20:44330/api/Orders/Sync?FilialId=2382&Date=" + date


        orders_responds = requests.get(created_orders_url, self.request_data)
        order_list = orders_responds.json()
        info_of_orders = []
        statuses = []
        for data in order_list:
            info_of_orders.append(data['orderNumber'])
            info_of_orders.append(data['statusId'])
            #Take order number and status id
        for status in info_of_orders:
            if type(status) == int:
                statuses.append(status) #Take order number in our list
            for status_id in self.status_dict:
                if status == status_id:
                    statuses.append(self.status_dict.get(status_id)) #Take name of status in our list from status_dict
        for i in range(0, len(statuses), 2):
            print('Номер ордеру та його статус:' + str(statuses[i:i + 2]) + ' дата початку синхронізації ' + date)






    def go_to_next_status(self, order_num, date):

        created_orders_url = "http://s-kv-center-v20:44330/api/Orders/Sync?FilialId=2382&Date=" + date

        update_order_url = "http://s-kv-center-v20:44330/api/Orders/Sync"


        orders_responds = requests.get(created_orders_url, self.request_data)
        order_list = orders_responds.json()
        info_of_orders = []
        orders = []
        order_id = []
        next_status_id = []

        for data in order_list:
            info_of_orders.append(data['orderNumber'])
            info_of_orders.append(data['statusId'])
            info_of_orders.append(data['orderId'])
            for i in range(0, len(info_of_orders), 3):
                orders.append(info_of_orders[i:i + 3])
        for j in range(len(orders)):
            if orders[j][0] == order_num:
                order_id.append(orders[j][2])
                order_id.append(orders[j][1])

        if order_id[1] == '0995336d-8483-46c7-a012-437df3cd40ab':
            next_status_id.insert(1,('2f916855-834b-47c0-bd26-c615a411dfdf'))
        elif order_id[1] == '2f916855-834b-47c0-bd26-c615a411dfdf':
            next_status_id.insert(1,('f9e38007-b27c-409f-8ff7-b2c7c39eb294'))
        elif order_id[1] == 'f9e38007-b27c-409f-8ff7-b2c7c39eb294':
            next_status_id.insert(1,('f1a67b87-fbd2-4f91-97eb-1764c42dc39e'))
        else:
            print('заказ видано')
            return True

        next_status = {
             "orderId": str(order_id[0]),
             "statusId": str(next_status_id[0])
                            }

        next_status_responds = requests.put(update_order_url, json.dumps(next_status), headers=self.headers)
        print(next_status_responds)
        print("заказ № " + str(order_num) + " переведено в наступний статус")
        print('some massage')

