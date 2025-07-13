import os
import requests
import zipfile
import io
import polars as pl

def download_ff5_monthly(save_path: str):
    url = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_CSV.zip"

    print("Downloading Fama-French 5 Factors (2x3)...")
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download data. Status code: {response.status_code}")

    with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
        filename = zf.namelist()[0]
        with zf.open(filename) as file:
            lines = file.read().decode("latin1").splitlines()

    header_idx = 3  # 上から4行目がカラム名
    data_start_idx = header_idx + 1
    data_end_idx = next(i for i, line in enumerate(lines) if "Annual Factors" in line) - 1

    raw_columns = lines[header_idx].strip().split(",")
    columns = ["Date"] + [col.strip() for col in raw_columns[1:]]

    records = []
    for line in lines[data_start_idx:data_end_idx]:
        if line.strip() == "":
            continue
        row = [x.strip() for x in line.split(",")]
        records.append(row)

    df = pl.DataFrame(records, schema=columns, orient="row")

    # Date列の変換
    df = df.with_columns(
        pl.col("Date").str.to_datetime(format="%Y%m")
    )

    # 数値列の変換（％ → 小数）
    df = df.with_columns([
        pl.col(col).cast(pl.Float64) / 100.0 for col in columns[1:]
    ])

    # 保存（dataディレクトリは既に存在する想定）
    df.write_csv(save_path)
    print(f"Saved to {save_path}")