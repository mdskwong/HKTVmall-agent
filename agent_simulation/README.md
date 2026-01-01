# Simulation subtask planner for agent

## 1. LLM first create empty brower
```
driver = create_driver()
```
## 2. goto HKTV Mall
```
url = "https://www.hktvmall.com/hktv/en/"
goto_url(url)
```

## 3. Search products with given text

search_products(text= 'protein')

## 4. Scrap products

```
product_data = scrap_products()
```
## 5. Choose a item 

This step should allow LLM to read the scrap data and return the selected product_code based on name/price/packing or even user preference

Below shows a hard-coded product to add.
```
select_product_id = product_data[0]['product_code']
print(product_data[0])
```

Product_data.json

    {"product_code": "H0888001_S_10159916", "product_name": "VITAL PROTEINS - 膠原蛋白多肽","product_price": "$ 301.00", "packing_spec": "567克"}...



## 6.  add the selected product to cart

Pass selected product id to tools
```
add_item_to_cart(select_product_id)
```

## 7. Repeat steps: 2 - 5 with different search text to add multiple items 

## 8. Go to check out page

```
click_btn(driver, btn_class_name= "btn-cart")
```

# Add / Update / Delete tools

Add/Update tools

    python oscopilot/tool_repository/manager/tool_manager.py --add --tool_name goto_url --tool_path agent_simulation/tools_to_add/goto_url.py
    python oscopilot/tool_repository/manager/tool_manager.py --add --tool_name search_products --tool_path agent_simulation/tools_to_add/search_products.py
    python oscopilot/tool_repository/manager/tool_manager.py --add --tool_name scrap_products --tool_path agent_simulation/tools_to_add/scrap_products.py
    python oscopilot/tool_repository/manager/tool_manager.py --add --tool_name pick_one_product --tool_path agent_simulation/tools_to_add/pick_one_product.py
    python oscopilot/tool_repository/manager/tool_manager.py --add --tool_name add_item_to_cart --tool_path agent_simulation/tools_to_add/add_item_to_cart.py

Delete tools

    python oscopilot/tool_repository/manager/tool_manager.py --delete --tool_name goto_url
    python oscopilot/tool_repository/manager/tool_manager.py --delete --tool_name search_products
    python oscopilot/tool_repository/manager/tool_manager.py --delete --tool_name scrap_products
    python oscopilot/tool_repository/manager/tool_manager.py --delete --tool_name pick_one_product
    python oscopilot/tool_repository/manager/tool_manager.py --delete --tool_name add_item_to_cart

