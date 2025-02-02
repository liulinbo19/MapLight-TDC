
from maplight import *
from tqdm import tqdm
import catboost as cb
from tdc.benchmark_group import admet_group

benchmark_config = {
    'caco2_wang': ('regression', False),
    'bioavailability_ma': ('binary', False),
    'lipophilicity_astrazeneca': ('regression', False),
    'solubility_aqsoldb': ('regression', False),
    'hia_hou': ('binary', False),
    'pgp_broccatelli': ('binary', False),
    'bbb_martins': ('binary', False),
    'ppbr_az': ('regression', False),
    'vdss_lombardo': ('regression', True),
    'cyp2c9_veith': ('binary', False),
    'cyp2d6_veith': ('binary', False),
    'cyp3a4_veith': ('binary', False),
    'cyp2c9_substrate_carbonmangels': ('binary', False),
    'cyp2d6_substrate_carbonmangels': ('binary', False),
    'cyp3a4_substrate_carbonmangels': ('binary', False),
    'half_life_obach': ('regression', True),
    'clearance_hepatocyte_az': ('regression', True),
    'clearance_microsome_az': ('regression', True),
    'ld50_zhu': ('regression', False),
    'herg': ('binary', False),
    'ames': ('binary', False),
    'dili': ('binary', False)
}

group = admet_group(path='data/')

# change comment to run all benchmarks
# for admet_benchmark in benchmark_config.keys():
 
    
    results = 202
    print('\\n\\n{}'.format(results))

    # 保存结果到文件
    with open('results.txt', 'w') as f:
        f.write(str(results))
