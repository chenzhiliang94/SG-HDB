'''
Created on 16 Jun 2017

@author: zhi liang
'''
from src.findMaxLoan import findMaxLoan
from src.getCPFToTopUp import getCPFToTopUp

nb1 = input('What is the purchase type? \n 1 for Single - 1st purchase \n 2 for Joint - 1st Purchase \n 3 for Single - Contra \n 4 for Joint - Contra \n 5 for Single - Buy and Sell \n 6 for Joint - Buy and Sell \n Answer:')
amountDic = {'1' : None,'2' : None,'3' : None,'4' : None,'5' : None,'6' : None,'7' : None,'8' : None,'9' : None,'10' : None,'11' : None,'12' : None,'13' : None,'14' : None,'15' : None,'16' : None}
numberBuyer = 1
def singleFirst():
    numberBuyer = 1
    CPFOA = input('input CPF Ordinary Account amount: ')
    cashSavings = input('input Cash Savings amount: ')     
    amountDic[1] = CPFOA
    amountDic[10] = cashSavings
            

def jointFirst():
    global numberBuyer
    numberBuyer = int(input("How many buyers?"))
    for x in range(numberBuyer):
        CPFOA = input("input CPF Ordinary Account amount of person number " + str(x+1) + ": ")
        cashSavings = input("input Cash savings amount of person number " + str(x+1) + ": ")
        amountDic[2*x + 1] = CPFOA
        amountDic[2*x + 9] = cashSavings

def singleContra():
    numberBuyer = 1
    CPFOA = input('input CPF Ordinary Account amount: ')
    CPFRefund = input('input CPF refund from previous sale: ') #determined by government
    cashProceeds = input('input Cash proceeds amount: ')
    cashSavings = input('input Cash Savings amount: ')     
    amountDic[1] = CPFOA
    amountDic[2] = CPFRefund
    amountDic[9] = cashProceeds
    amountDic[10] = cashSavings
    
def joinContra():
    global numberBuyer
    numberBuyer = int(input("How many buyers?"))
    for x in range(numberBuyer):
        CPFOA = input("input CPF Ordinary Account amount of person number " + str(x+1) + ": ")
        CPFRefund = input('input CPF refund from previous sale: ')
        cashProceeds = input('input Cash proceeds amount: ')
        cashSavings = input("input Cash savings amount of person number " + str(x+1) + ": ")
        amountDic[2*x + 1] = CPFOA
        amountDic[2*(x+1)] = CPFRefund
        amountDic[2*x + 9] = cashProceeds
        amountDic[2*x + 10] = cashSavings
        
def singleBS():
    numberBuyer = 1
    CPFOA = input('input CPF Ordinary Account amount: ')
    CPFRefund = input('input CPF refund from previous sale: ') #determined by user
    cashProceeds = input('input Cash proceeds amount: ')
    cashSavings = input('input Cash Savings amount: ')     
    amountDic[1] = CPFOA
    amountDic[2] = CPFRefund
    amountDic[9] = cashProceeds
    amountDic[10] = cashSavings
    
def jointBS():
    global numberBuyer
    numberBuyer = int(input("How many buyers?"))
    for x in range(numberBuyer):
        CPFOA = input("input CPF Ordinary Account amount of person number " + str(x+1) + ": ")
        CPFRefund = input('input CPF refund from previous sale: ')
        cashProceeds = input('input Cash proceeds amount: ')
        cashSavings = input("input Cash savings amount of person number " + str(x+1) + ": ")
        amountDic[2*x - 1] = CPFOA
        amountDic[2*x] = CPFRefund
        amountDic[2*x + 7] = cashProceeds
        amountDic[2*x + 8] = cashSavings

    
dispatcher = {'1' : singleFirst, '2': jointFirst, '3': singleContra, '4': joinContra, '5': singleBS, '6': jointBS}
dispatcher[nb1]()
#nb2 = cpf nb3 = cash nb4 = loan
nb2 = 0
nb3 = 0

for x in range(1,9):
    if (amountDic.get(x) == None):    
        nb2 = nb2
    else:
        nb2 = nb2 + int(amountDic[x])
for x in range(9,17):
    if (amountDic.get(x) == None):    
        nb3 = nb3
    else:
        nb3 = nb3 + int(amountDic[x])
    

