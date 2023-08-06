# connector_db_tools


[![Github License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Updates](https://pyup.io/repos/github/woctezuma/google-colab-transfer/shield.svg)](pyup)
[![Python 3](https://pyup.io/repos/github/woctezuma/google-colab-transfer/python-3-shield.svg)](pyup)
[![Code coverage](https://codecov.io/gh/woctezuma/google-colab-transfer/branch/master/graph/badge.svg)](codecov)




connector_db_tools is a Python library that implements for connection databases
## Installation

The code is packaged for PyPI, so that the installation consists in running:
```sh
pip install spark-datax-schema-tools 
```


## Usage

wrapper take connection database using pandas and modin

```sh

example1: (generate dummy_data)
================================
import ray
import os
from connector_db_tools import Core

ray.shutdown()
ray.init(local_mode=True)

""""config.json
 {"ORACLE":{
      "oracle":{
         "host":"XXXXXX",
         "port":1521,
         "db":"XXXXXX",
         "username":"XXXXX",
         "password":"XXXXX",
         "driver":"{Microsoft ODBC for Oracle}"
      }
 }
""""

path = os.getcwd()
path_file_config = os.path.join(path, "config.json")

df = Core.database_query(file_config=path_file_config, 
                         server="oracle", 
                         database="oracle", 
                         query=query, 
                         is_sql_direct=False)
       
df.head(10) 
                          
```


## License

[Apache License 2.0](https://www.dropbox.com/s/8t6xtgk06o3ij61/LICENSE?dl=0).


## New features v1.0

 
## BugFix
- choco install visualcpp-build-tools



## Reference

 - Jonathan Quiza [github](https://github.com/jonaqp).
 - Jonathan Quiza [RumiMLSpark](http://rumi-ml.herokuapp.com/).
 - Jonathan Quiza [linkedin](https://www.linkedin.com/in/jonaqp/).
