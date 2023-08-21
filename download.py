import pandas as pd
from pathlib import Path
import urllib.request
import time
from tqdm.auto import tqdm

BASE_URL = "https://mops.twse.com.tw/server-java/FileDownLoad?step=9&filePath=/home/html/nas/protect/t100/&fileName="

meta_data_path = "data/meta-data"
for meta_data in Path(meta_data_path).glob("*.csv"):
    Path("data", meta_data.stem).mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(meta_data, encoding="cp950")
    # Process column names
    col_names = df.columns.tolist()
    df.reset_index(inplace=True)
    df.drop("備註", axis=1, inplace=True)
    df.columns = col_names
    # Download files
    for _, row in tqdm(df.iterrows(), total=df.shape[0], desc=meta_data.stem):
        idx = row["公司代號"]
        name = row["公司名稱"]
        file_name = row["中文版永續報告書(修正後版本)"] if pd.notnull(row["中文版永續報告書(修正後版本)"]) else row["中文版永續報告書"]
        url = BASE_URL + file_name
        save_path = Path("data", meta_data.stem, f"{idx}_{name}.pdf")
        # Skip if the data is already downloaded
        if save_path.exists():
            continue
        urllib.request.urlretrieve(url, save_path)