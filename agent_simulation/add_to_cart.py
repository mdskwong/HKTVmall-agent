from selenium_utils.json_products_data import load_results_from_json
from tools_to_add import *

#4rd subtask: LLM to read the scrap data and return the selected product_code based on name/price/packing or even user preference
#{"product_code": "H0888001_S_10159916", "product_name": "VITAL PROTEINS - 膠原蛋白多肽", "product_price": "$ 301.00", "packing_spec": "567克"}
# product_data = load_results_from_json()
# select_product_id = product_data[0]['product_code']
# print(product_data[0])

select_product_id = 'H0888001_S_10132278A'

#5th subtask: add the selected product to cart
add_item_to_cart(select_product_id)
