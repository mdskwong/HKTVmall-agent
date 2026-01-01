def add_all_items_to_cart(pick_all_products_return_val):
    """
    Add all the selected products to cart.

    Args:
        pick_all_products_return_val (dict): The return value of pick_all_products, containing the product codes.

    Returns:
        str: A message indicating whether the products were successfully added to the cart.
    """
    product_codes = pick_all_products_return_val['product_codes']
    try:
        from selenium_utils.reconnect_driver import reconnect_driver

        # Reconnect to current browser
        driver = reconnect_driver()
        messages = []
        for product_code in product_codes:
            url = f"https://www.hktvmall.com/hktv/zh/cart/add?productCodePost={product_code}&qty=1"
            driver.get(url)
            print(f"[{__name__}]Successfully clicked Add to Cart for product code: {product_code}")
            messages.append(f"Product {product_code} added to cart successfully.")
        return '\n'.join(messages)
    except Exception as e:
        print(f"Error adding item to cart: {e}")
        return f"Failed to add products to cart."       
