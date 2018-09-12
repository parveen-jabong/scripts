import pandas
from csv import writer as csvwriter
from csv import QUOTE_NONE

OldUrlCounts = pandas.read_csv('./OldUrlCounts.csv')
NewUrlCounts = pandas.read_csv('./NewUrlCounts.csv')

oldUrls = OldUrlCounts['old_urls']
newUrls = NewUrlCounts['new_urls']
oldUrlCount = OldUrlCounts['count']
newUrlCount = NewUrlCounts['count']

with open('golden_count.csv', 'w', newline='', encoding='utf-8', buffering=1) as csvoutfile:
    writer = csvwriter(csvoutfile, lineterminator='\n', delimiter=',', quotechar='"',
                        escapechar='\\', doublequote=False, quoting=QUOTE_NONE, strict=True)
    index = 0
    for x in oldUrls:
        try:
            writer.writerow([oldUrls[index],oldUrlCount[index],newUrls[index],newUrlCount[index]])
        except:
            writer.writerow([x, "failed"])
        index += 1
