# script/main.py

import sys
import os

# src ディレクトリをモジュール検索パスに追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from download_ff5 import download_ff5_monthly

if __name__ == "__main__":
    save_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "FamaFrench5Factors_monthly.csv"))
    download_ff5_monthly(save_path)
    print("Download and processing complete.")