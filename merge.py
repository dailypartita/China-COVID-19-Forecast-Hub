import os
import pandas as pd
from pathlib import Path
from datetime import datetime

model_dir_list = ['XMU_CTModelling-FNN', 'XMU_CTModelling-LSTM', 'XMU_CTModelling-GRU', 'XMU_CTModelling-TCN', 'XMU_CTModelling-XGBoost']
for model_dir in model_dir_list:
    csv_dir = f'model-output/{model_dir}'
    csv_path_list = list(Path(csv_dir).glob('*.csv'))
    csv_data_list = []
    for csv_path in csv_path_list:
        csv_data_list.append(pd.read_csv(csv_path))
    concat_df = pd.concat(csv_data_list)
    concat_df.to_csv(csv_path_list[-1], index=False)