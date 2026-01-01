import re
from selenium.webdriver.common.by import By

def extract_product_details(item):
    """Extract product details from a single product item."""
    product_code = extract_product_code(item)
    product_name = extract_text(item, By.CLASS_NAME, 'brand-product-name')
    product_price = extract_text(item, By.CLASS_NAME, 'price')
    packing_spec = extract_text(item, By.CLASS_NAME, 'packing-spec')

    if product_code:
        return {
            'product_code': product_code,
            'product_name': product_name,
            'product_price': product_price,
            'packing_spec': packing_spec
        }
    return None

def extract_product_code(item):
    """Extract the product code using regex from the outerHTML."""
    try:
        match = re.search(r'data-id="([^"]+)"', item.get_attribute('outerHTML'))
        return match.group(1) if match else None
    except Exception as e:
        return None

def extract_text(item, by, class_name):
    """Extract text from an element, handling exceptions gracefully."""
    try:
        return item.find_element(by, class_name).text.strip()
    except Exception as e:
        return None