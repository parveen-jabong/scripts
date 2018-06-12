import requests,json

jt_url_temp = 'https://www.jabong.com/find/{TERM}/?jsondump=1'
headers = {}
headers['Accept'] = 'application/json'
headers['Content-type'] = 'application/json'
headers['postman-token'] = 'ca64e43a-1444-41bf-099e-f604ac515b52'
headers['x-mynt-ctx'] = 'storeid=4603'

file = open('golden_search_terms', 'r')
golden_terms = file.readlines()
file.close

op = open('golden_terms_counts', 'w', 0)

for term in golden_terms:
    golden_term = term.strip()
    retry = 0
    while retry == 0 or retry == 1:
        try:
            jt_url = jt_url_temp.replace("{TERM}", golden_term.replace(" ", "-"))
            jt_res = requests.get(jt_url)
            jt_count = json.loads(jt_res.text)[0]['APIResponse']['data']['summary']['productCnt']

            op.write(golden_term + "," + str(mt_count) + "," + str(jt_count) + "\n")
            retry = -1
        except:
            retry += 1
            if retry == 2:
                op.write(golden_term + ",-1,-1\n")
