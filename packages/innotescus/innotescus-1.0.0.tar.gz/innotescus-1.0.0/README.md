# Innotescus Python Client

A small python library for interacting with the Innotescus API
from python 3.8+.

## Development

Create a virtual environment, and install the application dependencies.

```shell
python3.8 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Rebuild Protobuf Files

```shell
make grpc
```

This will read the latest protobuf files from Innotescus.Schema,
and place generated code into **src/innotescus/_grpc**.

#### IMPORTANT NOTE FOR ARM64-BASED MACS

If you're developing on Apple Silicon machines, the above command
will likely fail, with the following error message (full paths removed
for brevity).

```shell
make grpc
ImportError: dlopen(.../_protoc_compiler.cpython-310-darwin.so, 0x0002):
  tried: '.../_protoc_compiler.cpython-310-darwin.so'
  (mach-o file, but is an incompatible architecture (have 'x86_64', need 'arm64e')),
  '/usr/lib/_protoc_compiler.cpython-310-darwin.so' (no such file)
make: *** [grpc] Error 1
```

This can be worked-around by instructing the build to run under x86_64
by running the arch command (**note** this is unique macos behavior,
as far as I'm aware).

```shell
arch -x86_64 make grpc

### OR ###

export ARCHPREFERENCE=x86_64
make grpc
```

### Uploading to PYPI from a CI/CD Job

```shell
# if the build agent doesn't autogen a venv
python3.8 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

TWINE_USERNAME=me TWINE_PASSWORD=t3hp@ssw0rd make upload
```

### Config Reference

| Config File Attribute     | Env Var                       | default                                   | description                                       |
| ----                      | ----                          | ----                                      | ----                                              |
|                           | INNO_CONFIG                   |                                           | File path for addition .ini config                |
| server_url                | INNO_SERVER_URL               | innotescus.app                            | Innotescus API domain name                        |
| port                      | INNO_PORT                     | 443                                       | Innotescus API port                               |
| auth_domain               | INNO_AUTH_DOMAIN              | auth.innotescus.app                       | Domain for OAuth2 requests                        |
| audience                  | INNO_AUDIENCE                 | https://innotescus-prod.auth0.com/api/v2/ | OAuth2 Audience                                   |
| scope                     | INNO_SCOPE                    |                                           | OAuth2 Scope                                      |
| ssl_verification          | INNO_SSL_VERIFICATION         | Yes                                       | Validate TLS Cert validity when making requests   |
| force_insecure_channel    | INNO_FORCE_INSECURE_CHANNEL   | No                                        | When true, make requests to API without TLS (must be to localhost) |
| client_id                 | INNO_CLIENT_ID                |                                           | Innotescus API Client ID (see: admin)             |
| client_secret             | INNO_CLIENT_SECRET            |                                           | Innotescus API Client Secret (see: admin)         |
|                           | INNO_IS_TEST                  |                                           | If set to any value, tells Innotescus this is a test run (so skip things like version checks) |


### Example Config File for Local Development

These are my local development settings (not using the envoy proxy).

```ini
[innotescus]
server_url = localhost
port = 9091
auth_domain = login.innotescus.app
audience = https://innotescus.auth0.com/api/v2/
ssl_verification = No

force_insecure_channel = Yes
client_id = <<NEED TO MAKE THIS FROM ADMIN>>
client_secret = <<NEED TO MAKE THIS FROM ADMIN>>
```
