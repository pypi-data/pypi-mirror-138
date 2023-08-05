from paramiko import SSHClient, AutoAddPolicy
from paramiko.ssh_exception import BadHostKeyException, AuthenticationException, SSHException
import logging
import socket
import os
from datetime import datetime
import uuid

logger = logging.getLogger("Main")
BUFSIZE = 10*1024
WRITETEST = str(uuid.uuid4())


class HmcClient:
    """Client to interact with HMC"""

    def __init__(self, host, user, outDir, password=None, ssh_key=None, connect=True):
        logger.debug(f'HMC: {user}@{host}, outDir: {outDir}, password: {password is not None}, ssh_key: {ssh_key is not None}, connect: {connect}')

        self.host       = host
        self.user       = user
        self.password   = password
        self.ssh_key    = ssh_key
        self.outDir     = outDir
        self.validDir   = False
        self.client     = None

        if connect:
            self.client     = self._connect()
            try:
                os.mkdir(outDir)
            except FileExistsError:
                if not os.path.isdir(outDir):
                    logger.error(f'File {outDir} exists and it is not a directory')
                    return
            except OSError:
                logger.error(f'Can not create directory {outDir}')
                return
            with open(os.path.join(outDir, WRITETEST), 'wt') as file:
                try:
                    file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    self.validDir = True
                except Exception as e:
                    logger.error(f'Can not write into {outDir}')
                    return
            os.remove(os.path.join(outDir, WRITETEST))
        else:
            # Do nothing!
            pass


    def _connect(self):
        if self.ssh_key is not None:
            logger.debug(f'{self.user}@{self.host}: try connection with ssh key only')
            client = self._try_to_connect(None, self.ssh_key)
            if client is not None:
                return client
        logger.debug(f'{self.user}@{self.host}: try connection with password only')
        client = self._try_to_connect(self.password, None)
        if client is not None:
            logger.error(f'{self.user}@{self.host}: connection failed')
        return client

    
    def _try_to_connect(self, password, ssh_key):
        logger.debug(f'Start connection: {self.user}@{self.host}, password:{password is not None}, ssh_key: {ssh_key}')
        try:
            client = SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(
                    self.host,
                    username=self.user,
                    password=password,
                    key_filename=ssh_key,
                    look_for_keys=True,
                )
            logger.debug(f'Connected to {self.user}@{self.host}')
        except 	BadHostKeyException as exc:
            logger.error(f'{self.user}@{self.host}: server’s host key could not be verified: {exc}')
            return None
        except AuthenticationException as exc:
            logger.error(f'{self.user}@{self.host}: authentication error: {exc}')
            return None
        except SSHException as exc:
            logger.error(f'{self.user}@{self.host}: SSH error: {exc}')
            return None
        except socket.error as exc:
            logger.error(f'{self.user}@{self.host}: socket error: {exc}')
            return None
        except Exception as exc:
            logger.error(f'{self.user}@{self.host}: unexpected error: {exc}')
            return None

        logger.debug(f'{self.user}@{self.host}: connection is successful')
        return client


    def isConnected(self):
        return self.client != None


    def close(self):
        if self.client is not None:
            self.client.close()
            logger.debug('Connection closed')
        else:
            logger.debug('Connection was not open')
        self.client = None


    def runCommand(self, command, fileName):
        if self.client is None:
            logger.error('Client was not connected. Command not executed')
            return

        if not self.validDir:
            logger.error('No valid output dir. Command not executed')
            
        try:
            logger.debug(f'{command} -> {fileName}')
            transport = self.client.get_transport()
            session = transport.open_session()
            session.set_combine_stderr(True)
            with open(os.path.join(self.outDir, fileName), 'wb') as file:
                session.exec_command('LANG=C ' + command)

                data = session.recv(BUFSIZE)
                while len(data) > 0:
                    file.write(data)
                    data = session.recv(BUFSIZE)
            rc = session.recv_exit_status()
            logger.debug(f'Return code: {rc}')
            #if rc != 0:
            #    logger.warning(f'RC={rc} for {self.user}@{self.host}:{command}')

        except SSHException as exc:
            logger.error(f'SSH error: {exc}')
            return
        except (OSError, IOError) as e:
            logger.error(f'I/O error: {e}')
