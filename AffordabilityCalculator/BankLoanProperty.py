'''
Created on 19 Jun 2017

@author: zhi liang & victor
'''
from src.findMaxLoan import findMaxLoan
from pulp import LpProblem, LpVariable, LpConstraint, LpMaximize, LpMinimize, value
from difflib import Differ

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
        amountDic[2*x + 10] = cashSavings

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
        amountDic[2*x + 1] = CPFOA
        amountDic[2*x + 2] = CPFRefund
        amountDic[2*x + 9] = cashProceeds
        amountDic[2*x + 10] = cashSavings

    
dispatcher = {'1' : singleFirst, '2': jointFirst, '3': singleContra, '4': joinContra, '5': singleBS, '6': jointBS}
dispatcher[nb1]()
#nb2 = cpf nb3 = cash nb4 = loan
nb2 = 0
nb3 = 0
#print(amountDic)
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
print(weightedAge)
sumCar = sum(carLoanList)
sumHomeLoan = sum(homeLoanList)
sumOtherCommitment = sum(otherCommitmentList)

maximumHDBLoan = findMaxLoan(3.5, sumSalary, weightedAge, sumCar, sumHomeLoan, sumOtherCommitment)

print("loan:" + str(maximumHDBLoan))

fees = 2000
if ((int(nb2) + int(nb3)) < fees):
    print("Not enough CPF and Cash to even cover legal fees")
    quit()
    
if (int(nb2) < fees):
    initialCPF = 0
    initialCash = int(nb3) - (fees - int(nb2))
else:
    initialCPF = int(nb2) - fees
    initialCash = int(nb3)
CPFinput = int(nb2)
Cashinput = int(nb3)
initialFunds = initialCPF + initialCash