def calculateStampDuty(propertyPrice):
    if (propertyPrice <= 180000):
        return 0.01 * propertyPrice
    elif (propertyPrice <= 360000):
        return 0.02 * (propertyPrice - 180000) + calculateStampDuty(180000)
    else:
        return 0.03 * (propertyPrice - 360000) + calculateStampDuty(360000)
'''
salaryList = [0,0,0,0]
homeLoanList = [0,0,0,0]
carLoanList = [0,0,0,0]
otherCommitmentList = [0,0,0,0]
ageList = [0,0,0,0]


for x in range(numberBuyer):
    ageList[x] = int(input('what is the age of person ' + str(x+1)))
    salaryList[x] = int(input('what is the salary of person ' + str(x+1)))
    homeLoanList[x] = int(input('what is the home loan of person ' + str(x+1)))
    carLoanList[x] = int(input('what is the car loan of person ' + str(x+1)))
    otherCommitmentList[x] = int(input('what are other commitments of person ' + str(x+1)))

numerator = 0
sumSalary = 0
for x in range(numberBuyer):
    numerator = numerator + ageList[x] * salaryList[x]
    sumSalary = sumSalary + salaryList[x]
weightedAge = numerator/sumSalary

sumCar = sum(carLoanList)
sumHomeLoan = sum(homeLoanList)
sumOtherCommitment = sum(otherCommitmentList)

maximumHDBLoan = findMaxLoan(3, sumSalary, weightedAge, sumCar, sumHomeLoan, sumOtherCommitment)
print("loan:" + str(maximumHDBLoan))
'''
   
maximumHDBLoan = 410000

fees = 2000
if (int(nb2) < fees):
    initialCPF = 0
    initialCash = int(nb3) - (fees - int(nb2))
else:
    initialCPF = int(nb2) - fees
    initialCash = int(nb3)
print(initialCPF)
print(initialCash)
initialFunds = initialCPF + initialCash

currentPropertyPrice = maximumHDBLoan * (10/9)
tenPercent = maximumHDBLoan/9
TEN_PERCENT = 0.1
ERROR_DIFFERENCE = 1

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
            #print("new StampDuty is: " + str(newStampDuty))
            #print("current StampDuty is: " + str(currentStampDuty))
            #newPropertyPrice = 10*(initialCash - newStampDuty)
            difference = newStampDuty - currentStampDuty
            #print("diff: " + str(difference))
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
            
            #print("new Property Price: " + str(newPropertyPrice))
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
            print("cash input: " + str(nb3))
            print("CPF input: " + str(nb2))
            print("max Property Price: " + str(newPropertyPrice))
            print("ten Percent Cash: " + str(tenPercentCash))
            print("ten Percent CPF: " + str(tenPercentCPF))
            print("excessCash: " + str(excessCash))
            print("excessCPF: " + str(excessCPF))
            print("HDB loan taken: " + str(maximumHDBLoan))
            print("Stamp Duty Taken: " + str(newStampDuty))
            quit()
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
            #print("new StampDuty is: " + str(newStampDuty))
            #print("current StampDuty is: " + str(currentStampDuty))
            #newPropertyPrice = 10*(initialCash - newStampDuty)
            if (difference < 0):
                toAddCash = TEN_PERCENT * difference * (tenPercentCash/(tenPercentCash + tenPercentCPF))
                toAddCPF = TEN_PERCENT * difference * (tenPercentCPF/(tenPercentCash + tenPercentCPF))
                tenPercentCash = tenPercentCash - toAddCash
                tenPercentCPF = tenPercentCPF - toAddCPF
                '''toAddCash = 0.9 * difference * (excessCash/(excessCash + excessCPF))
                toAddCPF = 0.9 * difference * (excessCPF/(excessCash + excessCPF))
                tenPercentCash = tenPercentCash - toAddCash
                tenPercentCPF = tenPercentCPF - toAddCPF
                '''
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
print("cash input: " + str(nb3))
print("CPF input: " + str(nb2))
print("max Property Price: " + str(newPropertyPrice))
print("ten Percent Cash: " + str(tenPercentCash))
print("ten Percent CPF: " + str(tenPercentCPF))
print("excessCash: " + str(excessCash))
print("excessCPF: " + str(excessCPF))
print("HDB loan taken: " + str(maximumHDBLoan))
print("Stamp Duty Taken: " + str(newStampDuty))


