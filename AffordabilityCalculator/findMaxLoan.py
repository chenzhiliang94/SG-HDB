def findMaxLoan(interestRate, salary, age, carLoan, homeLoan, otherCommitments):

    totalDebtObligation = carLoan + homeLoan + otherCommitments
    age = max(age, 21)
    numerator = min((0.6 * salary - totalDebtObligation), (0.3 * salary - homeLoan))

    a = 0
    if (65 - age >= 25):
        a = (interestRate/1200) * (((interestRate/1200)+1)**300)
        b = (((1 + (interestRate/1200))**300)-1)
        return (numerator*b/a)
    else:
        a = (interestRate/1200) * (((interestRate/1200)+1)**((65-age)*12))
        b = (((1 + (interestRate/1200))**((65-age)*12))-1)
        return (numerator*b/a)
    
