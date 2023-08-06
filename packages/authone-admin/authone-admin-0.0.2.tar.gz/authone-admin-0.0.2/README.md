# AuthOne-Python
AuthOne Python SDK

```bash
pip install authone-admin
```


## Quick Start

```python
from authone import AuthOne


auth = AuthOne(app_id, app_secret='<YOUR_APP_SECRET>')

auth.Token.validate('DID_TOKEN')

# Read the docs to learn more!
```
