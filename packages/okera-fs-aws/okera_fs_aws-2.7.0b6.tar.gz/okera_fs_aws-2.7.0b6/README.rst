okera_fs_aws
============

Okera access control for AWS S3 CLI v1

Dependencies
------------

Required:

-  Python 2,7, 3.6+

-  AWS CLI v1 for Python 2,7, 3.6+

-  ``jwt``, ``requests``, ``pytz``, ``urllib3``, ``pathlib``

.. code:: shell

    pip3 install jwt requests pytz urllib3 pathlib

Installation
------------

.. code:: shell

    pip3 install okera_fs_aws

To verify:

.. code:: python

    >>> import okera_fs_aws
    >>> okera_fs_aws.version()
    '##OKERA_RELEASE_VERSION##'

Configuration
-------------

If ~/.aws/config does not exist the user should create it by running aws configure.  The values assigned to access and secret key configurations will not effect the use of the okera_fs_aws plugin.  The 'plugins' definition below indicates the AWS CLI should load the 'okera_fs_aws' python module found on it's sys.path.  The [profile okera] section parameterizes the Okera CLI plugin.  There are two additional, optional parameters of the okera profile.  The token_source value can be set to 'authserver'.  The mode value can be set to 'proxy' when the Access Proxy service operates in proxy mode.

Example of the okera_fs updates to ~/.aws/config
::

    [profile okera]
    okera =
        proxy = https://<CDAS Access Proxy service host>:5010
        rest = https://<CDAS REST server host>:8083
        token = <User's JWT token>

    [plugins]
    okera = okera_fs_aws

Usage
-----

.. code:: shell

    aws s3 <command> --profile okera
