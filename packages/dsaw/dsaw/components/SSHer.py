# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from RemoteAccess import RemoteAccess as base, RemoteAccessError

class SSHer(base):

    class Inventory(base.Inventory):

        import pyre.inventory
        #auth_sock = pyre.inventory.str( 'auth_sock')
        known_hosts = pyre.inventory.str( 'known_hosts' )
        private_key = pyre.inventory.str( 'private_key' )
        pass # end of Inventory
    

    def __init__(self, name='ssher', facility='remoteaccess'):
        base.__init__(self, name=name, facility=facility)
        return


    def copyfile(self, server1, path1, server2, path2):
        'copy from server1 to server2'
        if not _localhost(server1) and not _localhost(server2):
            return self._copyfile_rr(server1, path1, server2, path2)
        if _localhost(server1) and _localhost(server2):
            import shutil
            shutil.copy(path1, path2)
        if _localhost(server1): self._copyfile_lr(path1, server2, path2)
        if _localhost(server2): self.getfile(server1, path1, os.path.split(path2)[0] or '.')
        return
    

    def pushdir( self, path, server, remotepath ):
        '''push a local directory to remote server

    Eg:
        pushdir('/a/b/c', server1, '/a1/b1'): directory /a/b/c will be copied to server1 and become /a1/b1/c
        '''

        if not os.path.exists(path): raise IOError, "%s does not exist" % path
        
        address = server.address
        port = server.port
        username = server.username
        known_hosts = self.inventory.known_hosts
        private_key = self.inventory.private_key

        # tar -czf - <sourcepath> | ssh <remotehost> "(cd <remotepath>; tar -xzf -)"
        pieces = [
            'tar',
            '-czf',
            '-',
            path,
            '|',
            'ssh',
            "-o 'StrictHostKeyChecking=no'",
            ]

        if port:
            pieces.append( '-p %s' % port )

        if known_hosts:
            pieces.append( "-o 'UserKnownHostsFile=%s'" % known_hosts )
        
        if private_key:
            pieces.append( "-i %s" % private_key )
            
        pieces += [
            '%s@%s' % (username, address),
            '"(cd %s; tar -xzf -)"' % remotepath,
            ]

        cmd = ' '.join(pieces)
        
        self._info.log( 'execute: %s' % cmd )

        failed, output, error = spawn( cmd )
        if failed:
            msg = '%r failed: %s' % (
                cmd, error )
            raise RemoteAccessError, msg
        return


    def getfile( self, server, remotepath, localdir ):
        'retrieve file from remote server to local path'
        address = server.address
        port = server.port
        username = server.username
        known_hosts = self.inventory.known_hosts
        private_key = self.inventory.private_key
        
        pieces = [
            'scp',
            "-o 'StrictHostKeyChecking=no'",
            ]
        
        if port:
            pieces.append( '-P %s' % port )

        if known_hosts:
            pieces.append( "-o 'UserKnownHostsFile=%s'" % known_hosts )
        
        if private_key:
            pieces.append( "-i %s" % private_key )
            
        pieces += [
            '%s@%s:%s' % (username, address, remotepath),
            '%s' % localdir,
            ]

        cmd = ' '.join(pieces)
        self._info.log( 'execute: %s' % cmd )

        failed, output, error = spawn( cmd )
        if failed:
            msg = '%r failed: %s' % (
                cmd, error )
            raise RemoteAccessError, msg

        remotedir, filename = os.path.split( remotepath )
        return os.path.join( localdir, filename )


    def getdir( self, server, remotepath, localdir ):
        'retrieve a directory from remote server to local path'
        return self.getfile(server, remotepath, localdir)


    def execute( self, cmd, server, remotepath, suppressException = False ):
        'execute command in the given directory of the given server'

        address = server.address
        port = server.port
        username = server.username
        known_hosts = self.inventory.known_hosts
        private_key = self.inventory.private_key

        rmtcmd = 'cd %s && %s' % (remotepath, cmd)
        
        pieces = [
            'ssh',
            "-o 'StrictHostKeyChecking=no'",
            ]
        
        if port:
            pieces.append( '-p %s' % port )

        if known_hosts:
            pieces.append( "-o 'UserKnownHostsFile=%s'" % known_hosts )

        if private_key:
            pieces.append( "-i %s" % private_key )
            
        pieces += [
            '%s@%s' % (username, address),
            '"%s"' % rmtcmd,
            ]

        cmd = ' '.join(pieces)

        self._info.log( 'execute: %s' % cmd )
        failed, output, error = spawn( cmd )
        if failed and not suppressException:
            msg = '%r failed: %s' % (
                cmd, error )
            raise RemoteAccessError, msg
        return failed, output, error


    def _copyfile_rr(self, server1, path1, server2, path2):
        'push a remote file to another remote server'
        if server1 == server2:
            pieces = [
                'cp',
                path1,
                path2,
                ]
        elif _tunneled_remote_host(server1) or _tunneled_remote_host(server2):
            raise NotImplementedError, 'server1: %s, server2: %s' % (server1, server2)
        else:
            address2 = server2.address
            port2 = server2.port
            username2 = server2.username

            pieces = [
                'scp',
                ]
            if port2:
                pieces.append('-P %s' % port2)
            pieces.append(' %s' % path1)
            pieces.append('%s@%s:%s' % (username2, address2, path2))
            

        cmd = ' '.join(pieces)
        
        self.execute(cmd, server1, '')
        return
    

    def _copyfile_lr( self, path, server, remotepath ):
        'push a local file to remote server'
        address = server.address
        port = server.port
        username = server.username
        known_hosts = self.inventory.known_hosts
        private_key = self.inventory.private_key

        pieces = [
            'scp',
            "-o 'StrictHostKeyChecking=no'",
            ]
        
        if port:
            pieces.append( '-P %s' % port )

        if known_hosts:
            pieces.append( "-o 'UserKnownHostsFile=%s'" % known_hosts )

        if private_key:
            pieces.append( "-i %s" % private_key )

        pieces += [
            path,
            '%s@%s:%s' % (username, address, remotepath),
            ]

        cmd = ' '.join(pieces)
        
        self._info.log( 'execute: %s' % cmd )

        failed, output, error = spawn( cmd )
        if failed:
            msg = '%r failed: %s' % (
                cmd, error )
            raise RemoteAccessError, msg
        return


    pass # end of SSHer


from dsaw.ComputingNode import ComputingNode
_localhost_aliases = ComputingNode.localhost_aliases
_localport_aliases = ComputingNode.localport_aliases + [
    22, '22',
    ]
def _tunneled_remote_host(server):
    address = server.address
    if address not in _localhost_aliases: return False
    port = server.port
    return port not in _localport_aliases
def _localhost(server):
    return server.isLocalhost()


import os
from dsaw.utils.spawn import spawn


# version
__id__ = "$Id$"

# End of file 
