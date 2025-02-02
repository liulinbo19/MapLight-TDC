code = """
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
for admet_benchmark in [list(benchmark_config.keys())[7]]:
    predictions_list = []
    for seed in tqdm([1, 2, 3, 4, 5]):
        benchmark = group.get(admet_benchmark)
        predictions = {}
        name = benchmark['name']
        train, test = benchmark['train_val'], benchmark['test']

        # --------------------------------------------- # 
        #  Train your model using train, valid, test    #
        #  Save test prediction in y_pred_test variable #
        X_train = get_fingerprints(train['Drug'])
        X_test = get_fingerprints(test['Drug'])

        task, log_scale = benchmark_config[name]
        params = {
                'random_strength': 2, 
                'random_seed': seed,
                'verbose': 0,
            }

        if task == 'regression':
            Y_scaler = scaler(log=log_scale)
            Y_scaler.fit(train['Y'].values)
            train['Y_scale'] = Y_scaler.transform(train['Y'].values)

            params['loss_function'] = 'MAE'            
            model = cb.CatBoostRegressor(**params)
            model.fit(X_train, train['Y_scale'].values)

            y_pred_test = Y_scaler.inverse_transform(model.predict(X_test)).reshape(-1)
        elif task == 'binary':
            params['loss_function'] = 'Logloss'
            model = cb.CatBoostClassifier(**params)
            model.fit(X_train, train['Y'].values)

            y_pred_test = model.predict_proba(X_test)[:, 1]
        # --------------------------------------------- #

        predictions[name] = y_pred_test
        predictions_list.append(predictions)
    
    results = group.evaluate_many(predictions_list)
    print('\\n\\n{}'.format(results))

    # 保存结果到文件
    with open('results.txt', 'w') as f:
        f.write(str(results))
"""
with open('run_script.py', 'w') as f:
    f.write(code)