if (initialCash < (maximumHDBLoan/16)): 
    if (3 * initialCash <= initialCPF): #case 1 i.e cash not enough for 5% and 15% = pure CPF with excess CPF
        excessCash = 0
        fifteenPercentCash = 0
        usedCPF = initialCash * 3
        excessCPF = initialCPF - usedCPF
        fivePercentCash = initialCash
        newPropertyPrice = fivePercentCash * 20
        initialTwentyPercent = fivePercentCash * 4
        currentStampDuty = calculateStampDuty(newPropertyPrice)

        if (excessCPF < currentStampDuty):
            outstandingStampDuty = currentStampDuty - excessCPF 
            usedCPF = usedCPF - outstandingStampDuty
            fivePercentCash = (usedCPF + fivePercentCash)/4 #normalise 5% accordingly
            fifteenPercentCash = initialCash - fivePercentCash
            excessCPF = 0
            twentyPercent = fivePercentCash + fifteenPercentCash + usedCPF
            newPropertyPrice = twentyPercent * 5
            newStampDuty = calculateStampDuty(newPropertyPrice)
            difference = 1000
            while(abs(difference) > 1):
                difference = newStampDuty - currentStampDuty
                if (excessCPF == 0):
                    twentyPercent = twentyPercent - difference
                    if (twentyPercent > initialTwentyPercent):
                        excessCPF = twentyPercent - initialTwentyPercent
                        twentyPercent = initialTwentyPercent
                        newPropertyPrice = initialTwentyPercent * 5
                    else:
                        newPropertyPrice = twentyPercent * 5
                else:
                    if (difference <= 0):
                        break
                    else:
                        if (excessCPF < difference):
                            excessCPF = 0
                            twentyPercent = twentyPercent - (difference - excessCPF)
                            newPropertyPrice = twentyPercent * 5
                        else:
                            excessCPF = excessCPF - difference
                            break
                #print("new Property Price: " + str(newPropertyPrice))
                currentStampDuty = newStampDuty
                newStampDuty = calculateStampDuty(newPropertyPrice)
            print("cash input: " + str(Cashinput))
            print("CPF input: " + str(CPFinput))
            print("your max prop price: " + str(newPropertyPrice))
            fivePercentCashFinal = (twentyPercent/4)
            print("fivePercent Cash used: " + str(fivePercentCashFinal))
            fifteenPercentCashFinal = twentyPercent * (fifteenPercentCash/(fifteenPercentCash + fivePercentCash + usedCPF))
            print("fifteenPercent Cash used: " + str(fifteenPercentCashFinal))
            usedCPFFinal = twentyPercent * (usedCPF/(fifteenPercentCash + fivePercentCash + usedCPF))
            print("CPF in fifteenPercent used: " + str(usedCPFFinal))
            print("excessCPF unused: " + str(excessCPF))
            print("excessCPF used: 0")
            print("excessCash used to top up: " + str(excessCash))
            loan = newPropertyPrice - twentyPercent
            print("Stamp Duty paid: " + str(newStampDuty))
            print("HDB Loan taken: " + str(loan) + " out of: " + str(maximumHDBLoan))
        else:
            excessCash = 0
            excessCPF = excessCPF - currentStampDuty
            print("your max prop price: " + str(newPropertyPrice))
            print("fivePercent Cash used: " + str(fivePercentCash))
            print("fifteenPercent Cash used: " + str(fifteenPercentCash))
            print("CPF in fifteenPercent used: " + str(usedCPF))
            print("excessCPF unused: " + str(excessCPF))
            print("excessCPF used: 0")
            print("excessCash used to top up: " + str(excessCash))
            print("Stamp Duty paid: " + str(currentStampDuty))
            loan = newPropertyPrice - (fivePercentCash + fifteenPercentCash + usedCPF)
            print("HDB Loan taken: " + str(loan) + " out of: " + str(maximumHDBLoan))
             
            
    else: #case 2 i.e 15% has some CPF and some cash. Also no excess CPF at all.
        fivePercentCash = (initialCash + initialCPF) / 4
        fifteenPercentCash = initialCash - fivePercentCash
        usedCPF = initialCPF #All CPF will be used in the 15% pool
        excessCash = 0
        excessCPF = 0
        newPropertyPrice = fivePercentCash * 20
        currentStampDuty = calculateStampDuty(newPropertyPrice)
        assert (fivePercentCash + fifteenPercentCash == initialCash), "totalCash = " + str(fivePercentCash + fifteenPercentCash) + " initialCash = " + str(initialCash)
        if (usedCPF >= currentStampDuty): #we prioritise removing stamp duty amount from CPF portion firsts
            usedCPF = usedCPF - currentStampDuty
            fivePercentCash = (initialCash + usedCPF) / 4
            fifteenPercentCash = initialCash - fivePercentCash
            assert (fivePercentCash + fifteenPercentCash == initialCash), "totalCash = " + str(fivePercentCash + fifteenPercentCash) + " initialCash = " + str(initialCash)
            newPropertyPrice = fivePercentCash * 20
            newStampDuty = calculateStampDuty(newPropertyPrice)
            difference = 1000
            while(abs(difference) > 1):
                #print("new StampDuty is: " + str(newStampDuty))
                #print("current StampDuty is: " + str(currentStampDuty))
                #newPropertyPrice = 10*(initialCash - newStampDuty)
                difference = newStampDuty - currentStampDuty
                #print("diff: " + str(difference))
                usedCPF = usedCPF - difference
                fivePercentCash = (fivePercentCash + fifteenPercentCash + usedCPF) / 4
                fifteenPercentCash = initialCash - fivePercentCash
                assert (fivePercentCash + fifteenPercentCash == initialCash), "totalCash = " + str(fivePercentCash + fifteenPercentCash) + " initialCash = " + str(initialCash)
                newPropertyPrice = fivePercentCash * 20
                #print("new Property Price: " + str(newPropertyPrice))
                currentStampDuty = newStampDuty
                newStampDuty = calculateStampDuty(newPropertyPrice)
            print("cash input: " + str(Cashinput))
            print("CPF input: " + str(CPFinput))
            print("your max prop price: " + str(newPropertyPrice))
            print("fivePercent Cash used: " + str(fivePercentCash))
            print("fifteenPercent Cash used: " + str(fifteenPercentCash))
            print("CPF in fifteenPercent used: " + str(usedCPF))
            print("excessCPF unused: " + str(excessCPF))
            print("excessCash used to top up: " + str(excessCash))
            print("excessCPF used: 0")
            print("Stamp Duty paid: " + str(newStampDuty))
        else:
            fifteenPercentCash = fifteenPercentCash - (currentStampDuty - usedCPF)
            fivePercentCash = (fifteenPercentCash + fivePercentCash)/ 4
            fifteenPercentCash = fivePercentCash * 3
            avaiCash = fivePercentCash + fifteenPercentCash
            usedCPF = 0
            excessCPF = 0
            newPropertyPrice = fivePercentCash * 20
            newStampDuty = calculateStampDuty(newPropertyPrice)
            difference = 1000
            while(abs(difference) > 1):
                difference = newStampDuty - currentStampDuty
                if (fifteenPercentCash + fivePercentCash - difference > initialCash):
                    usedCPF = -(difference) - (initialCash - fifteenPercentCash - fivePercentCash)
                    fivePercentCash = (initialCash + usedCPF) / 4
                    fifteenPercentCash = initialCash - fivePercentCash
                    newPropertyPrice = fivePercentCash * 20
                    currentStampDuty = newStampDuty
                    newStampDuty = calculateStampDuty(newPropertyPrice)
                else:
                    fivePercentCash = (fivePercentCash + fifteenPercentCash - difference) / 4
                    fifteenPercentCash = fivePercentCash * 3
                    newPropertyPrice = fivePercentCash * 20
                    currentStampDuty = newStampDuty
                    newStampDuty = calculateStampDuty(newPropertyPrice)
            print("cash input: " + str(Cashinput))
            print("CPF input: " + str(CPFinput))
            print("your max prop price: " + str(newPropertyPrice))
            print("fivePercent Cash used: " + str(fivePercentCash))
            print("fifteenPercent Cash used: " + str(fifteenPercentCash))
            print("CPF in fifteenPercent used: " + str(usedCPF))
            print("excessCPF unused: " + str(excessCPF))
            print("excessCash used to top up: " + str(excessCash))
            print("excessCPF used: 0")
            print("Stamp Duty paid: " + str(newStampDuty))
