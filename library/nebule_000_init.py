"""
Nebule Library Initialization

This module contains the initialization constants and settings for the nebule library.
It is equivalent to 000_init.php in the PHP version.

WARNING: Any modification of this code will change its footprint and automatically
result in its invalidation!
"""

# Library metadata
NEBULE_NAME = 'library'
NEBULE_SURNAME = 'nebule/library'
NEBULE_VERSION = '020261015'
NEBULE_AUTHOR = 'Project nebule'
NEBULE_LICENCE = 'GNU GPL v3 2010-2026'
NEBULE_WEBSITE = 'http://www.nebule.org/'
NEBULE_CODING = 'application/x-python'
NEBULE_FUNCTION_VERSION = '020251230'

# Library paths and files
LIB_LOCAL_ENVIRONMENT_FILE = 'c'
LIB_LOCAL_ENTITY_FILE = 'e'
LIB_LOCAL_LINKS_FOLDER = 'l'
LIB_LOCAL_OBJECTS_FOLDER = 'o'
LIB_LOCAL_HISTORY_FILE = 'h'

# Node ID constraints
LIB_NID_MIN_HASH_SIZE = 64
LIB_NID_MIN_NONE_SIZE = 8
LIB_NID_MAX_HASH_SIZE = 8192
LIB_NID_MIN_ALGO_SIZE = 2
LIB_NID_MAX_ALGO_SIZE = 12

# Link version
LIB_LINK_VERSION = '2:0'

# Default puppetmaster
LIB_DEFAULT_PUPPETMASTER_EID = '88848d09edc416e443ce1491753c75d75d7d8790c1253becf9a2191ac369f4ea.sha2.256'
LIB_DEFAULT_PUPPETMASTER_LOCATION = 'http://puppetmaster.nebule.org'

# Reference IDs (RID)
LIB_RID_SECURITY_AUTHORITY = 'a4b210d4fb820a5b715509e501e36873eb9e27dca1dd591a98a5fc264fd2238adf4b489d.none.288'
LIB_RID_CODE_AUTHORITY = '2b9dd679451eaca14a50e7a65352f959fc3ad55efc572dcd009c526bc01ab3fe304d8e69.none.288'
LIB_RID_TIME_AUTHORITY = 'bab7966fd5b483f9556ac34e4fac9f778d0014149f196236064931378785d81cae5e7a6e.none.288'
LIB_RID_DIRECTORY_AUTHORITY = '0a4c1e7930a65672379616a2637b84542049b416053ac0d9345300189791f7f8e05f3ed4.none.288'
LIB_RID_CODE_BRANCH = '50e1d0348892e7b8a555301983bccdb8a07871843ed8f392d539d3d90f37ea8c2a54d72a.none.288'
LIB_RID_INTERFACE_BOOTSTRAP = 'fc9bb365082ea3a3c8e8e9692815553ad9a70632fe12e9b6d54c8ae5e20959ce94fbb64f.none.288'
LIB_RID_INTERFACE_LIBRARY = '780c5e2767e15ad2a92d663cf4fb0841f31fd302ea0fa97a53bfd1038a0f1c130010e15c.none.288'
LIB_RID_INTERFACE_APPLICATIONS = '4046edc20127dfa1d99f645a7a4ca3db42e94feffa151319c406269bd6ede981c32b96e2.none.288'
LIB_RID_INTERFACE_APPLICATIONS_DIRECT = 'f202ca455549a1ddd553251f9c1df49ec6541c3412e52ed5f2ce2adfd772d07d0bfc2d28.none.288'
LIB_RID_INTERFACE_APPLICATIONS_ACTIVE = 'ae2b0dd506026c59b27ae93ef2d1ead7a2c893d2662d360c3937b699428010538b5c0af9.none.288'

# Reference code algorithm
LIB_REF_CODE_ALGO = 'sha2.256'

# Default values
LIB_FIRST_GENERATED_NAME_SIZE = 6
LIB_FIRST_GENERATED_PASSWORD_SIZE = 14
LIB_FIRST_RELOAD_DELAY = 3000

# First locations and authorities
LIB_FIRST_LOCALISATIONS = (
    'http://cerberus.nebule.org',
    'http://puppetmaster.nebule.org',
    'http://bachue.nebule.org',
)

