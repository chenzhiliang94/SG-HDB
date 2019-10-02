'''
Created on 26 Jul 2017

@author: zhi liang
'''

# current stamp duty tiers
STAMP_DUTY_TIER_ONE = 180000
STAMP_DUTY_TIER_TWO = 360000
ONE_PERCENT = 0.01
TWO_PERCENT = 0.02
THREE_PERCENT = 0.03

def calculateStampDuty(propertyPrice):
    if (propertyPrice <= STAMP_DUTY_TIER_ONE):
        return ONE_PERCENT * propertyPrice
    elif (propertyPrice <= STAMP_DUTY_TIER_TWO):
        return TWO_PERCENT * (propertyPrice - STAMP_DUTY_TIER_ONE) + calculateStampDuty(STAMP_DUTY_TIER_ONE)
    else:
        return THREE_PERCENT * (propertyPrice - STAMP_DUTY_TIER_TWO) + calculateStampDuty(STAMP_DUTY_TIER_TWO)
    

def getCPFToTopUp(excessCPFUnused, initialPP, stampDuty):
    ERROR_MARGIN = 1
    CPFToBeChanneled = 0.5 * excessCPFUnused
    difference = abs((calculateStampDuty(initialPP + CPFToBeChanneled) - stampDuty) - (excessCPFUnused - CPFToBeChanneled))
    while (difference > ERROR_MARGIN):
        CPFToBeChanneled = CPFToBeChanneled + 1
        difference = abs((calculateStampDuty(initialPP + CPFToBeChanneled) - stampDuty) - (excessCPFUnused - CPFToBeChanneled))
    return CPFToBeChanneled
