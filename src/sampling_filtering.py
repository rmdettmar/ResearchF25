import json
import ast
import cocotb
from cocotb.binary import BinaryValue

def compare_scenarios(taskid):
    flag=True
    # Read file contents
    with open(f'{taskid}/our_output.txt', 'r') as f:
        
        lines = f.readlines()
    
    # Parse data from each line
    all_test_cases = []
    for line in lines:

            # Convert string to Python object
            parsed = ast.literal_eval(line)
            if parsed[0] and 'out' in parsed[1]:
                # Parse JSON string
                test_cases = json.loads(parsed[1]['out'])
                
                
                for ke in test_cases:
                    for m in ke:
                        
                        for mm in m:
                            
                            test_cases=[]
                            test_tt={}
                            if mm!='clock cycles':
                                

                                
                                    # Convert binary string to integer
                                    test_tt[mm] = [int(BinaryValue(t).integer) for t in m[mm]]
                            test_cases.append(test_tt)
                               
                all_test_cases.append(test_cases)
 
    
    
    # Compare by scenario groups
    inconsistencies = {}
   

            
    for k in range(len(all_test_cases[0])):
                   
                            
                inconsistencies[k]=[]  

    flag=False
    # Compare all combinations pairwise
    for i in range(len(all_test_cases)):
        for j in range(i+1, len(all_test_cases)):
            # Compare ith and jth groups
            
                for k in range(len(all_test_cases[i])):
                    # Compare output variable
                    if str(all_test_cases[i][k]) != str(all_test_cases[j][k]):
                            flag=True
                            
                            inconsistencies[k].append({
                                'group_pair': [i, j],
                                
                            })
    if taskid in [40, 72, 79, 80, 88, 97, 106, 120, 141, 142, 146, 154]:
        print(taskid,inconsistencies)
    return flag
result={}
cases=[33, 36, 40, 42, 43, 52, 55, 56, 59, 60, 63, 66, 69, 72, 74, 75, 76, 77, 78, 79, 80, 86, 88, 89, 92, 93,  97, 98, 99, 103, 104, 105, 106, 107, 110, 118, 120, 122, 126, 127, 129, 133, 137, 141, 142, 144, 145, 146,  151, 152, 153, 154]
for i in cases  :
    
    result[i]=compare_scenarios(i)
print(result)
not_success=[]
success=[]
for i in cases:
    
    if result[i]==False:
        success.append(i)
    else:
        not_success.append(i)
print(not_success)
print(success)