# Reserved objects
LIB_FIRST_RESERVED_OBJECTS = (
    'nebule/objet',
    'nebule/objet/hash',
    'nebule/objet/homomorphe',
    'nebule/objet/type',
    'nebule/objet/localisation',
    'nebule/objet/taille',
    'nebule/objet/prenom',
    'nebule/objet/nom',
    'nebule/objet/surnom',
    'nebule/objet/prefix',
    'nebule/objet/suffix',
    'nebule/objet/lien',
    'nebule/objet/date',
    'nebule/objet/entite',
    'nebule/objet/entite/prive',
    'nebule/objet/entite/localisation',
    'nebule/objet/entite/maitre',
    'nebule/objet/entite/maitre/securite',
    'nebule/objet/entite/maitre/code',
    'nebule/objet/entite/maitre/annuaire',
    'nebule/objet/entite/maitre/temps',
    'nebule/objet/entite/autorite/locale',
    'nebule/objet/entite/recouvrement',
    'nebule/objet/interface/web/php/bootstrap',
    'nebule/objet/interface/web/php/bibliotheque',
    'nebule/objet/interface/web/php/applications',
    'nebule/objet/interface/web/php/applications/modules',
    'nebule/objet/interface/web/php/applications/direct',
    'nebule/objet/interface/web/php/applications/active',
    'nebule/option',
    'nebule/danger',
    'nebule/warning',
    'nebule/reference',
    'puppetmaster',
    'cerberus',
    'bachue',
    'kronos',
    'asabiyya',
)

# Command line arguments
LIB_ARG_BOOTSTRAP_BREAK = 'b'
LIB_ARG_FLUSH_SESSION = 'f'
LIB_ARG_UPDATE_APPLICATION = 'u'
LIB_ARG_SWITCH_APPLICATION = 'a'
LIB_ARG_RESCUE_MODE = 'r'
LIB_ARG_INLINE_DISPLAY = 'i'
LIB_ARG_STATIC_DISPLAY = 's'
LIB_ARG_FIRST_PUPPETMASTER_EID = 'bootstrapfirstpuppetmastereid'
LIB_ARG_FIRST_PUPPETMASTER_LOC = 'bootstrapfirstpuppetmasterlocation'
LIB_ARG_FIRST_SUBORD_EID = 'bootstrapfirstsubordinationeid'
LIB_ARG_FIRST_SUBORD_LOC = 'bootstrapfirstsubordinationlocation'

# Configuration names, types, and defaults
LIB_CONFIGURATIONS_NAME = (
    'puppetmaster',
    'hostURL',
    'permitWrite',
    'permitWriteObject',
    'permitCreateObject',
    'permitSynchronizeObject',
    'permitProtectedObject',
    'permitWriteLink',
    'permitCreateLink',
    'permitSynchronizeLink',
    'permitUploadLink',
    'permitPublicUploadLink',
    'permitPublicUploadCodeAuthoritiesLink',
    'permitObfuscatedLink',
    'permitWriteEntity',
    'permitPublicCreateEntity',
    'permitWriteGroup',
    'permitWriteConversation',
    'permitCurrency',
    'permitWriteCurrency',
    'permitCreateCurrency',
    'permitWriteTransaction',
    'permitObfuscatedTransaction',
    'permitSynchronizeApplication',
    'permitPublicSynchronizeApplication',
    'permitDeleteObjectOnUnknownHash',
    'permitCheckSignOnVerify',
    'permitCheckObjectHash',
    'permitListInvalidLinks',
    'permitHistoryLinksSign',
    'permitInstanceEntityAsAuthority',
    'permitDefaultEntityAsAuthority',
    'permitLocalSecondaryAuthorities',
    'permitRecoveryEntities',
    'permitRecoveryRemoveEntity',
    'permitInstanceEntityAsRecovery',
    'permitDefaultEntityAsRecovery',
    'permitAddLinkToSigner',
    'permitListOtherHash',
    'permitLocalisationStats',
    'permitFollowUpdates',
    'permitOnlineRescue',
    'permitLogs',
    'permitJavaScript',
    'codeBranch',
    'logsLevel',
    'modeRescue',
    'cryptoLibrary',
    'cryptoHashAlgorithm',
    'cryptoSymmetricAlgorithm',
    'cryptoAsymmetricAlgorithm',
    'socialLibrary',
    'ioLibrary',
    'ioReadMaxLinks',
    'ioReadMaxData',
    'ioReadMaxUpload',
    'ioTimeout',
    'displayUnsecureURL',
    'displayNameSize',
    'displayEmotions',
    'forceDisplayEntityOnTitle',
    'linkMaxFollowedUpdates',
    'linkMaxRL',
    'linkMaxUIDbyRL',
    'linkMaxRS',
    'permitSessionOptions',
    'permitSessionBuffer',
    'permitBufferIO',
    'sessionBufferSize',
    'defaultEntity',
    'defaultApplication',
    'permitApplication1',
    'permitApplication2',
    'permitApplication3',
    'permitApplication4',
    'permitApplication5',
    'permitApplication6',
    'permitApplication7',
    'permitApplication8',
    'permitApplication9',
    'defaultObfuscateLinks',
    'defaultLinksVersion',
    'subordinationEntity',
)

