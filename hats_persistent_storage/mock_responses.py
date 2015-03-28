import json

MOCK_DEVICE_BLOB = '{"state": "on", "manufacturer": "Cyberdyne Systems LTD"}'
MOCK_HOUSE_BLOB = '{"nickname": "The Apartment", "address": "221B Baker St"}'
def getMockResponse(query):
    if query == 'HD' or query == 'RD':
        return json.dumps([{'device-id':'G7Umyvw7cUyxYx9ezuPLDw', 'device-type':'light', 'blob':MOCK_DEVICE_BLOB}, 
                           {'device-id':'nzqnOd3DikipN8spJxE5nQ', 'device-type':'stereo', 'blob':MOCK_DEVICE_BLOB}, 
                           {'device-id':'5CILH42iOU2qF1DiHCLEjg', 'device-type':'thermostat', 'blob':MOCK_DEVICE_BLOB}, 
                           {'device-id':'olnQYPjfJUyijwhY71sxQw', 'device-type':'light', 'blob':MOCK_DEVICE_BLOB}])
    elif query == 'RT' or query == 'RD':
        return json.dumps([{'device-id':'G7Umyvw7cUyxYx9ezuPLDw', 'device-type':'light', 'blob':MOCK_DEVICE_BLOB},
                           {'device-id':'olnQYPjfJUyijwhY71sxQw', 'device-type':'light', 'blob':MOCK_DEVICE_BLOB}])
    elif query == 'HI':
        return json.dumps({'version':0, 'blob':MOCK_HOUSE_BLOB})
    elif query == 'UI':
        return json.dumps({'user-id': 'bsaget', 'user-full-name': 'Bob Saget'})
    elif query == 'AL' or query == 'AT' or query == 'CI' or query == 'CT' or query == 'CI':
        return json.dumps([{'time':'2015-03-27T21:07:46Z', 'blob':'light-on'}, 
                           {'time':'2015-03-27T21:07:49Z', 'blob':'light-off'}, 
                           {'time':'2015-03-27T21:07:50Z', 'blob':'light-on'}, 
                           {'time':'2015-03-27T21:07:41Z', 'blob':'light-off'}])
    else:
        return json.dumps({'fake-attribute':'fake-data'})
