import requests
import time

# 0. Configuration stuff

# 0.1 It's not recommended, but the simplest way to authenticate is to use an API key
# Generate one here: https://cloud.google.com/docs/authentication/api-keys
apikey = "ENTER KEY HERE"

# 0.2 Upload into a bucket in Google Cloud Storage:
# https://console.cloud.google.com/storage
# Format is: gs://[bucket name]/[filename]
fileurl = "gs://cloud-samples-tests/speech/brooklyn.flac"

transcriptdestination = "transcript.json"

payload = {
    "config": {
        "encoding": "FLAC",
        "sampleRateHertz": 16000, # 0.3 Server will throw INVALID ARGUMENT response if it detects this is wrong
        "languageCode": "en-US",
        "enableAutomaticPunctuation": "true",
        "enableWordTimeOffsets": "true",
        "useEnhanced": "true",
        "model": "video" # 0.4 phone_call, video, command_and_search, or default
    },
    "audio": {
        "uri": fileurl
    }
}



# 1. Initiate long-running transcription job and get job name
apipoint = "https://speech.googleapis.com/v1p1beta1/speech:longrunningrecognize?key="+apikey
r1 = requests.post(apipoint, json=payload)
print r1.json()    # If this crashes you can still retrieve the job manually
retrievalname = r1.json()["name"]
retrievedataurl = "https://speech.googleapis.com/v1p1beta1/operations/"+retrievalname+"?key="+apikey


# 2. Periodically poll server to see if transcript is ready
timeelapsed = 0
pollinginterval = 10

while True:
    r2 = requests.get(retrievedataurl)
    # print r2.json()
    if "progressPercent" in r2.json()["metadata"]:
        if r2.json()["metadata"]["progressPercent"] == 100:
            break
        else:
            print "Progress: " +str(r2.json()["metadata"]["progressPercent"]) +"%"
    time.sleep(pollinginterval)
    timeelapsed = timeelapsed + pollinginterval
    print "Time elapsed: " + str(timeelapsed) + "s"

print r2.json()

with open(transcriptdestination, 'w') as f:
    f.write(r2.content)