LIB_CONFIGURATIONS_TYPE = (
    ('puppetmaster', 'string'),
    ('hostURL', 'string'),
    ('permitWrite', 'boolean'),
    ('permitWriteObject', 'boolean'),
    ('permitCreateObject', 'boolean'),
    ('permitSynchronizeObject', 'boolean'),
    ('permitProtectedObject', 'boolean'),
    ('permitWriteLink', 'boolean'),
    ('permitCreateLink', 'boolean'),
    ('permitSynchronizeLink', 'boolean'),
    ('permitUploadLink', 'boolean'),
    ('permitPublicUploadLink', 'boolean'),
    ('permitPublicUploadCodeAuthoritiesLink', 'boolean'),
    ('permitObfuscatedLink', 'boolean'),
    ('permitWriteEntity', 'boolean'),
    ('permitPublicCreateEntity', 'boolean'),
    ('permitWriteGroup', 'boolean'),
    ('permitWriteConversation', 'boolean'),
    ('permitCurrency', 'boolean'),
    ('permitWriteCurrency', 'boolean'),
    ('permitCreateCurrency', 'boolean'),
    ('permitWriteTransaction', 'boolean'),
    ('permitObfuscatedTransaction', 'boolean'),
    ('permitSynchronizeApplication', 'boolean'),
    ('permitPublicSynchronizeApplication', 'boolean'),
    ('permitDeleteObjectOnUnknownHash', 'boolean'),
    ('permitCheckSignOnVerify', 'boolean'),
    ('permitCheckObjectHash', 'boolean'),
    ('permitListInvalidLinks', 'boolean'),
    ('permitHistoryLinksSign', 'boolean'),
    ('permitInstanceEntityAsAuthority', 'boolean'),
    ('permitDefaultEntityAsAuthority', 'boolean'),
    ('permitLocalSecondaryAuthorities', 'boolean'),
    ('permitRecoveryEntities', 'boolean'),
    ('permitRecoveryRemoveEntity', 'boolean'),
    ('permitInstanceEntityAsRecovery', 'boolean'),
    ('permitDefaultEntityAsRecovery', 'boolean'),
    ('permitAddLinkToSigner', 'boolean'),
    ('permitListOtherHash', 'boolean'),
    ('permitLocalisationStats', 'boolean'),
    ('permitFollowUpdates', 'boolean'),
    ('permitOnlineRescue', 'boolean'),
    ('permitLogs', 'boolean'),
    ('permitJavaScript', 'boolean'),
    ('codeBranch', 'string'),
    ('logsLevel', 'string'),
    ('modeRescue', 'boolean'),
    ('cryptoLibrary', 'string'),
    ('cryptoHashAlgorithm', 'string'),
    ('cryptoSymmetricAlgorithm', 'string'),
    ('cryptoAsymmetricAlgorithm', 'string'),
    ('socialLibrary', 'string'),
    ('ioLibrary', 'string'),
    ('ioReadMaxLinks', 'integer'),
    ('ioReadMaxData', 'integer'),
    ('ioReadMaxUpload', 'integer'),
    ('ioTimeout', 'integer'),
    ('displayUnsecureURL', 'boolean'),
    ('displayNameSize', 'integer'),
    ('displayEmotions', 'boolean'),
    ('forceDisplayEntityOnTitle', 'boolean'),
    ('linkMaxFollowedUpdates', 'integer'),
    ('linkMaxRL', 'integer'),
    ('linkMaxUIDbyRL', 'integer'),
    ('linkMaxRS', 'integer'),
    ('permitSessionOptions', 'boolean'),
    ('permitSessionBuffer', 'boolean'),
    ('permitBufferIO', 'boolean'),
    ('sessionBufferSize', 'integer'),
    ('defaultEntity', 'string'),
    ('defaultApplication', 'string'),
    ('permitApplication1', 'boolean'),
    ('permitApplication2', 'boolean'),
    ('permitApplication3', 'boolean'),
    ('permitApplication4', 'boolean'),
    ('permitApplication5', 'boolean'),
    ('permitApplication6', 'boolean'),
    ('permitApplication7', 'boolean'),
    ('permitApplication8', 'boolean'),
    ('permitApplication9', 'boolean'),
    ('defaultObfuscateLinks', 'boolean'),
    ('defaultLinksVersion', 'string'),
    ('subordinationEntity', 'string'),
)

