# script/main.py

import sys
from pathlib import Path

# プロジェクトのルートディレクトリを取得
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent

# src をモジュールパスに追加
sys.path.append(str(project_root / "src"))

from download_ff5 import download_ff5_monthly

if __name__ == "__main__":
    save_path = project_root / "data" / "FamaFrench5Factors_monthly.csv"
    download_ff5_monthly(str(save_path))  # polarsはstr型が必要
    print("Download and processing complete.")