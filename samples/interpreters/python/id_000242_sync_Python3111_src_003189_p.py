QUERY_SETUP ='''
SELECT
    '{A} ->> ({B}, {C}) in {R}' AS MV, CASE WHEN COUNT(*) = 0 THEN 'MAYBE MVD' ELSE 'NO MVD' END AS MVDFROM 
    FROM(    
        SELECT 
            {A} 
        FROM 
            {R} 
        GROUP BY {A}    
        HAVING COUNT(*) > 1 AND COUNT(*) <> COUNT(DISTINCT {B}) * COUNT(DISTINCT {C})) 
        X;
'''


tables =[   
            
            
            ("Projects",("ID","PID","SID","SN","PN","MID","MN")),
            ("Coffees",("DID","HID","CID","DN","DS","CN","CC"))
        ]


from itertools import permutations

def writer():
    with open("MV_checks.sql","w") as fd_checks:
        for table, columns in tables:
            for x,y,z in permutations(columns,3):
                fd_checks.write(QUERY_SETUP.format(R=table,A=x,B=y,C=z))

writer()
