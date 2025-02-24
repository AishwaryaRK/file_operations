import collections
import csv
import heapq
from _datetime import datetime
import logging


class SalesAnalytics:
    def __init__(self, filename: str):
        self.revenue_sales = collections.defaultdict(lambda: collections.defaultdict(float))
        self.product_quantity_map = collections.defaultdict(int)
        self.transaction = collections.defaultdict(lambda: collections.defaultdict(list))
        self.__aggregate_data(filename)

    def __aggregate_data(self, filename: str):
        try:
            with open(filename, "r") as fd:
                # fd.readline()
                # for line in fd:
                #     data = line.split(",")

                reader = csv.DictReader(fd)
                next(reader)
                for data in reader:
                    timestamp = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S")
                    month = timestamp.month
                    product_id = data["product_id"]
                    category = data["category"]
                    price = float(data["price"])
                    quantity = float(data["quantity"])
                    location = data["location"]
                    payment_method = data["payment_method"]
                    shipping_cost = float(data["shipping_cost"])

                    self.revenue_sales[month][category] += price * quantity

                    self.product_quantity_map[product_id] += quantity

                    if payment_method in self.transaction[location]:
                        self.transaction[location][payment_method][0] += (price * quantity + shipping_cost)
                        self.transaction[location][payment_method][1] += 1
                    else:
                        self.transaction[location][payment_method] = [(price * quantity + shipping_cost), 1]


        except FileNotFoundError as e:
            logging.error("error: file not found %s", e)
        except ValueError as e:
            logging.error("error: invalid file content %s", e)
        except Exception as e:
            logging.error("error: %s", e)

    def monthly_revenue_sales(self):
        return self.revenue_sales

    def top_k_products_sold(self, n: int):
        max_heap = []
        for product_id, quantity in self.product_quantity_map.items():
            heapq.heappush(max_heap, (-quantity, product_id))

        result = []
        for i in range(n):
            quantity, product_id = heapq.heappop(max_heap)
            result.append((product_id, -quantity))
        return result

    def avg_transaction_by_payment_per_location(self):
        for location, payment_transactions in self.transaction.items():
            for payment, total_transaction in payment_transactions.items():
                total_transaction_value = total_transaction[0]
                count = total_transaction[1]
                print(location, payment, total_transaction_value / count)


sale_analytics = SalesAnalytics("sales_data.csv")
# revenue_sales = sale_analytics.monthly_revenue_sales()
# for month, categories in revenue_sales.items():
#     for category, sales in categories.items():
#         print(month, category, sales)
#
# print(sale_analytics.top_k_products_sold(5))

sale_analytics.avg_transaction_by_payment_per_location()