else: #case 3 i.e cash can fulfill 5%
    fivePercentCash = maximumHDBLoan/16
    if (initialCPF + (initialCash - fivePercentCash) >= 3 * fivePercentCash and initialCPF >= 3 * fivePercentCash):
        
        # initialise solution using the optimal solution from a linear program, without stamp duty
        excessCash = initialCash - fivePercentCash   #case 3 i.e cash can fulfill 5% and 15% is pure CPF - excess cash and excess CPF
        usedCPF = (3 * fivePercentCash) #150000
        excessCPF = initialCPF - usedCPF
        x1 = LpVariable("x1", 0, excessCash)
        x2 = LpVariable("x2", 0, excessCash)
        y1 = LpVariable("y1", 0, excessCPF)
        y2 = LpVariable("y2", 0, excessCPF)
        prob = LpProblem("problem", LpMaximize)
        prob += x1 + x2 + y1 + y2
        prob += x1 + x2 <= excessCash
        prob += y1 + y2 <= excessCPF
        prob += 0.05*(x1 + x2 + y1 + y2) - x1 <= 0
        prob += 0.15*(x1 + x2 + y1 + y2) - y1 <= 0
        prob += 0.05*(x1 + x2 + y1 + y2) - x1 >= 0
        prob += 0.15*(x1 + x2 + y1 + y2) - y1 >= 0
        status = prob.solve()
        addedCash = value(x1)
        addedCPF = value(y1)
        excessCash = excessCash - addedCash #used
        excessCPFused = value(y2) 
        excessCPFnotUsed = excessCPF - excessCPFused - addedCPF #cannot use
        fivePercentCash = fivePercentCash + value(x1)# + 0.05 * (excessCash)
        fifteenPercentCash = 0
        usedCPF = usedCPF + addedCPF      
        newPropertyPrice = fivePercentCash * 20
        currentStampDuty = calculateStampDuty(newPropertyPrice)
        
        
        if (excessCPFnotUsed >= currentStampDuty): #working
            print("cash input: " + str(Cashinput))
            print("CPF input: " + str(CPFinput))
            print("your max prop price: " + str(newPropertyPrice))
            print("fivePercent Cash used: " + str(fivePercentCash))
            print("fifteenPercent Cash used: " + str(fifteenPercentCash))
            print("CPF in fifteenPercent used: " + str(usedCPF))
            print("excessCPF unused: " + str(excessCPFnotUsed - currentStampDuty))
            print("excessCPF used: " + str(excessCPFused))
            print("excessCash used: " + str(excessCash))
            print("Stamp Duty paid: " + str(currentStampDuty))      
        elif (excessCash + excessCPFnotUsed + excessCPFused >= currentStampDuty * 0.8 and excessCPFnotUsed < currentStampDuty): #problems maybe
            outstandingStampDuty = currentStampDuty - excessCPFnotUsed
            excessCPFnotUsed = 0
            if (excessCPFused < outstandingStampDuty * 0.8):
                outstandingStampDuty = outstandingStampDuty - 1.25 * excessCPFused
                fivePercentCash = fivePercentCash - 0.0625 * excessCPFused
                usedCPF = usedCPF - 0.1875 * excessCPFused
                excessCPFused = 0
                if (excessCash < outstandingStampDuty * 0.8):
                    usedCPF = usedCPF - 0.1875 * excessCash
                    fivePercentCash = fivePercentCash - 0.0625 * excessCash
                    outstandingStampDuty = outstandingStampDuty - 1.25 * excessCash
                    fivePercentCash = fivePercentCash - 0.25 * outstandingStampDuty
                    usedCPF = usedCPF - 0.75 * outstandingStampDuty
                    excessCash = 0
                    newPropertyPrice = fivePercentCash * 20
                    newStampDuty = calculateStampDuty(newPropertyPrice)
                else:
                    excessCash = excessCash - 0.8 * outstandingStampDuty
                    usedCPF = usedCPF - 0.15 * outstandingStampDuty
                    fivePercentCash = fivePercentCash - 0.05 * outstandingStampDuty
                    #newPropertyPrice = maximumHDBLoan + fivePercentCash + fifteenPercentCash + usedCPF + excessCash
                    newPropertyPrice = 20 * fivePercentCash
                    newStampDuty = calculateStampDuty(newPropertyPrice)
            else:
                excessCPFused = excessCPFused - 0.8 * outstandingStampDuty
                usedCPF = usedCPF - 0.15 * outstandingStampDuty
                fivePercentCash = fivePercentCash - 0.05 * outstandingStampDuty
                newPropertyPrice = maximumHDBLoan + fivePercentCash + fifteenPercentCash + usedCPF + excessCash + excessCPFused
                newStampDuty = calculateStampDuty(newPropertyPrice)
            difference = 1000
            while(abs(difference) > 1):
                difference = newStampDuty - currentStampDuty
                if (difference < 0):
                    print(difference)
                    if (not excessCash == 0):
                        fivePercentCash = fivePercentCash - 0.05 * difference
                        usedCPF = usedCPF - 0.15 * difference
                        excessCash = excessCash - 0.8 * difference
                    else:
                        fivePercentCash = fivePercentCash - 0.25 * difference
                        usedCPF = usedCPF - 0.75 * difference
                else:
                    if (excessCPFused < 0.8 * difference):
                        excessCPFused = 0
                        if (excessCash < 0.8 * (difference -  1.25 * excessCPFused)):
                            excessCash = 0
                            fivePercentCash = fivePercentCash - 0.25 * (difference - (1.25 * (excessCPFused + excessCash))) - 0.0625 * (excessCPFused + excessCash)
                            usedCPF = usedCPF - 0.75 * (difference - (1.25 * (excessCPFused + excessCash))) - 0.1875 * (excessCash + excessCPFused)
                        else:
                            excessCash = excessCash - 0.8 * (difference -  1.25 * excessCPFused)
                            fivePercentCash = fivePercentCash - 0.05 * (difference -  1.25 * excessCPFused) - 0.0625 * (excessCPFused)
                            usedCPF = usedCPF - 0.15 * (difference -  1.25 * excessCPFused) - 0.1875 * (excessCPFused)
                    else:
                        excessCPFused = excessCPFused - 0.8 * difference
                        fivePercentCash = fivePercentCash - 0.05 * (difference)
                        usedCPF = usedCPF - 0.15 * difference
                #newPropertyPrice = maximumHDBLoan + fivePercentCash + usedCPF + excessCPFused + excessCash
                newPropertyPrice = 20 * fivePercentCash
                currentStampDuty = newStampDuty
                newStampDuty = calculateStampDuty(newPropertyPrice)
            print("cash input: " + str(Cashinput))
            print("CPF input: " + str(CPFinput))
            print("your max prop price: " + str(newPropertyPrice))
            print("fivePercent Cash used: " + str(fivePercentCash))
            print("fifteenPercent Cash used: " + str(fifteenPercentCash))
            print("CPF in fifteenPercent used: " + str(usedCPF))
            print("excessCPF unused: " + str(excessCPFnotUsed))
            print("excessCPF used: " + str(excessCPFused))
            print("excessCash used: " + str(excessCash))
            print("Stamp Duty paid: " + str(newStampDuty))
        else:
            print(fivePercentCash)
            print(usedCPF)
            print(fifteenPercentCash)
            print(excessCash)
            print(excessCPFused)
            print(excessCPFnotUsed)
            outstandingStampDuty = currentStampDuty - excessCPFnotUsed - 1.25 * excessCPFused - 1.25 * excessCash
            initialFivePercent = maximumHDBLoan/16
            fivePercentCash = fivePercentCash - (excessCPFused + excessCash) * 0.0625 - (0.25 * (outstandingStampDuty))
            usedCPF = usedCPF - (excessCPFused + excessCash) * 0.1875 - (0.75 * (outstandingStampDuty))
            excessCPFnotUsed = 0
            excessCPFused = 0
            excessCash = 0
            newPropertyPrice = (fivePercentCash + usedCPF) * 5
            newStampDuty = calculateStampDuty(newPropertyPrice)
            difference = 1000
            while(abs(difference) > 1):
                print(fivePercentCash)
                print(usedCPF)
                print(newPropertyPrice)
                print(excessCash)
                print(newStampDuty)
                difference = newStampDuty - currentStampDuty
                print(difference)
                if (difference < 0):
                    if ((fivePercentCash - 0.25 * difference) > initialFivePercent):
                        toAdd = initialFivePercent - fivePercentCash
                        usedCPF = usedCPF + 3 * toAdd
                        excess = (fivePercentCash - 0.25 * difference) - initialFivePercent
                        print(initialFivePercent)
                        print(fivePercentCash)
                        print(difference)
                        print("excess: " + str(excess))
                        fivePercentCash = initialFivePercent
                        fivePercentCash = fivePercentCash + 0.05 * excess
                        usedCPF = usedCPF + 0.15 * excess
                        excessCash = excessCash + 0.8 * excess
                    else:
                        fivePercentCash = fivePercentCash - 0.25 * difference
                        usedCPF = usedCPF - 0.75 * difference
                else:
                    if (excessCash == 0):
                        fivePercentCash = fivePercentCash - 0.25 * difference
                        usedCPF = usedCPF - 0.75 * difference
                    elif (excessCash < 0.8 * difference):
                        fivePercentCash = fivePercentCash - 0.0625 * excessCash
                        usedCPF = usedCPF - 0.1875 * excessCash
                        outstandingDifference = 1.25 * excessCash
                        fivePercentCash = fivePercentCash - 0.25 * outstandingDifference
                        usedCPF = usedCPF - 0.75 * outstandingDifference
                        excessCash = 0
                    else:
                        excessCash = excessCash - 0.8 * difference
                        fivePercentCash = fivePercentCash - 0.05 * difference
                        usedCPF = usedCPF - 0.15 * difference

                #newPropertyPrice = currentLoan + fivePercentCash + fifteenPercentCash + usedCPF + excessCash + excessCPFused
                newPropertyPrice = 20 * fivePercentCash
                currentStampDuty = newStampDuty
                newStampDuty = calculateStampDuty(newPropertyPrice)
            print("cash input: " + str(Cashinput))
            print("CPF input: " + str(CPFinput))
            print("your max prop price: " + str(newPropertyPrice))
            print("fivePercent Cash used: " + str(fivePercentCash))
            print("fifteenPercent Cash used: " + str(fifteenPercentCash))
            print("CPF in fifteenPercent used: " + str(usedCPF))
            print("excessCPF unused: " + str(excessCPFnotUsed))
            print("excessCPF used: " + str(excessCPFused))
            print("excessCash used: " + str(excessCash))
            print("Stamp Duty paid: " + str(newStampDuty))   
    elif (initialCPF + (initialCash - fivePercentCash) >= 3 * fivePercentCash and initialCPF < 3 * fivePercentCash):
        excessCPF = 0 #case 4 i.e cash can fulfill 5%, 15% contains both CPF and cash. No excess CPF
        excessCash = initialCash - fivePercentCash - (3 * fivePercentCash - initialCPF) #problem maybe
        fifteenPercentCash = initialCash - fivePercentCash - excessCash
        usedCPF = initialCPF
        newPropertyPrice = maximumHDBLoan + fifteenPercentCash + usedCPF + fivePercentCash + excessCash
        newfivePercentCash = fivePercentCash + 0.05 * excessCash #NOT FIVE PERCENT OF PROPERTY PRICE NOW
        newfifteenPercentCash = fifteenPercentCash + 0.15 * excessCash
        excessCash = 0.8 * excessCash
        currentStampDuty = calculateStampDuty(newPropertyPrice)

        if (excessCash <  0.8 * currentStampDuty):
            #print("here1")
            outstandingStampDuty = currentStampDuty -  1.25 * excessCash
            newfivePercentCash_1 = newfivePercentCash - outstandingStampDuty/4 - excessCash/16
            newfifteenPercentCash_1 = (newfifteenPercentCash - (((3/4) * outstandingStampDuty + 0.1875 * excessCash) * newfifteenPercentCash/(newfifteenPercentCash + usedCPF)))
            usedCPF_1 = (usedCPF - (((3/4) * outstandingStampDuty + 0.1875 * excessCash) * usedCPF/(newfifteenPercentCash + usedCPF)))
            excessCash = 0
            newfivePercentCash = newfivePercentCash_1
            newfifteenPercentCash = newfifteenPercentCash_1
            usedCPF = usedCPF_1
            newPropertyPrice = newfivePercentCash * 20
            newStampDuty = calculateStampDuty(newPropertyPrice)
        else:
            #print("here2")
            excessCash = excessCash - (0.8 * currentStampDuty)
            newfivePercentCash_1 = newfivePercentCash - (0.05 * currentStampDuty)
            newfifteenPercentCash_1 = newfifteenPercentCash - (0.15 * currentStampDuty)
            newfivePercentCash = newfivePercentCash_1
            newfifteenPercentCash = newfifteenPercentCash_1
            newPropertyPrice = newPropertyPrice - currentStampDuty
            newStampDuty = calculateStampDuty(newPropertyPrice)
        difference = 1000
        while(abs(difference) > 1):
            difference = newStampDuty - currentStampDuty
            if (excessCash == 0):
                if (difference < 0):
                    #print("here3")
                    excessCash = excessCash - 0.8 * difference
                    newfivePercentCash = newfivePercentCash - 0.05 * difference
                    newfifteenPercentCash_1 = newfifteenPercentCash - (0.15 * difference * (newfifteenPercentCash)/(newfifteenPercentCash + usedCPF))
                    usedCPF_1 = usedCPF - (0.15 * difference * (usedCPF/(usedCPF + newfifteenPercentCash)))
                    newfifteenPercentCash = newfifteenPercentCash_1
                    usedCPF = usedCPF_1
                    newPropertyPrice = newPropertyPrice - difference
                    currentStampDuty = newStampDuty
                    newStampDuty = calculateStampDuty(newPropertyPrice)
                else:
                    if (difference <= (fivePercentCash + fifteenPercentCash - (newfifteenPercentCash + newfivePercentCash))):
                        #print("here4")
                        newfivePercentCash = newfivePercentCash - 0.25 * difference
                        newfifteenPercentCash_1 = newfifteenPercentCash - (0.75 * difference * (newfifteenPercentCash)/(newfifteenPercentCash + usedCPF))
                        usedCPF_1 = usedCPF - (0.75 * difference * (usedCPF/(usedCPF + newfifteenPercentCash)))
                        newfifteenPercentCash = newfifteenPercentCash_1
                        usedCPF = usedCPF_1      
                        newPropertyPrice = 5 * (newfivePercentCash + newfifteenPercentCash + usedCPF)
                        currentStampDuty = newStampDuty
                        newStampDuty = calculateStampDuty(newPropertyPrice)
                    else:
                        #print("here5")
                        newfivePercentCash = fivePercentCash
                        newfifteenPercentCash = fifteenPercentCash
                        excessCash = difference - (fivePercentCash + fifteenPercentCash - (newfifteenPercentCash + newfivePercentCash))
                        newPropertyPrice = newfifteenPercentCash + newfivePercentCash + maximumHDBLoan + excessCash
                        currentStampDuty = newStampDuty
                        newStampDuty = calculateStampDuty(newPropertyPrice)
                                                   
            else:
                if (difference < 0):
                    #print("here6")
                    excessCash = excessCash - 0.8 * difference
                    newfivePercentCash = newfivePercentCash - (0.05 * difference)
                    newfifteenPercentCash_1 = newfifteenPercentCash - (0.15 * difference)
                    #usedCPF_1 = usedCPF - (0.15 * difference * (usedCPF/(usedCPF + newfifteenPercentCash)))
                    newfifteenPercentCash = newfifteenPercentCash_1
                    #usedCPF = usedCPF_1         
                    newPropertyPrice = (newfivePercentCash * 20)
                    currentStampDuty = newStampDuty
                    newStampDuty = calculateStampDuty(newPropertyPrice)
                else:
                    if (excessCash < difference):
                        #print("here7")
                        outstandingDifference = difference - excessCash
                        excessCash = 0
                        newfivePercentCash = newfivePercentCash - 0.25 * outstandingDifference
                        newfifteenPercentCash_1 = newfifteenPercentCash - (0.75 * outstandingDifference * (newfifteenPercentCash)/(newfifteenPercentCash + usedCPF))
                        usedCPF_1 = usedCPF - (0.75 * outstandingDifference * (usedCPF/(usedCPF + newfifteenPercentCash)))
                        newfifteenPercentCash = newfifteenPercentCash_1
                        usedCPF = usedCPF_1         
                        newPropertyPrice = newfivePercentCash * 20
                        currentStampDuty = newStampDuty
                        newStampDuty = calculateStampDuty(newPropertyPrice)
                    else:# PROBLEM
                        #print("here8")
                        excessCash = excessCash - 0.8 * difference
                        newfivePercentCash = newfivePercentCash - 0.0625 * difference
                        newfifteenPercentCash_1 = newfifteenPercentCash - (0.1875 * difference * (newfifteenPercentCash)/(newfifteenPercentCash + usedCPF))
                        usedCPF_1 = usedCPF - (0.1875 * difference * (usedCPF/(usedCPF + newfifteenPercentCash)))
                        newfifteenPercentCash = newfifteenPercentCash_1
                        usedCPF = usedCPF_1
                        
                        newPropertyPrice = newfivePercentCash * 20
                        currentStampDuty = newStampDuty
                        newStampDuty = calculateStampDuty(newPropertyPrice)
        print("cash input: " + str(Cashinput))
        print("CPF input: " + str(CPFinput))
        print("your max prop price: " + str(newPropertyPrice))
        print("fivePercent Cash used: " + str(newfivePercentCash))
        print("fifteenPercent Cash used: " + str(newfifteenPercentCash))
        print("CPF in fifteenPercent used: " + str(usedCPF))
        print("excessCPF unused: " + str(excessCPF))
        print("excessCash used to top up: " + str(excessCash))
        print("excessCPF used: " + str(excessCPF))
        print("Stamp Duty paid: " + str(newStampDuty))                
        #print("used CPF: " + str((newusedCPF/(newfivePercentCash + newusedCPF + newfifteenPercentCash) * twentyPercent)))
        #print("five Percent Cash: " + str((newfivePercentCash/(newfivePercentCash + newusedCPF + newfifteenPercentCash) * twentyPercent)))
        #print("fifteen Percent Cash: " + str((newfifteenPercentCash/(newfivePercentCash + newusedCPF + newfifteenPercentCash) * twentyPercent)))
    else: #case 5 i.e no excess anything. 15% contains both CPF and cash. Cash no longer is 5% because some channelled for burden CPF portion. Total property price goes down
        #print("here!!!")
        twentyPercent = initialCPF + initialCash
        fivePercentCash = (twentyPercent/4)
        fifteenPercentCash = initialCash - fivePercentCash
        usedCPF = initialCPF
        newPropertyPrice = twentyPercent * 5
        currentStampDuty = calculateStampDuty(newPropertyPrice)
        twentyPercent = twentyPercent - currentStampDuty
        newPropertyPrice = twentyPercent * 5
        newStampDuty = calculateStampDuty(newPropertyPrice)
        difference = 1000
        while(abs(difference) > 1):
            difference = newStampDuty - currentStampDuty
            twentyPercent = twentyPercent - difference
            newPropertyPrice = twentyPercent * 5
            currentStampDuty = newStampDuty
            newStampDuty = calculateStampDuty(newPropertyPrice)
        print("cash input: " + str(Cashinput))
        print("CPF input: " + str(CPFinput))
        print("your max prop price: " + str(newPropertyPrice))
        print("fivePercent Cash used: " + str(twentyPercent * (fivePercentCash/(usedCPF + fivePercentCash + fifteenPercentCash))))
        print("fifteenPercent Cash used: " + str(twentyPercent * (fifteenPercentCash/(usedCPF + fivePercentCash + fifteenPercentCash))))
        print("used CPF = " + str(twentyPercent * (usedCPF/(usedCPF + fivePercentCash + fifteenPercentCash))))
        print("excessCPF unused: 0")
        print("excessCash used to top up: 0")
        print("excessCPF used: 0")
        print("Stamp Duty paid: " + str(newStampDuty))
        
              
        

     
            
            
        
    
        
        
                       
                    
        



