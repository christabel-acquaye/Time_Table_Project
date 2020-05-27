
import datetime
import pprint


def checkConsecutive(l): 
    return sorted(l) == list(range(min(l), max(l)+1)) 
      
if __name__ == "__main__":
    
    ls = [
        {
            'period': 1,
            'date': '2020-05-07 00:00:00'
        },
        {
            'period': 2,
            'date': '2020-05-01 00:00:00'
        },
        {
            'period': 3,
            'date': '2020-05-01 00:00:00'
        },
        {
            'period': 4,
            'date': '2020-05-03 00:00:00'
        },
        {
            'period': 5,
            'date': '2020-05-02 00:00:00'
        },
        {
            'period': 6,
            'date': '2020-05-03 00:00:00'
        }

    ]
    
    ls.sort(key=lambda item: datetime.datetime.strptime(item['date'], "%Y-%m-%d %H:%M:%S"))
    
    count = 0
    grouped = {}
    for ass in range(len(ls)):
        period_ls = []
        if ls[ass-1]['date'] == ls[ass]['date']:
            period_ls.append(ls[ass-1]['period'])
            period_ls.append(ls[ass]['period'])
        else:
            period_ls.append(ls[ass]['period'])
        grouped.update({
            ls[ass]['date']: period_ls
        })
    
  
    pprint.pprint(grouped)
    for key in grouped:
        if len(grouped[key]) > 1:
            if checkConsecutive(grouped[key]):
                print(key, '->', grouped[key])
                count += 1
    print(count)
        



            
        
    