LIB_CONFIGURATIONS_DEFAULT = (
    ('puppetmaster', LIB_DEFAULT_PUPPETMASTER_EID),
    ('hostURL', 'localhost'),
    ('permitWrite', True),
    ('permitWriteObject', True),
    ('permitCreateObject', True),
    ('permitSynchronizeObject', True),
    ('permitProtectedObject', False),
    ('permitWriteLink', True),
    ('permitCreateLink', True),
    ('permitSynchronizeLink', True),
    ('permitUploadLink', False),
    ('permitPublicUploadLink', False),
    ('permitPublicUploadCodeAuthoritiesLink', False),
    ('permitObfuscatedLink', False),
    ('permitWriteEntity', True),
    ('permitPublicCreateEntity', True),
    ('permitWriteGroup', True),
    ('permitWriteConversation', False),
    ('permitCurrency', False),
    ('permitWriteCurrency', False),
    ('permitCreateCurrency', False),
    ('permitWriteTransaction', False),
    ('permitObfuscatedTransaction', False),
    ('permitSynchronizeApplication', True),
    ('permitPublicSynchronizeApplication', True),
    ('permitDeleteObjectOnUnknownHash', True),
    ('permitCheckSignOnVerify', True),
    ('permitCheckObjectHash', True),
    ('permitListInvalidLinks', False),
    ('permitHistoryLinksSign', False),
    ('permitInstanceEntityAsAuthority', False),
    ('permitDefaultEntityAsAuthority', False),
    ('permitLocalSecondaryAuthorities', True),
    ('permitRecoveryEntities', False),
    ('permitRecoveryRemoveEntity', False),
    ('permitInstanceEntityAsRecovery', False),
    ('permitDefaultEntityAsRecovery', False),
    ('permitAddLinkToSigner', True),
    ('permitListOtherHash', False),
    ('permitLocalisationStats', True),
    ('permitFollowUpdates', True),
    ('permitOnlineRescue', False),
    ('permitLogs', False),
    ('permitJavaScript', False),
    ('codeBranch', 'stable'),
    ('logsLevel', 'NORMAL'),
    ('modeRescue', False),
    ('cryptoLibrary', 'openssl'),
    ('cryptoHashAlgorithm', 'sha2.256'),
    ('cryptoSymmetricAlgorithm', 'aes.256.ctr'),
    ('cryptoAsymmetricAlgorithm', 'rsa.2048'),
    ('socialLibrary', 'authority'),
    ('ioLibrary', 'ioFileSystem'),
    ('ioReadMaxLinks', 2000),
    ('ioReadMaxData', 10000),
    ('ioReadMaxUpload', 2000000),
    ('ioTimeout', 1),
    ('displayUnsecureURL', True),
    ('displayNameSize', 128),
    ('displayEmotions', False),
    ('forceDisplayEntityOnTitle', False),
    ('linkMaxFollowedUpdates', 100),
    ('linkMaxRL', 1),
    ('linkMaxUIDbyRL', 4),
    ('linkMaxRS', 1),
    ('permitSessionOptions', True),
    ('permitSessionBuffer', True),
    ('permitBufferIO', True),
    ('sessionBufferSize', 1000),
    ('defaultEntity', LIB_DEFAULT_PUPPETMASTER_EID),
    ('defaultApplication', '1'),
    ('permitApplication1', True),
    ('permitApplication2', True),
    ('permitApplication3', True),
    ('permitApplication4', False),
    ('permitApplication5', False),
    ('permitApplication6', False),
    ('permitApplication7', False),
    ('permitApplication8', False),
    ('permitApplication9', False),
    ('defaultObfuscateLinks', False),
    ('defaultLinksVersion', '2.0'),
    ('subordinationEntity', ''),
)
