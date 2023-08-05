from pprint import pprint
import requests
from version import __version__, __branch__


VERSION = __version__
if __branch__ != 'main':
    VERSION += '+'+__branch__

PROJECT_ID = "30449210"
URL_1 = 'https://gitlab.com/api/v4/projects/'+PROJECT_ID+'/packages'
TOKEN = 'glpat-tfz1WBmYJuPUBc_CqMWy'

response_packages = requests.get(url=URL_1, headers={'PRIVATE-TOKEN': TOKEN})
pprint(response_packages.json())
print("version de la branche : ", VERSION)

print("nombre de versions déployées : ", len(response_packages.json()))

for k in range(len(response_packages.json())):
    response = response_packages.json()[k]
    print(response["version"])
    if response["version"] == VERSION:
        ID = response['id']
        URL_2 = '/'+str(ID)
        response_package_files = requests.get(url=URL_1+URL_2, headers={'PRIVATE-TOKEN': TOKEN})
        print("URL = ", URL_1+URL_2)
        pprint(response_package_files.json())
        r = requests.delete(url=URL_1+URL_2, headers={'PRIVATE-TOKEN': TOKEN})
        print("ERREUR ? ", r.status_code, r.reason)
