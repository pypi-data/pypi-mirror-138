# BMI calculation

### The following are the objective,
    

1) Calculate the BMI (Body Mass Index) using Formula 1, BMI Category and
Health risk from Input data (person_detail.json) of the person and add them as 3 new columns.

            Formula 1 - BMI
            BMI(kg/m2) = mass(kg) / height(m)2


2) Count the total number of overweight people using ranges in the column BMI
Category.

        BMI Category------------BMI Range (kg/m2)------------Health risk

        Underweight------------  18.4 and below ------------Malnutrition risk

        Normal weight------------ 18.5 - 24.9------------------Low risk

        Overweight---------------- 25 - 29.9 ----------------Enhanced risk

        Moderately obese---------- 30 - 34.9 ---------------- Medium risk

        Severely obese ----------- 35 - 39.9  ---------------- High risk

        Very severely obese ---- 40 and above ---------------Very high risk


### There are few major functions used in the whole program,

1. 'fitness_calc.py' (in 'src' directory) has the functions to calculate BMI, Categorization and the count of Overweight persons.
2. 'utility.py' is created to make functions generic. It has the file handling functions.
3. 'test.py' has the function to unit test the code.
4. 'main.py' is used to get the desired output from the input data.
5. 'person_detail.json' has the input data containing persons' Gender, Height and Weight.
6. 'Final_BMI_Results.csv' will give the desired out in .csv format.
7. 'setup.py' has the required package details. 


