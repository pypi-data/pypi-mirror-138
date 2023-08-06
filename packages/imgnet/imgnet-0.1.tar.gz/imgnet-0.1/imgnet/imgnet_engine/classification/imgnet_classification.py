from imgnet.imgnet_utils.common_utils import read_yaml
import os
import yaml
import logging
import pandas as pd
from imgnet.imgnet_tools.all_encryption import decodeFile

def trainEngine(request_data,params_path, config_path):
    print("ok")
    config = read_yaml(config_path)

    paths = config["data_path"]
    print(paths)
    IMGNET_ENGINE = paths["IMGNET_ENGINE"]
    ARTIFACTS = paths["ARTIFACTS"]
    SECTION = paths["SECTION"]

    save_data = os.path.join(IMGNET_ENGINE, ARTIFACTS, SECTION)

    try:
        if request_data:
            print(request_data)
            # if 'model_obj' in request_data:
            #     MODEL_NAME = request_data['model_obj']
            #
            # if 'batch_size' in request_data:
            #     BATCH_SIZE = int(request_data['batch_size'])
            #
            # if 'augmentation' in request_data:
            #     AUGMENTATION = request_data['augmentation']
            #
            # if 'optimizer' in request_data:
            #     OPTIMIZER = request_data['optimizer']
            #
            # if 'no_of_epochs' in request_data:
            #     EPOCHS = int(request_data['no_of_epochs'])
            #
            # if 'loss_func' in request_data:
            #     LOSS_FUNC = request_data['loss_func']
            #
            # fileName = request_data['files'][0]['name']
            # # print(f"name of file: {fileName}")
            # codedvalue = request_data['files'][0]['base64']
            # codedvalue = codedvalue.split(',')
            # # os_operation.remove_folder(os.path.join(save_data,'data'))
            #
            # codedvalue = codedvalue[-1]
            # decodeFile(codedvalue, os.path.join(save_data, fileName))
            #
            # config['AUGMENTATION'] = AUGMENTATION
            # config['BATCH_SIZE'] = BATCH_SIZE
            # config['MODEL_NAME'] = MODEL_NAME
            # config['OPTIMIZER'] = OPTIMIZER
            # config['EPOCHS'] = EPOCHS
            # config['LOSS_FUNC'] = LOSS_FUNC
            # print(config)
            #
            # with open('params/classification.yaml', 'w') as f:
            #     print("Putting file inside classification,yaml")
            #     yaml.dump(config, f)

            return "Model Successfully trained"

    except Exception as e:
        return f"Somthing went wrong! {e}"

