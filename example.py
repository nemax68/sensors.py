#!/usr/bin/env python3
"""
@author: Pavel Rojtberg (http://www.rojtberg.net)
@see: https://github.com/paroj/sensors.py
@copyright: The MIT License (MIT) <http://opensource.org/licenses/MIT>
"""

import sensors

src = {
    "in0": "ARM core voltage",
    "in1": "Board voltage",
    "in2": "IO Voltage",
    "in3": "FPGA core voltage",
    "in4": "DDR voltage",
}

value_min = {
    "in0": 1.35,
    "in1": 4.90,
    "in2": 3.25,
    "in3": 2.45,
    "in4": 1.45,
}

value_max = {
    "in0": 1.45,
    "in1": 5.10,
    "in2": 3.40,
    "in3": 2.60,
    "in4": 1.55,
}

def check_feature(chip, feature):
    sfs = list(sensors.SubFeatureIterator(chip, feature)) # get a list of all subfeatures

    label = sensors.get_label(chip, feature)

    skipname = len(feature.name)+1 # skip common prefix

    # vals is a list of value min and max
    vals = [sensors.get_value(chip, sf.number) for sf in sfs]

    if feature.type == sensors.feature.INTRUSION:
        # short path for INTRUSION to demonstrate type usage
        status = "alarm" if int(vals[0]) == 1 else "normal"
        print("\t"+label+"\t"+status)

    names = [sf.name[skipname:].decode("utf-8") for sf in sfs]
    data = list(zip(names, vals))

    str_data = ", ".join([e[0]+": "+str(e[1]) for e in data])

    if vals[2] > value_max[label]:
        print("\tCheck "+src[label]+"\tFAILED! "+str(vals[2])+" > "+str(value_max[label])+")")
        return False

    if vals[1] < value_min[label]:
        print("\tCheck "+src[label]+"\tFAILED! "+str(vals[1])+" < "+str(value_min[label])+")")
        return False

    print("\tCheck "+src[label]+"\t"+"\t("+str(vals[0])+") ....OK")
    return True

if __name__ == "__main__":
    sensors.init() # optionally takes config file

    print("Checking board voltage:")

    print("libsensors version: "+sensors.version)

    for chip in sensors.ChipIterator(): # optional arg like "coretemp-*" restricts iterator
        print(sensors.chip_snprintf_name(chip)+" ("+sensors.get_adapter_name(chip.bus)+")")
        for feature in sensors.FeatureIterator(chip):
            check_feature(chip, feature)

    sensors.cleanup()
