from gcloud import storage
import time
import requests
import json
api_key='INSERT API KEY HERE'
client = storage.Client()
bucket = client.get_bucket('INSERT BUCKET HERE')
blob = bucket.blob('audio.flac')
print('A fazer o upload do ficheiro')
blob.upload_from_filename('2.flac')
blob.make_public()
url = 'https://speech.googleapis.com/v1/speech:longrunningrecognize?key={}'.format(api_key)
payload = json.load(open("request.json"))
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
r = requests.post(url, data=json.dumps(payload), headers=headers)
a=json.loads(r.text)['name']
print('Instancia criada com o numero {}'.format(a))
def req(a):
    return requests.get('https://speech.googleapis.com/v1/operations/{}?key={}'.format(a,api_key))
r=req(a)
output_file=open('results.txt', 'w')
response=json.loads(r.text)
print(response)
while(('response'  not in response)):
    r=req(a)
    if json.loads(r.text) != response:
        response=json.loads(r.text)
        if 'progressPercent' in response['metadata']:
            print('Percentagem: {}%'.format(response['metadata']['progressPercent']))
        else:
            print(response)
    time.sleep(5)
print('Guardando o ficheiro')
for results in response['response']['results']:
    output_file.write(results['alternatives'][0]['transcript'].encode('utf-8')+'\n')
output_file.close()
print('Sucesso')
