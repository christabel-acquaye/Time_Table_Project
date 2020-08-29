import pprint
import operator
  
if __name__ == "__main__":
    ls = [
            {'alt': 210,
            'coord_latitude': '6.66759',
            'coord_longitude': '-1.56837',
            'id': '7',
            'roomName': 'OLD',
            'size': 200},
            {'alt': 105,
            'coord_latitude': '6.66759',
            'coord_longitude': '-1.56837',
            'id': '12',
            'roomName': 'NB_R2',
            'size': 100},
            {'alt': 210,
            'coord_latitude': '6.66759',
            'coord_longitude': '-1.56837',
            'id': '10',
            'roomName': 'EHC_102',
            'size': 200},
            {'alt': 210,
            'coord_latitude': '6.66759',
            'coord_longitude': '-1.56837',
            'id': '8',
            'roomName': 'NB_T3',
            'size': 200}]

    
    for item in ls:
        pprint.pprint(item)