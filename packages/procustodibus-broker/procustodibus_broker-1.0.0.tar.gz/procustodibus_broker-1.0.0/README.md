Pro Custodibus Broker
=====================

[Pro Custodibus](https://www.procustodibus.com/) is a service that makes [WireGuard](https://www.wireguard.com/) VPNs easy to deploy and manage.

To integrate Pro Custodibus with your own SIEM or other log tools, you can run the Pro Custodibus broker on one of your own internal hosts, and the broker will pull alerts and other events from Pro Custodibus and push them to your own security management systems.


Installing
----------

Requires python 3.8 or newer and libsodium. Installer script can install requirements, plus the broker itself, on most linuxes. Install from source like the following:
```
./install.sh --install
```

Or run it like the following to see more options:
```
./install.sh --help
```

See the [Installer Documentation](https://docs.procustodibus.com/guide/integrations/brokers/#install) for full details.


Development
-----------

### Set up dev env

1. Create a virtualenv with [pyenv](https://github.com/pyenv/pyenv):
```
pyenv virtualenv 3.8.12 procustodibus-broker
```

2. Activate the virtualenv:
```
pyenv local procustodibus-broker 3.8.12 3.9.10 3.10.2
```

3. Install tox:
```
pip install tox
```

4. Install pre-commit and pre-push hooks:
```
tox -e pre-commit install
tox -e pre-commit install -- -t pre-push
```

### Dev tasks

List all tox tasks you can run:
```
tox -av
```

Run unit tests in watch mode:
```
tox -e watch
```

Run all (docker-based) installer tests:
```
docker-compose -f test_install/docker-compose.yml build --pull
tox -e py38 test_install
```

Manually run pre-push hook on all version-controlled files:
```
tox -e pre-commit run -- -a --hook-stage push
```


Resources
---------

* Home page: https://www.procustodibus.com/
* Documentation: https://docs.procustodibus.com/guide/integrations/brokers/
* Changelog: https://docs.procustodibus.com/guide/integrations/brokers/#changelog
* Issue tracker: https://todo.sr.ht/~arx10/procustodibus-broker
* Source code: https://git.sr.ht/~arx10/procustodibus-broker


License
-------

[The MIT License](https://git.sr.ht/~arx10/procustodibus-broker/tree/main/LICENSE)
