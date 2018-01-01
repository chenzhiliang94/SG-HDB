# SG-HDB
Calculate what is the price of housing flat you can afford in Singapore!

If you are taking a bank loan - run python file: BankLoanProperty.py
If you are taking a HDB loan - run python file: HDBLoanProperty.py

Regardless, you must know the amount of CASH you have at hand and the amount of CPF you have

Also, the files ask for the number of people buying the flat - current HDB legislation (2017-2018) dictates that any amount of available CASH and CPF provided by each party
will be pooled together as one sum. Furthermore, personal details will be asked (such as salary per month, age etc) so the maximum loan available will be generated.

Current BANK LOAN policy: 
- 5% of final HDB price must be provided in cash
- 15% of final HDB price can be provided by cash or CPF, or a mixture of both
- loan can only fulfill ***up to 80%*** of the final HDB price.
- additional CPF ***can*** be used to top up the HDB final price, provided the percentages amount (5% pure cash, 15% mix cash and CPF) can be abided by 

Current HDB LOAN policy: 
- 10% of final HDB price must be provided by a mix of cash and CPF
- loan can only fulfill ***up to 90%*** of the final HDB price.
- additional CPF and CASH ***can*** be used to top up the HDB final price

STAMP DUTY amount applies in the following manner (STAMP DUTY can be paid with both CPF and CASH):
- first 180,000: 1%
- next 180,000: 2%
- remainder: 3%
- [source](http://www.hdb.gov.sg/cs/infoweb/business/estate-agents-and-salespersons/buying-a-resale-flat/costs-and-fees)


A flat legal fee of $2000 is applied regardless of which situation (can be covered with BOTH CPF and CASH)




How the maximum HDB price is calculated:
- The initial cash, CPF, and loan available are treated as variables in a linear programming model
- The constraints are created based on the 5%, 15%, 10% thresholds (depending which loan is taken)
- The initial optimal amount is initialised via linear programming and subjected to a further iterative method which converges to a
optimal maximum HDB price.
**Note**: The iterative method is needed because of the fluctuating stamp duty amount which cannot be fitted into a linear optimization model


Sources:
- Linear programming library used: puLp [source](https://pythonhosted.org/PuLP/)
- [Singapore HDB policy](http://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/new/hdb-flat)




