from queue import Queue
import re,openpyxl,os,requests,json,sys

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
    endpointParams['fields']='caption,like_count'
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

q = Queue()
target = input("Enter the parent hashtag : ")
q.put(target)
vis = {}
encntr = []
#You can increase or decrease this variable based on you Graph API limit
api_call_limit = 2

while(api_call_limit and not q.empty()) :
    sz = q.qsize()
    brdth_dct = {}
    mnlk = 999999999
    mxlk = 0
    mxoc = 0
    for itd in range(sz):    
        params['hashtag_name'] = q.get()
        if(params['hashtag_name'] in vis) :
            continue
        print("Requesting data for ",params['hashtag_name'])
        v = []
        vis[params['hashtag_name']] = True

        #Request id of  hashtag and then request top media of the hashtag
        hstinforesp = hstinfo(params)
        params['hashtag_id'] = hstinforesp['json_data']['data'][0]['id']
        hashtoprep = hashtopmedia(params) 

        #Search for hashtags in the caption
        rank_in_top_media = 1
        for cpt in hashtoprep['json_data']['data']:  
            try: 
                s = hs.findall(cpt['caption'])
                for i in s:
                    if(i not in brdth_dct):
                        brdth_dct[i] = [0,0,50,0.0]
                    brdth_dct[i][0]+=1
                    mxoc = max(brdth_dct[i][0],mxoc)
                    try:
                        brdth_dct[i][1]+=int(cpt['like_count'])
                        mnlk = min(mnlk,int(cpt['like_count']))
                        mxlk = max(mxlk,brdth_dct[i][1])
                    except:
                        pass
                    brdth_dct[i][2]=min(rank_in_top_media,brdth_dct[i][2])
            except:
                pass
            rank_in_top_media+=1
            v.append(s)
        
        for hsh, vct in brdth_dct.items():
            #Some posts don't show their likes so we will set their likes to minimum encountered likes of a post xDDD
            vct[1] = mnlk*vct[0]
            #Setting priority rating for the hashtag based on net likes, number of occurences and minimum rank in the top media
            vct[3]+= float(vct[0]/mxoc) + float(vct[1]/mxlk) + 1.0 - float(vct[2]/25) 
        
        dl = list(brdth_dct.items())
        #Sort the tuples nodes of hashtags based on decreasing order of priority rating
        dl.sort(key = lambda x: x[1][3], reverse=True)
        
        for i in dl:
            q.put((i[0])[1:])
            encntr.append(i)
        #Decrease the number of requests left
        api_call_limit-=1
        if(api_call_limit==0):
            break

#Entering hashtags and their occurences in Excel files in decreasing order
sheet.cell(row=1 , column=1).value = 'Hashtags'
sheet.cell(row=1 , column=2).value = 'No. of occurrences'
sheet.cell(row=1 , column=3).value = 'Total no. of likes on associated posts'
sheet.cell(row=1 , column=4).value = 'Minimum rank in top media of whole breadth'
sheet.cell(row=1 , column=5).value = 'Priority rating'
x=2
for i in encntr:
    sheet.cell(row=x , column=1).value = i[0]
    sheet.cell(row=x , column=2).value = i[1][0]
    sheet.cell(row=x , column=3).value = i[1][1]
    sheet.cell(row=x , column=4).value = i[1][2]
    sheet.cell(row=x , column=5).value = i[1][3]
    x += 1
wb.save(r"{}/bfs_hashtags.xlsx".format(pth))
