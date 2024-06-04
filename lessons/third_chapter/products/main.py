from fastapi import FastAPI
from products_db.products_db import sample_products


app = FastAPI()


@app.get('/product/{product_id}')
async def get_product(product_id: int):
    for product in sample_products:
        if product['product_id'] == product_id:
            return product
    else:
        return {'message': f'Product with product_id {product_id} not found'}


@app.get('/products/search')
async def get_searched_product(keyword: str, category: str = None, limit: int = 10):
    result = []

    for product_item in sample_products:
        if (keyword.lower() in product_item["name"].lower()
                and (category is None or category.lower() == product_item["category"].lower())):
            if limit > 0:
                limit -= 1
                result.append(product_item)
            else:
                break

    return result
