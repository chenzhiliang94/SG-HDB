'''
Created on 26 Jul 2017

@author: zhi liang
'''
def calculateStampDuty(propertyPrice):
    if (propertyPrice <= 180000):
        return 0.01 * propertyPrice
    elif (propertyPrice <= 360000):
        return 0.02 * (propertyPrice - 180000) + calculateStampDuty(180000)
    else:
        return 0.03 * (propertyPrice - 360000) + calculateStampDuty(360000)
    

def getCPFToTopUp(excessCPFUnused, initialPP, stampDuty):
    ERROR_MARGIN = 1
    CPFToBeChanneled = 0.5 * excessCPFUnused
    difference = abs((calculateStampDuty(initialPP + CPFToBeChanneled) - stampDuty) - (excessCPFUnused - CPFToBeChanneled))
    while (difference > ERROR_MARGIN):
        print(CPFToBeChanneled)
        CPFToBeChanneled = CPFToBeChanneled + 1
        difference = abs((calculateStampDuty(initialPP + CPFToBeChanneled) - stampDuty) - (excessCPFUnused - CPFToBeChanneled))
    return CPFToBeChanneled