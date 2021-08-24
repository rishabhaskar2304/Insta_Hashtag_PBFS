from collections import deque
import re,openpyxl,os,requests,json

#Function to make API calls
def makeApiCall( url , endPointParams) :

    data = requests.get(url , endPointParams)
    response = {}
    response['url'] = url
    response['endpoint_params'] = endPointParams
    response['json_data'] =  json.loads(data.content)
    return response

#Function to get id of a hashtag
def hstinfo(params):
    endpointParams={}
    endpointParams['user_id']=params['insta_id']
    endpointParams['q']=params['hashtag_name']
    endpointParams['fields']='id'
    endpointParams['access_token']=params['access_token']

    url = params['endpoint_base'] + 'ig_hashtag_search'

    return makeApiCall(url,endpointParams)

#Function to get Top Media of a hashtag
def hashtopmedia(params):
    endpointParams={}
    endpointParams['user_id']=params['insta_id']
    endpointParams['fields']='caption'
    endpointParams['access_token']=params['access_token']

    url = params['endpoint_base'] + params['hashtag_id'] + '/top_media'

    return makeApiCall(url,endpointParams)

#Initializing openpyxl object
pth = os.path.dirname(__file__)
wb = openpyxl.Workbook()
sheet = wb.active

params = {}
#Enter your app details
params['access_token'] = ''
params['graph_domain'] = 'https://graph.facebook.com/'
params['graph_version'] = 'v11.0'
params['endpoint_base'] = params['graph_domain'] + params['graph_version'] + '/'
params['insta_id'] = ''               

#Regular expression for segregating hashtags out of whole caption
hs = re.compile(r'#\w+')

q = deque()
target = input("Enter the parent hashtag : ")
q.append(target)
vis = {}
encntr = []
#You can increase or decrease this variable based on you Graph API limit
api_call_limit = 1

while(api_call_limit and q.__len__()>0) :
    params['hashtag_name'] = q.popleft()
    if(params['hashtag_name'] in vis) :
        continue
    v = []
    vis[params['hashtag_name']] = True

    #Request id of  hashtag and then request top media of the hashtag
    hstinforesp = hstinfo(params)
    params['hashtag_id'] = hstinforesp['json_data']['data'][0]['id']
    hashtoprep = hashtopmedia(params) 

    #Search for hashtags in the caption
    for cpt in hashtoprep['json_data']['data']:
        s = hs.findall(cpt['caption'])
        v.append(s)
    #Incrementing number of occurences of a hashtag
    d = {}
    for vt in v:
        for it in vt:
            if(it not in d):
                d[it]=1
            else:
                d[it]+=1
    dl = list(d.items())
    #Sort the tuples nodes of hashtags based on decreasing order of occurences
    dl.sort(key= lambda x: x[1], reverse=True)
    for i in dl:
        q.append(i[0])
        encntr.append(i)
    #Decrease the number of requests left
    api_call_limit-=1

#Entering hashtags and their occurences in Excel files in decreasing order
x=1
for i in encntr:
    sheet.cell(row=x , column=1).value = i[0]
    sheet.cell(row=x , column=2).value = i[1]
    x += 1
wb.save(r"{}/bfs_hashtags.xlsx".format(pth))
