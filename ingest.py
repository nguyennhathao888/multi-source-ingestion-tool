from read_yaml import load_soucre
from retry_logic import make_session
import logging
import pandas as pd
import click
import os

@click.command()
@click.option("--config",default="source.yaml",help="Yaml file location")
@click.option("--output",default="./data",help="Save folder")
def run(config,output):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    os.makedirs(output,exist_ok=True)
    sources=load_soucre()
    for s in sources:
        try:
            data=process_source(s)
            df=pd.DataFrame(data)
            out_path=os.path.join(output,f"{s['name']}.parquet")
            df.to_parquet(out_path,engine="pyarrow")
            logging.info(f"{s['name']}: fetched {len(data)} record to {out_path}")
        except Exception as e:
            logging.error(f"{s['name']} error when fetch - {e}")

def fetch_api(source: dict):
    session=make_session()
    logging.info(f"Fetching api {source['name']}")
    res=session.get(source['url'])
    res.raise_for_status()
    return res.json()[source['response_key']]

def fetch_csv(source: dict):
    df=pd.read_csv(source['url'])
    return df.to_dict(orient="records")

def process_source(source: dict):
    if source['type']=='api':
        return fetch_api(source)
    elif source['type']=='csv':
        return fetch_csv(source)
    else:
        raise ValueError(f"Not supporting {source['type']}")

def main():
    source = load_soucre()
    all_result={}
    for s in source:
        try:
            data = process_source(s)
            all_result[s['name']]=data
            logging.info(f"{s['name']}: take {len(data)} record")
        except Exception as e:
            logging.error(f"{s['name']} failed {e}")
    return all_result

if __name__ == "__main__":
    """logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    results = main()
    for name, data in results.items():
        print(f"{name}: {len(data)} record")
    """
    run()