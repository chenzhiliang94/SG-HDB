from HDBLoanProperty import calculate

loan_all = range(200000,600000, 10000)
inputCPF_all = range(10000, 50000, 3000)
inputCash_all = range (10000, 50000, 3000)

def testHDBAffordabibility(inputCPF, inputCash, loan):

    fees, initialCash, initialCPF, newPropertyPrice, \
    tenPercentCash, tenPercentCPF, excessCash, excessCPF, newStampDuty = calculate(inputCPF, inputCash, loan)
    if (excessCPF < 0 or excessCash < 0):
        return
    assertPercentageConstraint(tenPercentCash, tenPercentCPF, newPropertyPrice, excessCash, excessCPF)
    assertCorrectSum(tenPercentCash, tenPercentCPF, initialCPF, initialCash, fees, excessCash, excessCPF, newStampDuty)
    assertSufficientHouseLoan(tenPercentCash, tenPercentCPF, newPropertyPrice, loan, excessCash, excessCPF)


def assertPercentageConstraint(tenPercentCash, tenPercentCPF, newPropertyPrice, excessCash, excessCPF):
    ### assert that cash and CPF used in house purchase is always more or equals to 10%

    assert (((tenPercentCPF + tenPercentCash) - ((newPropertyPrice-excessCPF-excessCash)/10)) > -100)

def assertCorrectSum(tenPercentCash, tenPercentCPF, inputCPF, inputCash, fees, excessCash, excessCPF, newStampDuty):
    ### assert that sum of money used is equal or less than the amount of money available at the start
    assert ((tenPercentCash + tenPercentCPF  + excessCPF + excessCash + newStampDuty ) - (inputCash + inputCPF)) < 100

def assertSufficientHouseLoan(tenPercentCash, tenPercentCPF, newPropertyPrice, loan, excessCash, excessCPF):
    ### assert that loan used is sufficient

    assert (loan - (newPropertyPrice - (tenPercentCPF + tenPercentCash) - (excessCash + excessCPF))) > -100


def unitTestIteration(loans, CPFs, cashs):
    for loan in loans:
        for cpf in CPFs:
            for cash in cashs:
                testHDBAffordabibility(cpf, cash, loan)

unitTestIteration(loan_all, inputCPF_all, inputCash_all)

