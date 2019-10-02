'''
Created on 16 Jun 2017

@author: zhi liang
'''

from getCPFToTopUp import getCPFToTopUp

def calculateStampDuty(propertyPrice):
    if (propertyPrice <= 180000):
        return 0.01 * propertyPrice
    elif (propertyPrice <= 360000):
        return 0.02 * (propertyPrice - 180000) + calculateStampDuty(180000)
    else:
        return 0.03 * (propertyPrice - 360000) + calculateStampDuty(360000)


def calculate(inputCPF, inputCash, loan):

    maximumHDBLoan = loan
    FEES = 2000
    initialCPF = 0
    initialCash = 0
    currentPropertyPrice = maximumHDBLoan * (10 / 9)
    TEN_PERCENT = 0.1
    ERROR_DIFFERENCE = 1

    if (int(inputCPF) < FEES):
        initialCPF = 0
        initialCash = int(inputCash) - (FEES - int(inputCPF))
    else:
        initialCPF = int(inputCPF) - FEES
        initialCash = int(inputCash)

    initialFunds = initialCPF + initialCash
    tenPercent = maximumHDBLoan / 9


    if (initialFunds >= (TEN_PERCENT * currentPropertyPrice)):
        if (initialCPF < (TEN_PERCENT * currentPropertyPrice)):
            newPropertyPrice = initialFunds + maximumHDBLoan
            excessCash = initialCash - (TEN_PERCENT * currentPropertyPrice - initialCPF)
            tenPercentCash = (TEN_PERCENT * currentPropertyPrice - initialCPF) + (TEN_PERCENT * excessCash)
            tenPercentCPF = initialCPF
            excessCPF = 0
            excessCash = 0.9 * excessCash
            currentStampDuty = calculateStampDuty(newPropertyPrice)
            if (excessCash >= 0.9 * currentStampDuty):
                excessCash = excessCash - 0.9 * currentStampDuty
                if (tenPercentCPF >= TEN_PERCENT * currentStampDuty):
                    tenPercentCPF = tenPercentCPF - (TEN_PERCENT * currentStampDuty)
                else:
                    tenPercentCash = tenPercentCash - (TEN_PERCENT * currentStampDuty - tenPercentCPF)
                    tenPercentCPF = 0
                newPropertyPrice = (tenPercentCash + tenPercentCPF) * 10
                newStampDuty = calculateStampDuty(newPropertyPrice)
            else:
                tenPercentCash = tenPercentCash - (TEN_PERCENT * excessCash * (tenPercentCash/(tenPercentCash + tenPercentCPF)))
                tenPercentCPF = tenPercentCPF - (TEN_PERCENT * excessCash * (tenPercentCPF/(tenPercentCash + tenPercentCPF)))
                outstandingStampDuty = currentStampDuty - (10/9) * excessCash
                excessCash = 0
                if (tenPercentCPF >= outstandingStampDuty):
                    tenPercentCPF = tenPercentCPF - outstandingStampDuty
                else:
                    tenPercentCash = tenPercentCash - (outstandingStampDuty - tenPercentCPF)
                    tenPercentCPF = 0
                newPropertyPrice = (tenPercentCash + tenPercentCPF) * 10
                newStampDuty = calculateStampDuty(newPropertyPrice)

            difference = 1000
            while(abs(difference) > 1):
                difference = newStampDuty - currentStampDuty
                if (difference < 0):
                    toAddCash = TEN_PERCENT * difference * (tenPercentCash/(tenPercentCash + tenPercentCPF))
                    tenPercentCash = tenPercentCash - toAddCash
                    toAddCPF = TEN_PERCENT * difference * (tenPercentCPF/(tenPercentCash + tenPercentCPF))
                    tenPercentCPF = tenPercentCPF - toAddCPF
                    excessCash = excessCash - 0.9 * difference
                else:
                    if (excessCash >= difference * 0.9):
                        excessCash = excessCash - (0.9 * difference)
                        toRemoveCash = TEN_PERCENT * difference * (tenPercentCash/(tenPercentCash + tenPercentCPF))
                        toRemoveCPF = TEN_PERCENT * difference * (tenPercentCPF/(tenPercentCash + tenPercentCPF))
                        tenPercentCash = tenPercentCash - toRemoveCash
                        tenPercentCPF = tenPercentCPF - toRemoveCPF
                    else:
                        toRemoveCash = TEN_PERCENT * excessCash * (tenPercentCash/(tenPercentCash + tenPercentCPF))
                        toRemoveCPF = TEN_PERCENT * excessCash * (tenPercentCPF/(tenPercentCash + tenPercentCPF))
                        tenPercentCash = tenPercentCash - toRemoveCash
                        tenPercentCPF = tenPercentCash - toRemoveCPF
                        outstandingDifference = difference - (10/9) * excessCash
                        toRemoveCash = outstandingDifference * (tenPercentCash/(tenPercentCash + tenPercentCPF))
                        toRemoveCPF = outstandingDifference * excessCash * (tenPercentCPF/(tenPercentCash + tenPercentCPF))
                newPropertyPrice = (tenPercentCash + tenPercentCPF) * 10

                currentStampDuty = newStampDuty
                newStampDuty = calculateStampDuty(newPropertyPrice)
        else:
            tenPercentCPF = (TEN_PERCENT * currentPropertyPrice) #CPF used totally for 10%
            excessCPF = initialCPF - (tenPercentCPF) #excess CPF which can be used to pay stamp duty
            tenPercentCash = 0
            excessCash = initialCash
            tenPercentCash = tenPercentCash + TEN_PERCENT * excessCash
            excessCash = 0.9 * excessCash
            newPropertyPrice = tenPercentCash + tenPercentCPF + excessCash + maximumHDBLoan
            currentStampDuty = calculateStampDuty(newPropertyPrice)
            if (excessCPF >= currentStampDuty):

                excessCPF = excessCPF - currentStampDuty
                CPFToTopUp = getCPFToTopUp(excessCPF, newPropertyPrice, currentStampDuty)
                tenPercentCPF = tenPercentCPF + 0.1 * CPFToTopUp
                excessCPF = 0.9 * CPFToTopUp
                newPropertyPrice = newPropertyPrice + CPFToTopUp
                newStampDuty = calculateStampDuty(newPropertyPrice)

            else:
                outstandingStampDuty = currentStampDuty - excessCPF
                excessCPF = 0
                if (excessCash >= 0.9 * outstandingStampDuty):
                    toRemoveCash = (0.9 * outstandingStampDuty)
                    excessCash = excessCash - toRemoveCash
                    toRemoveCPF =  (0.1 * outstandingStampDuty * (tenPercentCPF/(tenPercentCPF + tenPercentCash)))
                    toRemoveCash =  (0.1 * outstandingStampDuty * (tenPercentCash/(tenPercentCPF + tenPercentCash)))
                    tenPercentCPF = tenPercentCPF - toRemoveCPF
                    tenPercentCash = tenPercentCash - toRemoveCash
                    newPropertyPrice = (tenPercentCash + excessCash + maximumHDBLoan)# excess cash
                else:
                    outstandingStampDuty = currentStampDuty - (10/9) * (excessCash)
                    tenPercentCPF = tenPercentCPF - (TEN_PERCENT * excessCash)
                    toRemoveCPF = (outstandingStampDuty)
                    tenPercentCPF = tenPercentCPF - toRemoveCPF
                    excessCash = 0
                    newPropertyPrice = (tenPercentCash * 10) #no excess anything
            newStampDuty = calculateStampDuty(newPropertyPrice)
            difference = 1000
            while(abs(difference) > 1):
                difference = newStampDuty - currentStampDuty
                if (difference < 0):
                    toAddCash = TEN_PERCENT * difference * (tenPercentCash/(tenPercentCash + tenPercentCPF))
                    toAddCPF = TEN_PERCENT * difference * (tenPercentCPF/(tenPercentCash + tenPercentCPF))
                    tenPercentCash = tenPercentCash - toAddCash
                    tenPercentCPF = tenPercentCPF - toAddCPF
                    excessCash = excessCash + 0.9 * difference
                else:
                    if (excessCPF + excessCash >= 0.9 * difference):
                        toRemoveCPF =  (0.9 * difference * (excessCPF/(excessCash + excessCPF)))
                        toRemoveCash = (0.9 * difference * (excessCash/(excessCash + excessCPF)))
                        excessCPF = excessCPF - toRemoveCPF
                        excessCash = excessCash - toRemoveCash
                        toAddCash = TEN_PERCENT * difference * (tenPercentCash/(tenPercentCash + tenPercentCPF))
                        toAddCPF = TEN_PERCENT * difference * (tenPercentCPF/(tenPercentCash + tenPercentCPF))
                        tenPercentCash = tenPercentCash - toAddCash
                        tenPercentCPF = tenPercentCPF - toAddCPF
                    else:
                        outstandingDifference = difference - (10/9) * (excessCPF + excessCash)
                        toRemoveCash = TEN_PERCENT * (excessCPF + excessCash) * (tenPercentCash/(tenPercentCash + tenPercentCPF))
                        toRemoveCPF = TEN_PERCENT * (excessCPF + excessCash) * (tenPercentCPF/(tenPercentCash + tenPercentCPF))
                        tenPercentCash = tenPercentCash - toAddCash
                        tenPercentCPF = tenPercentCPF - toAddCPF
                        toRemoveCPF =  (outstandingDifference * (tenPercentCPF/(tenPercentCash + tenPercentCPF)))
                        toRemoveCash = (outstandingDifference * (tenPercentCash/(tenPercentCash + tenPercentCPF)))
                        tenPercentCash = tenPercentCash - toRemoveCash
                        tenPercentCPF = tenPercentCPF - toRemoveCPF
                if (excessCash == 0):
                    newPropertyPrice = (tenPercentCash + tenPercentCPF) * 10
                else:
                    newPropertyPrice = (tenPercentCash + tenPercentCPF + excessCash + maximumHDBLoan)
                currentStampDuty = newStampDuty
                newStampDuty = calculateStampDuty(newPropertyPrice)


    elif (initialFunds < (TEN_PERCENT * currentPropertyPrice)):
        excessCash = 0
        excessCPF = 0
        tenPercentCash = initialCash
        tenPercentCPF = initialCPF
        newPropertyPrice = (tenPercentCash + tenPercentCPF) * 10
        currentStampDuty = calculateStampDuty(newPropertyPrice)
        toRemoveCash = currentStampDuty * (tenPercentCash/(tenPercentCash + tenPercentCPF))
        toRemoveCPF = currentStampDuty * (tenPercentCPF/(tenPercentCash + tenPercentCPF))
        tenPercentCash = tenPercentCash - toRemoveCash
        tenPercentCPF = tenPercentCPF - toRemoveCPF
        newPropertyPrice = (tenPercentCash + tenPercentCPF)*10
        newStampDuty = calculateStampDuty(newPropertyPrice)
        difference = 1000
        while(abs(difference) > 1):
            difference = newStampDuty - currentStampDuty
            toRemoveCash = difference * (tenPercentCash/(tenPercentCash + tenPercentCPF))
            toRemoveCPF = difference * (tenPercentCPF/(tenPercentCash + tenPercentCPF))
            tenPercentCash = tenPercentCash - toRemoveCash
            tenPercentCPF = tenPercentCPF - toRemoveCPF
            newPropertyPrice = (tenPercentCash + tenPercentCPF) * 10
            currentStampDuty = newStampDuty
            newStampDuty = calculateStampDuty(newPropertyPrice)
    CPFToTopUp = getCPFToTopUp(excessCPF, newPropertyPrice, newStampDuty)
    tenPercentCPF = tenPercentCPF + 0.1 * CPFToTopUp
    excessCPF = 0.9 * CPFToTopUp
    newPropertyPrice = newPropertyPrice + CPFToTopUp
    newStampDuty = calculateStampDuty(newPropertyPrice)
    print("legal fees: " + str(FEES))
    print("cash input: " + str(initialCash))
    print("CPF input: " + str(initialCPF))
    print("max Property Price: " + str(newPropertyPrice))
    print("ten Percent Cash: " + str(tenPercentCash))
    print("ten Percent CPF: " + str(tenPercentCPF))
    print("excessCash: " + str(excessCash))
    print("excessCPF: " + str(excessCPF))
    print("HDB loan taken: " + str(maximumHDBLoan))
    print("Stamp Duty Taken: " + str(newStampDuty))
    return FEES, initialCash, initialCPF, newPropertyPrice, tenPercentCash, tenPercentCPF, excessCash, excessCPF, newStampDuty


#CPFOA = input('input CPF Ordinary Account amount: ')
#cashSavings = input('input Cash Savings amount: ')

#initialCPF, initialCash = CPFOA, cashSavings
#calculate(initialCPF, initialCash)

