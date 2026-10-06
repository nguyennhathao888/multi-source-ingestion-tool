import requests
from pydantic import ValidationError
from models import product
from retry_logic import make_session
import logging
import pandas as pd
import time
import os


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def fetch_products(limit:int=30):
    url = f"https://dummyjson.com/products?limit={limit}"
    session=make_session()
    res = session.get(url)
    res.raise_for_status()
    return res.json()['products']

def main():
    raw_products=fetch_products(limit=100)
    valid,invalid=[],[]
    for item in raw_products:
        try:
            p=product(**item)
            valid.append(p)
        except ValidationError as e:
            invalid.append((item.get("id"),e))
            logging.warning(f"Product id={item.get("id")} invalid: {e}")

    logging.info(f'parsed {len(valid)} valid and {len(invalid)} invalid products')
    for pid,err in invalid:
        logging.error(f"Product id={pid}")
        logging.error(err)
    data=[p.model_dump() for p in valid]
    df=pd.DataFrame(data)
    df.to_csv("products.csv",index=False)
    df.to_json("products.json",orient="records")
    df.to_parquet("products.parquet",engine="pyarrow")
    for file in ["products.csv","products.json","products.parquet"]:
        size_kb=os.path.getsize(file)/1024
        print(f"{file}: {size_kb:.2f} kb")

if __name__ =="__main__":
    main()
    print(fetch_products())


    