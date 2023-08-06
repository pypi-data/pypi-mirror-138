## Asklora module for ingestion data
- using credetials from json file
```python
import asklora

portal = asklora.Portal()
# example from json file
portal.set_credentials_from_json("creds.json")

# get rkd client
rkd = portal.get_rkd_client()

# get quote data
aapl =rkd.get_quote("AAPL.O",df=True)
```
- using credentials from secret key
```python
import asklora

portal = asklora.Portal()

# example from secret key
portal.set_credentials_from_secret(secret)

# get rkd client
rkd = portal.get_rkd_client()

# get quote data
aapl =rkd.get_quote("AAPL.O",df=True)
```