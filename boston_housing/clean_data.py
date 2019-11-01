'''
The Boston house-price data of Harrison, D. and Rubinfeld, D.L. 'Hedonic
prices and the demand for clean air', J. Environ. Economics & Management,
vol.5, 81-102, 1978.   Used in Belsley, Kuh & Welsch, 'Regression diagnostics
...', Wiley, 1980.   N.B. Various transformations are used in the table on
pages 244-261 of the latter.

Variables in order:
CRIM     per capita crime rate by town
ZN       proportion of residential land zoned for lots over 25,000 sq.ft.
INDUS    proportion of non-retail business acres per town
CHAS     Charles River dummy variable (= 1 if tract bounds river; 0 otherwise)
NOX      nitric oxides concentration (parts per 10 million)
RM       average number of rooms per dwelling
AGE      proportion of owner-occupied units built prior to 1940
DIS      weighted distances to five Boston employment centres
RAD      index of accessibility to radial highways
TAX      full-value property-tax rate per $10,000
PTRATIO  pupil-teacher ratio by town
B        1000(Bk - 0.63)^2 where Bk is the proportion of blacks by town
LSTAT    % lower status of the population
MEDV     Median value of owner-occupied homes in $1000's
'''

input_path = 'houses.data'
output_path = 'houses.csv'

with open(input_path, 'r') as f:
    lines = f.readlines()

with open(output_path, 'w+') as f:
    csv_lines = ['CRIM,ZN,INDUS,CHAS,NOX,RM,AGE,DIS,RAD,TAX,PTRATIO,B,LSTAT,MEDV\n']
    
    for line in lines:
        current_line = []
        for chunk in line.split(' '):
            if chunk != '':
                chunk = chunk.replace('\n', '')
                current_line.append(chunk)
        
        if len(current_line) == 3:
            # 3 elements means we need to append to the previous line.
            previous_line = csv_lines[-1].split(',')
            current_line[-1] += '\n'
            csv_lines[-1] = ','.join(previous_line + current_line)
        else:
            csv_lines.append(','.join(current_line))
    
    f.writelines(csv_lines)
    print(f'Wrote {len(csv_lines)} line(s) to [{output_path}].')
