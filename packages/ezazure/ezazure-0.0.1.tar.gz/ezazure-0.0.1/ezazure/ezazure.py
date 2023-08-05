"""Easy Azure interface for uploading and downloading files"""

from __future__ import annotations

from os import listdir, remove
from os.path import basename, dirname, expanduser, isfile, join
import re

from azure.storage.blob import (
    BlobClient,
    BlobServiceClient,
    ContainerClient,
    ContentSettings,
)
import yaml


class Azure:
    """Easy Azure interface for uploading/downloading files

    Parameters
    ----------
    config_fname: str, optional, default='.ezazure'
        Configuration file, containing your azure connection string (which can
        be the actual connection string, or the name of a file that contains
        your connection string) and your azure container. Example:

        .. code-block:: yaml

           connection_str: ~/secrets/azure
           container: litmon-private

        :code:`container` is only the default storage container, and can be
        overwritten in the :meth:`upload` and :meth:`download` functions.

    Attributes
    ----------
    client: azure.storage.blob.BlobServiceClient
        Client for interfacing with Azure
    """
    def __init__(self, /, config_fname: str = '.ezazure'):

        # load configuration
        try:

            # load config from file
            config = yaml.safe_load(open(config_fname, 'r'))

            # get connection string
            connection_str = config['connection_str']

            # get default container
            self._container = config['container']

        # missing / improperly formatted file
        except (FileNotFoundError, KeyError):
            raise RuntimeError(
                f'ezazure.Azure() requires a {config_fname} file that '
                'contains your connection parameters. See the documentation '
                'for required fields.'
            )

        # load connection str from file
        if 'AccountKey' not in connection_str:
            connection_str = expanduser(connection_str)
            try:
                connection_str = \
                    open(connection_str, 'r').read().strip()
            except FileNotFoundError:
                raise FileNotFoundError(
                    'Unable to read Azure connection string from '
                    f'{connection_str}.'
                )

        # extract account name
        self._account = \
            re.search(r'AccountName=([^;]*);', connection_str).group(1)

        # connect to Azure
        self.client = BlobServiceClient.from_connection_string(connection_str)

    def download(
        self,
        /,
        file: str,
        *,
        container: str = None,
        regex: bool = False,
        replace: bool = False,
    ):
        """Download file from Azure

        Parameters
        ----------
        file: str
            file to download
        container: str, optional, default=None
            if supplied, download from this container (instead of default
            container listed in :code:`.ezazure`)
        regex: bool, optional, default=False
            treat :code:`file` as a regex expression. download all files that
            match. all files will be downloaded to the same directory.
        replace: bool, optional, default=False
            if :code:`dest/file` exists locally, then skip the download
        """

        # process regular expresion
        if regex:

            # download each file that matches pattern
            [
                self.download(
                    file=join(dirname(file), _file),
                    container=container,
                    regex=False,
                    replace=replace,
                )
                for _file in self._get_listing(container=container)[0]
                if re.search(file, join(dirname(file), _file)) is not None
            ]

            # return to stop processing
            return

        # check if file exists
        if not replace and isfile(file):
            return

        # get default container
        if container is None:
            container = self._container

        # connect to Azure
        client: BlobClient = self.client.get_blob_client(
            container=container,
            blob=basename(file)
        )

        # download file
        with open(file, 'wb') as f:
            f.write(client.download_blob().readall())

    def upload(
        self,
        /,
        file: str,
        *,
        container: str = None,
        regex: bool = False,
        replace: bool = True,
        update_listing: bool = True,
    ):
        """Upload file to Azure

        Parameters
        ----------
        file: str
            file to upload. This file will be uploaded as
            :code:`basename(file)`. (I.e. it will NOT be uploaded to a
            directory within the container, but rather to the container root
            level.)
        container: str, optional, default=None
            if supplied, download from this container (instead of default
            container listed in :code:`.ezazure`)
        regex: bool, optional, default=False
            treat :code:`file` as a regex expression. upload all files that
            match. all files must be in the same directory.
        replace: bool, optional, default=True
            replace existing file on server if it exists
        update_listing: bool, optional, default=True
            if True, and if there is public access to :code:`container`, then
            update directory listing (with :meth:`_update_listing`) after
            uploading
        """

        # process regular expresion
        if regex:

            # upload each file that matches pattern
            [
                self.upload(
                    file=join(dirname(file), _file),
                    container=container,
                    regex=False,
                    replace=replace,
                    update_listing=False,
                )
                for _file in listdir(dirname(file))
                if re.search(file, join(dirname(file), _file)) is not None
            ]

            # update listing
            if update_listing:
                self._update_listing(container=container)

            # return to stop processing
            return

        # get default container
        if container is None:
            container = self._container

        # connect to Azure
        client: BlobClient = self.client.get_blob_client(
            container=container,
            blob=basename(file),
        )

        # delete existing
        if client.exists():
            if replace:
                client.delete_blob()
            else:
                return

        # check if is html file
        if basename(file).rsplit('.')[-1] == 'html':
            content_settings = ContentSettings(content_type='text/html')
        else:
            content_settings = None

        # upload file
        with open(file, 'rb') as data:
            client.upload_blob(
                data,
                content_settings=content_settings,
            )

        # update directory listing
        if update_listing:
            self._update_listing(container=container)

    def _get_listing(
        self,
        /,
        *,
        container: str = None
    ) -> tuple(list[str], bool):
        """Get list of files on server

        Parameters
        ----------
        container: str, optional, default=None
            if supplied, download from this container (instead of default
            container listed in :code:`.ezazure`)

        Returns
        -------
        list[str]
            list of files
        bool
            whether container has public access
        """

        # get default container
        if container is None:
            container = self._container

        # generate client
        client: ContainerClient = self.client.get_container_client(
            container=container,
        )

        # check public access
        public_access = \
            client.get_container_properties()['public_access'] is not None

        # get file list
        return [file['name'] for file in client.list_blobs()], public_access

    def _update_listing(
        self,
        /,
        *,
        container: str = None,
        fname: str = 'directory.html'
    ):
        """Update the directory listing for the current container

        This creates a simple html page that provides links to all files in the
        container.

        If the container has no public access, then this function will do
        nothing.

        Parameters
        ----------
        container: str, optional, default=None
            if supplied, download from this container (instead of default
            container listed in :code:`.ezazure`)
        fname: str, optional, default='directory.html'
            filename for directory listing
        """

        # get default container
        if container is None:
            container = self._container

        # get file list
        files, public_access = self._get_listing(container=container)

        # skip if no public access
        if not public_access:
            return

        # create html page
        container_url = \
            f'https://{self._account}.blob.core.windows.net/{container}'
        with open(fname, 'w') as fid:
            for file in files:
                if file == fname:
                    continue
                print(
                    f'<a href={container_url}/{file}>{file}</a><br>',
                    file=fid,
                )

        # upload directory listing
        self.upload(
            fname,
            container=container,
            replace=True,
            update_listing=False
        )

        # clean up
        remove(fname)
