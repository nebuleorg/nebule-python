# ------------------------------------------------------------------------------------------
# Imports

# ------------------------------------------------------------------------------------------
#  /// WARNING /// WARNING /// WARNING /// WARNING /// WARNING /// WARNING /// WARNING ///
# ------------------------------------------------------------------------------------------
#
# [FR] Toute modification de ce code entrainera une modification de son empreinte
#      et entrainera donc automatiquement son invalidation !
# [EN] Any changes to this code will cause a change in its footprint and therefore
#      automatically result in its invalidation!
# [ES] Cualquier cambio en el código causarán un cambio en su presencia y por lo
#      tanto lugar automáticamente a su anulación!
#
# ------------------------------------------------------------------------------------------

if __name__ == '__main__':
    print('Do not call directly!')


class Node:
    TYPE = 'node'
    nodeId = '0'
    isNew = False

    def __init__(self, nid):
        if self.checkNID(nid):
            self.nodeId = nid
        else:
            self.nodeId = '0'
            self.isNew = True

    def checkNID(self, nid):
        return True

class Group(Node):
    TYPE = 'group'


class Entity(Node):
    TYPE = 'entity'
    publicKey = ''
    privateKeyID = '0'
    privateKey = ''
    privateKeyPassword = ''
