"""Optional pandas version. Install pandas first if needed."""
try:
    import pandas as pd
except ImportError:
    print("未安装 pandas。可运行：python -m pip install pandas")
else:
    df = pd.read_csv("input/learning_records.csv")
    print(df)
    print(df.groupby("done")["minutes"].mean())
