#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
from ConfigParser import ConfigParser
from collections import OrderedDict
 

if __name__ == "__main__":
    cfg = ConfigParser(dict_type=OrderedDict)
    cfg.optionxform=str
    if len(sys.argv) > 1:
        f = open(sys.argv[1])
    else:
        f = sys.stdin
    cfg.readfp(f)
    f.close()
 
    config = OrderedDict()
    be_nested = ["treatments", "samples"]
    for section in cfg.sections():
        for name, value in cfg.items(section):
            if section in be_nested:
                if section not in config: config[section] = OrderedDict()
                config[section][name] = [x.strip().strip('"').strip("'") for x in value.split(',') if x]
            else:
                key_name = name.lower()
                config[key_name] = [x.strip().strip('"').strip("'") for x in value.split(',') if x]
                if len(config[key_name]) == 1: config[key_name] = config[key_name][0]
                elif len(config[key_name]) == 0: config[key_name] = ''
    print json.dumps(config,indent=4)
