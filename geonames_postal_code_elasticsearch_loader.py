# coding: utf-8
from __future__ import print_function
from elasticsearch import Elasticsearch, helpers
import csv
import sys
from datetime import datetime
from tqdm import tqdm
import time

csv.field_size_limit(sys.maxsize)
es = Elasticsearch(sys.argv[2])

reload(sys)  
sys.setdefaultencoding('utf8')

def documents(reader, es):
    todays_date = datetime.today().strftime("%Y-%m-%d")
    count = 0
    i = 0
    for row in tqdm(reader, total=1264941): # approx
        try:
            coords = row[9] + "," + row[10]
            doc = { "country_code" : row[0],
                    "postal_code" : row[1],
                    "place_name" : row[2],
                    "admin_name1" : row[3],
                    "admin_code1" : row[4],
                    "admin_name2" : row[5],
                    "admin_code2" : row[6],
                    "admin_name3" : row[7],
                    "admin_code3" : row[8],
                    "accuracy" : row[11],
                    "coordinates" : coords,  # 9, 10
                    "modification_date" : todays_date,
                    "suggest": {
                        "input" : [row[2]]
                    }
                   }
            action = {"_index" : "geonames_postalcode",
                      "_type" : "geoname",
                      "_id" : i,
                      "_source" : doc}
            yield action
            i+=1
        except:
            count += 1
    print('Exception count:', count)

if __name__ == "__main__":
    t = time.time()
    f = open(sys.argv[1] + '.txt', 'rt')
    reader = csv.reader(f, delimiter='\t')
    actions = documents(reader, es)
    helpers.bulk(es, actions, chunk_size=500)
    es.indices.refresh(index='geonames_postalcode')
    e = (time.time() - t) / 60
    print("Elapsed minutes: ", e)
