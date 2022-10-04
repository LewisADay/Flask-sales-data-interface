
from csv import DictReader
from itertools import product
import pandas as pd

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

        self.items_sold = 0
        self.num_customers = 0
        self.total_discount = 0
        self.avg_discount_rate = 0
        self.avg_total = 0
        self.total_commission = 0
        self.avg_commission = 0
        self.total_commission_per_promotion = 0

        self._query()

    def _parse_orders_csv(self):

        # Storage variables
        order_ids = []
        customer_ids = []
        vendors = []

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
                    order_ids.append(int(order['id']))
                    customer_ids.append(int(order['customer_id']))
                    vendors.append(int(order['vendor_id']))
                
                # If date greater than the date we're after
                # finish early, we've passed it
                # (exploiting the fact orders.csv is date ordered ascending)
                if date_greater_than_date(date, self.date):
                    break

        return pd.DataFrame(
            list(zip(order_ids, customer_ids, vendors)),
            columns=['order_id', 'customer_id', 'vendor_id'],
            )

    def _parse_order_lines_csv(self, base_order_ids):

        # Open order_lines.csv
        with open('order_lines.csv', 'r') as file:
            rows = [0]
            row = 1
            dict_reader = DictReader(file)
            for entry in dict_reader:
                if int(entry['order_id']) in base_order_ids:
                    rows.append(row)
                row += 1

        # Read order_lines.csv
        return pd.read_csv(
            'order_lines.csv',
            usecols=[
                'order_id',
                'product_id',
                'quantity',
                'full_price_amount',
                'discounted_amount',
                'total_amount'
                ],
            skiprows=lambda x: x not in rows,
            header=0,
            dtype={
                'order_id': int,
                'product_id': int,
                'quantity': int,
                'full_price_amount': float,
                'discounted_amount': float,
                'total_amount': float
                }
            )

    def _parse_commissions_csv(self):
        # Return dict
        commissions = {}

        # Open commissions.csv
        with open('commissions.csv', 'r') as file:

            # Read each line as a dict
            dict_reader = DictReader(file)
            for entry in dict_reader:

                # If this entry is for the date we're after, get its info
                if entry['date'] == self.date:
                    commissions[int(entry['vendor_id'])] = float(entry['rate'])

                # If date greater than the date we're after
                # finish early, we've passed it
                # (exploiting the fact commissions.csv is date ordered ascending)
                if date_greater_than_date(entry['date'], self.date):
                    break

            return commissions

    def _parse_product_promotions_csv(self):
        # Return dict
        promotions = {}

        # Open product_promotions.csv
        with open('product_promotions.csv', 'r') as file:

            # Read each line as a dict
            dict_reader = DictReader(file)
            for entry in dict_reader:

                # If this entry is for the date we're after, get its info
                if entry['date'] == self.date:
                    promotions[int(entry['product_id'])] = int(entry['promotion_id'])

                # If date greater than the date we're after
                # finish early, we've passed it
                # (exploiting the fact commissions.csv is date ordered ascending)
                if date_greater_than_date(entry['date'], self.date):
                    break

            return promotions

    def _parse_promotions_csv(self):
        # Return dict
        promotions = {}

        # Open promotions.csv
        with open('promotions.csv', 'r') as file:

            # Read each line as a dict
            dict_reader = DictReader(file)
            for entry in dict_reader:
                promotions[int(entry['id'])] = str(entry['description'])

        return promotions

    def _get_data(self):
        self.order_csv_df = self._parse_orders_csv()
        self.order_lines_csv_df = self._parse_order_lines_csv(list(self.order_csv_df['order_id'].values))
        self.commissions_dict = self._parse_commissions_csv()
        self.product_promotions_dict = self._parse_product_promotions_csv()
        self.promotions_dict = self._parse_promotions_csv()

    def _calc_vals(self):

        # Get required values

        # Simple calculations
        self.items_sold = sum(self.order_lines_csv_df['quantity'])
        self.num_customers = len(set(self.order_csv_df['customer_id']))
        self.total_discount = sum(self.order_lines_csv_df['full_price_amount'] - self.order_lines_csv_df['discounted_amount'])
        total = sum(self.order_lines_csv_df['total_amount'])
        self.avg_discount_rate = self.total_discount / total
        self.avg_total = total / self.items_sold

        # Commission is a bit more complicated

        # Setup dict for commission per promotion
        self.total_commission_per_promotion = {}

        # Init to 0 for all promotions
        for promotion in self.promotions_dict.values():
            self.total_commission_per_promotion[promotion] = 0

        for vendor, rate in self.commissions_dict.items():
            vendor_mask = (self.order_csv_df['vendor_id'] == vendor)
            vendors_orders = self.order_csv_df['order_id'][vendor_mask]
            for order in vendors_orders:
                order_mask = (self.order_lines_csv_df['order_id'] == order)
                # Per product
                for product_id in self.order_lines_csv_df['product_id'][order_mask]:
                    product_mask = order_mask & (self.order_lines_csv_df['product_id'] == product_id)
                    commission = float(self.order_lines_csv_df['total_amount'][product_mask]) * rate
                    if product_id in self.promotions_dict:
                        promotion = self.promotions_dict[product_id]
                    else:
                        promotion = 0
                    if promotion in self.total_commission_per_promotion:
                        self.total_commission_per_promotion[promotion] += commission
                    else:
                        self.total_commission_per_promotion[promotion] = commission

        self.total_commission = sum(self.total_commission_per_promotion.values())
        self.avg_commission = self.total_commission / self.items_sold


    def _query(self):
        # Get data for this date in pandas dataframes
        self._get_data()

        # Process data
        self._calc_vals()

        # Format data
        self.items_sold = f"{self.items_sold:d}"
        self.num_customers = f"{self.num_customers:d}"
        self.total_discount = f"{self.total_discount:.2f}"
        self.avg_discount_rate = f"{self.avg_discount_rate:.2f}"
        self.avg_total = f"{self.avg_total:.2f}"
        self.total_commission = f"{self.total_commission:.2f}"
        self.avg_commission = f"{self.avg_commission:.2f}"

        self.total_commission_per_promotion = {promotion: f"{amount:.2f}" for promotion, amount in self.total_commission_per_promotion.items() if promotion != 0}

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
    tmp = "2019-08-01"
    query = Query(tmp)
