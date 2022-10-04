
from csv import DictReader
from typing import Dict

def is_valid_date(input):
    """A really bad way to check the validity of thise date format
    
    //

    """
    try:
        y, m, d = get_date_from_str(input)
    except ValueError:
        return False
    if d <= 0 or d > 31:
        return False
    if m <= 0 or m > 12:
        return False
    if y <= 0 or y > 9999:
        return False
    return True


def get_date_from_str(date_str):
    """Assuming date_str is of the form DD-MM-YYYY, get those ints"""
    year, month, day = date_str.split('-')
    return int(year), int(month), int(day)

def date_greater_than_date(date1, date2):
    """Return date1 > date2"""

    # If equal check
    if date1 == date2:
        return False

    # Get actual date information
    y1, m1, d1 = get_date_from_str(date1)
    y2, m2, d2 = get_date_from_str(date2)

    # First test the year
    if y1 > y2:
        return True
    if y1 < y2:
        return False

    # Only the case y1 == y2 remains
    # Now test the month
    if m1 > m2:
        return True
    if m1 < m2:
        return False
    
    # Only the case m1 == m2 remains
    # Finally test the day
    return d1 > d2


class Query:
    def __init__(self, date):
        self.date = date
        self.year, self.month, self.day = get_date_from_str(date)

        self.items_sold = None
        self.num_customers = None
        self.total_discount = None
        self.avg_discount = None
        self.avg_total = None
        self.total_commission = None
        self.avg_commission = None
        self.total_commission_per_promotion = None

        self._query()


    def _parse_orders_csv(self):

        # Storage for return variables
        order_ids = []
        unique_customers = set()
        vendors_orders = {}

        # Open orders.csv
        with open('orders.csv', 'r') as file:

            # Read each line as a dict
            dict_reader = DictReader(file)
            for order in dict_reader:

                # Get date+time information of order
                date = order['created_at']

                # Get date
                date, time = date.split(' ')

                # If this is the date we're after, get its info
                if date == self.date:
                    id = order['id']
                    order_ids.append(id)
                    unique_customers.add(order['customer_id'])
                    vendor = order['vendor_id']
                    if vendor in vendors_orders:
                        vendors_orders[vendor].append(id)
                    else:
                        vendors_orders[vendor] = [id]
                
                # If date greater than the date we're after
                # finish early, we've passed it
                # (exploiting the fact orders'csv is date ordered ascending)
                if date_greater_than_date(date, self.date):
                    break

        return order_ids, unique_customers, vendors_orders

    def _parse_order_lines_csv(self, order_ids):

        # Storage for return variables
        total_discount = 0
        num_items = 0
        avg_order_total = 0
        avg_discount_rate = 0

        # Temporary variables
        order_totals = {}

        # Open order_lines.csv
        with open('order_lines.csv', 'r') as file:

            # Read each line as a dict
            dict_reader = DictReader(file)
            for entry in dict_reader:
                order_id = entry['order_id']

                # Determine if order is from the correct date
                if order_id not in order_ids:
                    continue

                # If it is...

                # Calculate discount amount
                # Get price and discounted price
                full_price = float(entry['full_price_amount'])
                disc_price = float(entry['discounted_amount'])

                # Calculate total discount applied and add to total
                total_discount += full_price - disc_price

                # Add number of units sold to items count
                num_items += int(entry['quantity'])

                # Add to this orders total
                if order_id in order_totals:
                    order_totals[order_id] += float(entry['discount_rate'])
                else:
                    order_totals[order_id] = float(entry['discount_rate'])

        return total_discount, num_items, avg_order_total, avg_discount_rate


    def _get_data(self):
        order_ids, unique_customers, vendors_orders = self._parse_orders_csv()
        self.num_customers = len(unique_customers)
        self.total_discount, self.items_sold, self.avg_order_total, self.avg_discount_rate = self._parse_order_lines_csv(order_ids)


    def _query(self):
        # Get data for this date in one pandas dataframe
        self._get_data()
        # Process data

"""Output form

Items sold: {}
Unique customers: {}
Total amout of discount given: {}
Average discount rate applied to each item: {}
Average total per order: {}
Total commissions generated: {}
Average commission per order: {}
Total commissions earned per promotion: {}

"""

if __name__ == "__main__":
    tmp = "1984-08"
    print(is_valid_date(tmp))
