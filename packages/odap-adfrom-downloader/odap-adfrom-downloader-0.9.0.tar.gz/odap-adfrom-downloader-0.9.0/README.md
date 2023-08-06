# DataSentics Python package for downloading adform data

**This package is distributed under the "DataSentics SW packages Terms of Use." See [license](https://github.com/DataSentics/odap-ga-downloader/blob/main/LICENSE)**

## Downloads data from adform in zip files

You need to specify:
  * Credentials (name, setup_id, client_id, secret)
  * Optionally you can specify scope, which data from Adform you would like to download, dates and file directory

```bash
$ pip install adform-downloader

from adform.Client import Client, FilePersistingHandler
from adform.Credentials import Credentials

setup_id = ""
client_id = ""
client_secret = ""

# optionally can be added into credentials. Written with default values
file = "/tmp/" # for state file
scopes = [
        "https://api.adform.com/scope/buyer.masterdata",
        "https://api.adform.com/scope/eapi",
        "https://api.adform.com/scope/buyer.rtb.lineitem",
    ]
tables = ["Click", "Event", "Impression", "Trackingpoint", "meta"]
start_day=today-8days, # format dd-mm-yyyy
end_day=today,
landing_file = "/tmp/" # for data, can be same as file

persisting_handler = FilePersistingHandler(location=file)
credentials = Credentials(setup_id=setup_id, client_id=client_id, client_secret=client_secret)
client = Client(credentials, persisting_handler)
client.download_masterdata_files_by_id()
```
