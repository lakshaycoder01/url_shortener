import unicodecsv as csv

toCSV = [
    {"url": "http://www.legislation.qld.gov.au", "value": "12345"},
    {"url": "http://pittstreetpress.com", "value": "thrifk"},
    {"url": "http://www.peddleitnow.com.au", "value": "hQge0yg"}
]


keys = toCSV[0].keys()
print(keys)
with open('url.csv', 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(toCSV)
