from multiprocessing import Process, Manager


class WarehouseManager:
    def __init__(self):
        self.data = Manager().dict()

    def process_request(self, request):
        name = request[0]
        command = request[1]
        modi = request[2]
        if command == 'receipt':
            if name in self.data.keys():
                self.data[name] += modi
            else:
                self.data[name] = modi
        elif command == 'shipment':
            if name in self.data.keys() and self.data[name] > 0:
                self.data[name] -= modi

    def run(self, requests):
        list = []
        for request in requests:
            pr = Process(target=self.process_request, args=(request, ))
            list.append(pr)
            pr.start()
        for pr in list:
            pr.join()


if __name__ == '__main__':
    # Создаем менеджера склада
    manager = WarehouseManager()

    # Множество запросов на изменение данных о складских запасах
    requests = [
        ("product1", "receipt", 100),
        ("product2", "receipt", 150),
        ("product1", "shipment", 30),
        ("product3", "receipt", 200),
        ("product2", "shipment", 50)
    ]

    # Запускаем обработку запросов
    manager.run(requests)

    # Выводим обновленные данные о складских запасах
    print(manager.data)





