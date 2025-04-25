# ------------------------------------------------------------------------------------------
# Imports
import os.path
import traceback
import random
import syslog
import datetime
import binascii

# ------------------------------------------------------------------------------------------
BOOTSTRAP_NAME = 'bootstrap'
BOOTSTRAP_SURNAME = 'nebule/bootstrap'
BOOTSTRAP_AUTHOR = 'Project nebule'
BOOTSTRAP_VERSION = '020250425'
BOOTSTRAP_LICENCE = 'GNU GPL 2010-2025'
BOOTSTRAP_WEBSITE = 'www.nebule.org'
BOOTSTRAP_NODE = '88848d09edc416e443ce1491753c75d75d7d8790c1253becf9a2191ac369f4ea.sha2.256'
BOOTSTRAP_CODING = 'application/x-python'
# ------------------------------------------------------------------------------------------


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


# TODO vérifier version de Python


#
#
#
#
#
# ==/ 1 /===================================================================================
# PART1 - Initialization of the bootstrap environment.
#
# This part include all default values for the procedural library (Lib PP).
# ------------------------------------------------------------------------------------------

loggerSessionID = binascii.hexlify(random.randbytes(6)).decode('ascii')
metrologyStartTime = datetime.datetime.now()


def log_init(name):
    syslog.openlog(f'{name}/{loggerSessionID}', syslog.LOG_NDELAY, syslog.LOG_USER)


def log_reopen(name):
    syslog.closelog()
    log_init(name)


def log_add(message, level='msg', function='', uid='00000000'):
    diffdate = datetime.datetime.now() - metrologyStartTime
    syslog.syslog(f'LogT={diffdate} LogL="{level}" LogI="{uid}" LogF="{function}" LogM="{message}"')


def log_add_disp(message, level='msg', function='', uid='00000000'):
    log_add(message, level, function, uid)
    print(f'{level}({function}) : {uid} : {message}')


log_init(BOOTSTRAP_NAME)
syslog.syslog(f'LogT=0 LogT0={metrologyStartTime} LogL="info" LogI="76941959" LogM="start {BOOTSTRAP_NAME}"')
BOOTSTRAP_FILE_NAME = 'nebule.py'

nebuleInstance = ''
bootstrapBreak = []

#
#
#
#
#
# ==/ 2 /===================================================================================
# PART2 : Procedural PHP library for nebule (Lib PP).
#
# TODO
# ------------------------------------------------------------------------------------------

LIB_LINK_VERSION = '2:0'
LIB_DEFAULT_PUPPETMASTER_EID = '88848d09edc416e443ce1491753c75d75d7d8790c1253becf9a2191ac369f4ea.sha2.256'
LIB_DEFAULT_PUPPETMASTER_LOCATION = 'http://puppetmaster.nebule.org'
LIB_RID_SECURITY_AUTHORITY = 'a4b210d4fb820a5b715509e501e36873eb9e27dca1dd591a98a5fc264fd2238adf4b489d.none.288'
LIB_RID_CODE_AUTHORITY = '2b9dd679451eaca14a50e7a65352f959fc3ad55efc572dcd009c526bc01ab3fe304d8e69.none.288'
LIB_RID_TIME_AUTHORITY = 'bab7966fd5b483f9556ac34e4fac9f778d0014149f196236064931378785d81cae5e7a6e.none.288'
LIB_RID_DIRECTORY_AUTHORITY = '0a4c1e7930a65672379616a2637b84542049b416053ac0d9345300189791f7f8e05f3ed4.none.288'
LIB_RID_CODE_BRANCH = '50e1d0348892e7b8a555301983bccdb8a07871843ed8f392d539d3d90f37ea8c2a54d72a.none.288'
LIB_RID_INTERFACE_BOOTSTRAP = 'fc9bb365082ea3a3c8e8e9692815553ad9a70632fe12e9b6d54c8ae5e20959ce94fbb64f.none.288'
LIB_RID_INTERFACE_LIBRARY = '780c5e2767e15ad2a92d663cf4fb0841f31fd302ea0fa97a53bfd1038a0f1c130010e15c.none.288'
LIB_RID_INTERFACE_APPLICATIONS = '4046edc20127dfa1d99f645a7a4ca3db42e94feffa151319c406269bd6ede981c32b96e2.none.288'
LIB_RID_INTERFACE_APPLICATIONS_DIRECT = 'f202ca455549a1ddd553251f9c1df49ec6541c3412e52ed5f2ce2adfd772d07d0bfc2d28' \
                                        '.none.288 '
LIB_RID_INTERFACE_APPLICATIONS_ACTIVE = 'ae2b0dd506026c59b27ae93ef2d1ead7a2c893d2662d360c3937b699428010538b5c0af9' \
                                        '.none.288 '
LIB_REF_CODE_ALGO = 'sha2.256'
LIB_LOCAL_ENVIRONMENT_FILE = 'c'
LIB_LOCAL_ENTITY_FILE = 'e'
LIB_LOCAL_LINKS_FOLDER = 'l'
LIB_LOCAL_OBJECTS_FOLDER = 'o'
LIB_LOCAL_HISTORY_FILE = 'h'
LIB_NID_MIN_HASH_SIZE = 64
LIB_NID_MIN_NONE_SIZE = 8
LIB_NID_MAX_HASH_SIZE = 8192
LIB_NID_MIN_ALGO_SIZE = 2
LIB_NID_MAX_ALGO_SIZE = 12
LIB_FIRST_GENERATED_NAME_SIZE = 6
LIB_FIRST_GENERATED_PASSWORD_SIZE = 14
LIB_FIRST_RELOAD_DELAY = 3000

LIB_FIRST_LOCALISATIONS = (
    'http://cerberus.nebule.org',
    'http://puppetmaster.nebule.org',
    'http://bachue.nebule.org',
)
LIB_FIRST_AUTHORITIES_PUBLIC_KEY = (
    """-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAudMrAyvG3uqI9JLZRtqi
nlgiF6hAp/whKWlujNXE+x0p6ibJEaIAPS+VyR4Lw9819UqObpMI2fa+Ql8/dJPM
9r7Js/eJbRy6U7+EtBJa8ZIBTRtGXjKdBhkyQcWm8TqglitTG0pIoJOlB1+CbP2W
TtfbC6ZEFBFhlEH+qqy7Laua3m2yqVXqTY9FEBPYcX/Q2qpOeep+DkMQ/UwYyCZ0
Pv7KJ0aLlbju2UpYAp+zNfl6OKo37Va29anhU1i7lfXug7h0d9Lc4Xpl+KLfKn4A
g6VHSKXRAENvCXnGG3DM7UUdHM74NQXtwKzmtEwn7KT/3MKM6ohdbffkrAJFaeby
EMCVqq9nH4CZUIOGzLsAICtA6FXD5bi0OKv1Y1fzH4MHlc8FL5fCEdJ2ZftlURDH
Z2X2dE73Tx3TuyHr3e3A2xXMxcXZ0bs41Ey9wUWPRtBfEU6Yr3yXDQjMmLeCj/Vz
0Z/92hX5zE6UDpxTbuoPSUzGH0xwwZzsLAOIM0TvOxDI1ATX8M0Di2veYdLJMqoF
QMqFriycSa9a4U4SyXomUAqj9jBzn1dmPN+cvC+2ByqoRdGKkJQZAnLcfpN+G+lt
/GJe8Xgw01QlOFGT8PV9IvZek96PociLNqoyOhye7q5/Ik0fsEEIzYW2jvLGnrkv
6dEOw+BEVa0QiNx/ju9yzHMCAwEAAQ==
-----END PUBLIC KEY-----
""",
    """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAza1LNLyY3EMTeCOATF0A
VvK8MtfpBTV/VEihy5dVedjNERbSsowCaWFDBUmUhRqAVDH/0I3qbP15gNTVa5As
yF0GX3w3268XF7ZEqgfjyDEzVpsUq2iThecHMekKPkiE7UAySfLLNkfnA0yEPcnN
JXo+fGEdnxhXimGO8aEmNNb4St5CUGNFjXlInvQH8vv5s3JV+ZPgAbpnB77ykYSx
+ernGQulv5E6j4sjHLh0M7eoHvt21HuKHHp0dyl5ZVSJJDak1rBRbpmumFqFzSf5
dVCtMiX1Dd2bqqw844JptVciFO/8tVXfaIt3aSbC61bjF+gCGFIe3meOVTVbJ5lN
BQIDAQAB
-----END PUBLIC KEY-----
""",
    """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA9fNcqhAIUjQnXJTl7kRR
OWaxG/4luD/V22MqyIGBkopRNS0N2KS+DcTGa8znBbOhZrObtmEG3sRvqMrR5bSL
1TJXvmYf7IP3UygVw2q4khp/Xxpu4dYFow0+Y0Hj6TMf6H0BNa0OZiwpOArCtScz
qgbkLcYViD4pEccCoC/IttBSeXGZ9p9Yaqal8W11EBe8LlajJ0XGRPEy/KZogXzE
OtkCmN47ZsfeKtn75ordrzOL+2W4KgA26QPCfBdPzanrV1NSeGyzmxV6lb2PAVUP
A1tjFJTZ9FBwf4YzWKzOuj4V+0oftsHRI+hKfBphHqWaVrg8QBjONLUePQPNRvZM
GQIDAQAB
-----END PUBLIC KEY-----
""",
    """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDG3s5ky2Ku85OCgVSGqNIpTLUY
ozhnkLO2WScjhREDVTmbA+oiEQ28myOP/30LI6vI3dMHK3dPIcyYK8ApaoGn0H3x
qxRlLiWpdAm47WMgbhuzktHxQ2D7pWWERPb/ybRrXZxymKb2Zv4RXd2WN+qulk1J
vQKPJnvvk30EMrSyhQIDAQAB
-----END PUBLIC KEY-----
""",
    """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAq9dMDhbJB0FK7voozRcd
hLtTJHkrVxPt1XmhFJTnLLsqkbS5hoRqw8POMb5YKpJRinuE19auF12vUwVNNRV1
WEKqNw23yQFj5DAeJhQ0rn12BRr9EGO0fpVcT45c1XUBJ+O3RCjGbLvAuPllVv6o
kPqbWxrpBgjFUbvUgxC543t+Nu7Uih7c5oABp+9H6nLEdWpF+MhbTsOpNp1G+C5o
u6cSeGbs98x91v71AQB/5Y1poVDSCeaO8KT0I1BF6h8ookYJaFtZ4gO/qm4doQDg
YQzYHG+jbU1QJriY5uCQqbgrbGj8b8VfUGNtSoRPVfDbhU0mxKJrrAtpLjsWModS
fQIDAQAB
-----END PUBLIC KEY-----
""",
)
LIB_FIRST_LINKS = (
    'nebule:link/2:0_0>020210714/l>88848d09edc416e443ce1491753c75d75d7d8790c1253becf9a2191ac369f4ea.sha2.256>5d5b09f6dcb2d53a5fffc60c4ac0d55fabdf556069d6631545f42aa6e3500f2e.sha2.256>8e2adbda190535721fc8fceead980361e33523e97a9748aba95642f8310eb5ec.sha2.256_88848d09edc416e443ce1491753c75d75d7d8790c1253becf9a2191ac369f4ea.sha2.256>4fcc946ef03dff882c0b6a1717c99c0ce57639e99d1f52509e846874c98dad5abd28685c9d065b4ef0e9fefbbee217e91fc4a72ecac81712e1e2c14bd06612e71e9afdb09ef1c10e68117fe8edc4f93510318719d0a6d7436a1802cd38f814cba8503ef24d50aeca961825bc39b169acbe52240fa8528a44f387ee5dff0e096a2ab49a0b181fa688678540dfc409000104a6ab77c44a4495ac98d48f35658238c99f5b1f83d04c3309412ebf26b7b23c18bdde43b964ebb6b28b60393b4c343f567137461743153091039c07e35432fa7d0b46b729f65c11960cbda5cb78f3d8da52aaf662724e771125cce2fb99ef1409fbb23840872c6557fe63f2b25c8fc49b6b5663a44cdf2e829ffa9698cc121648136fd102333a556a97ac5b208a6b6fa584e239a35237fe9c38fd09fbe4c0580ca538d92c4e29d5e22ce4846df2563dc4cb39a599b92f22018b4973b768cf59cb8f517f3adae3ee21b7c43a812ec6c245fe548e6187a0e07ce6a0af38c40ccd24383216cbd312322e1583d5d358ccdc9911b67fdbf7d13b9f57a0a17a42f736be9dbd383fd9e7c0ce2589fbd6550a8e07ab90618302956a1bf69e76aaf3da829e1af4f7c7ceff169ce5e698ebe1987fa1b694c6b25130c0be5bbfdfe4a8594e54067abe235bf796cf455a84906d02ebc79e3feaa069db7c4adac872c104bfcbc08b2dfbcc3c9fd6aa465fb9d86c7f26.sha2.512',
    'nebule:link/2:0_0>020210714/l>88848d09edc416e443ce1491753c75d75d7d8790c1253becf9a2191ac369f4ea.sha2.256>970bdb5df1e795929c71503d578b1b6bed601bb65ed7b8e4ae77dd85125d7864.sha2.256>5312dedbae053266a3556f44aba2292f24cdf1c3213aa5b4934005dd582aefa0.sha2.256_88848d09edc416e443ce1491753c75d75d7d8790c1253becf9a2191ac369f4ea.sha2.256>72ce2d1c9075a26bb8264564055426cec289d350cbc1e8d5e7472ee28db17606d06777a5831d3346f82a78a1e0b1a7ce2b66d61f59e0c15e8deb53c45f3245746c4afeece6a240cf50f285597b51050c49156b2b07860c4a78ec07d8bd1ec5bb1450b41b914e96642ae0260b819821727ded678288a10c21a02809a22333fad392c5f2d67636e1174c03d936457371a8f2dae5e1369f93adff03903426a6c69cddada88b6ec687573a2ec5cb78cb8f9401631739c78adcf000b92acece6cc34626528be94173754eda077ea26bbc45b7a4067b1dfdccb54ce8efb7634d2ab19ec0b30441d38d77e412e3bca1fc77fb6552fed7e14b4dfae157db5d1abc0bd768f0fd548a4124908985b7c9cc47e8058516008e99850cf0d7811981c8fd0621ebf8ca0a16b2ea3d6f2bf1a0e6b881344638d314f76af6c97dbf5618d04d881ee3b555284fcf461c23d3729aceb4be35118d28e7bccd2001324cdacb0b8000b21cf23c6d09cbf6d8d0ab4b64dd9e6872ed90ee349164c62a08506f5148cd6beb0b18449f798e6517419db44f14e623de912a6161b1f45eb3a40f8215b61cc5735c1362f7a45463dcc4c8b9a08954afc49f4c9eba13508aa9a5d5ed1bea9f8136ca2acb5c5601dca31b033f802b7fc0491f8b9062574500ad17674e1bfdcd78b183f1e4eeb7395822e95161c3fa5f3a1b59f8c18c9d4ba716a7cb7756d3d971d881.sha2.512',
    'nebule:link/2:0_0>020210714/l>88848d09edc416e443ce1491753c75d75d7d8790c1253becf9a2191ac369f4ea.sha2.256>f976f916d794ad6384c9084cef7f2515305c464b2ab541142d952126ca9367e3.sha2.256>940c75a60c14a24e5f8bda796f72bef57ab1f64713a6fefd9a4097be95a9e96a.sha2.256_88848d09edc416e443ce1491753c75d75d7d8790c1253becf9a2191ac369f4ea.sha2.256>56a9487ee5ea86fa35649b3b5e9fe6c20387139d41b3aa822dacacaa4c1284f31f60aec293df1406fcd6dfc89248457d4f97f35c1ebe0a30c0a0424eb28b9c5b2299b3faecf5b691857f73eaedd98e56b8c17c4f183bb300f6e0c01f156be592e1669fa26db14fc864ebc913df77e53ebeb6e8fdefd49ac71fd00a42f99a790c098a33755078cb73b37c618a379c12578d66be94256689d0cc65427cee7c51e07f37553931e66d0b0090779d3e869fb45888a4c0b1e61bc1ce63f8a12ea4ff6cb039f62c24c1b5cbbee78329e21042278514d4b9cdd3f028c2b12e6ad4a00526e1fc2093a65c8d33402cae2f38a40fa1ec6b37a52725ad1010e78b9b6262d50055e6214a2b4b96fdc7354220b5a0117979441ffd24f976e42943defdf36ef9910fb452d920890251c4e5297e56a16d2a4ab97c00882cff19b42f3f6a1edca9cf6f0a7e157a8dfbeb5595ebb576e5d512f5f046071455a55d1098e19e3725dae564e9fc138d4faec180e5fd71a6db36c6cbece824e52cac913004ad406247b2eb51a91a2c0a2552961a265157c59e8455a4a7c8ad7e0be90014bc8fcac3e103fc4469380961d7d1f59a77678f2ff97f7db78cb243a0bb71ab6b63f4a10e786a06b8d4aff2f5b5a133a1019524af59923c813fcc0bc4588b64e6cb6e81c77fdaec73b069d20e435d69f40fe0a2e5656c9fa7aed13fda2d071bd9c850a7415ffdcd.sha2.512',
    'nebule:link/2:0_0>020210714/l>88848d09edc416e443ce1491753c75d75d7d8790c1253becf9a2191ac369f4ea.sha2.256>90f1075d96b6d74e3b69bc96448993f9f3a02f593ad0795d5b02e992bacf5b39.sha2.256>0f183d69e06108ac3791eb4fe5bf38beec824db0a2d9966caffcfef5bc563355.sha2.256_88848d09edc416e443ce1491753c75d75d7d8790c1253becf9a2191ac369f4ea.sha2.256>3a2ea2a5abfb9078ee67ba038f0f7e2900edde48e613ac2cc9c51e2f3951094c8087ce85ff08adf5eecd30d1442210b39e80cb65359290493df77f5d7f1b6b5a4311b506954887e432865174cef01390e8ce891582bdaa1564235848f151869824796316e1206f60132290474b314f55b4c038739e296137f84ea4f7dbf1a099dfdd5f141e0111da06b83016c2dcf857b0542836f9a9ed3cec5623a8be3142b3d29df5b580355969673029dc8c738a485105c8bb653cbc788d49557f02f8d4cf8f3971c23ab9b889f6757da351686ac7b9ed18860750c1f9de77d430805c7a0109eba20bcc33e7bafc77eda83974155285d0af75cebdf3b4784f3adb9ae05c89ef47578658849493ab6ee0cc58410a1a5bae9e75162fcc84a292617b32803d717af6e41cd5c750394edc38cc299dc0bf5133ec610d696d7e1ecd05398332aac8a255741094c2f96802867a139ca9203f8edd5cc23a0a32b75df643d76caf852e1b4557a7efb9b8d837f1a985d3b435df9460e37628a7f37d8527f208bfd9ed58989b72ffc152e7f4e1bbc195319a66bd78e5a9c056905dd0da842be58be710ff41ff96d63166e767868b1d6705cdeb4fbb3261fd36cf64c47db39567b49fda3c257c020b577c837bfe362b6e9b261efe8a33b1586820451eaf9767d8c6511a598864e2f6238be310166ee7309026f7afdf69059f110b88431e6242b2beac7456.sha2.512',
    'nebule:link/2:0_0>020210714/l>01351dd781453092d99377d94990da9bf220c85c43737674a257b525f6566fb4.sha2.256>daea63066cd8f5d4a9c8c80f3cc51f3c20b7fc74ac170ab2ce1950999b422f17.sha2.256_88848d09edc416e443ce1491753c75d75d7d8790c1253becf9a2191ac369f4ea.sha2.256>8c2333c73a4444979bfe70f1f7f84a095e088ac7d46f3c8f5883461a5c03f3656524302923456527f2df35410b4e6e9f78aa0a8e1eb944b0c1d2ffae256ddec4c4a0ca4487c90aa0f695f595625a841505c53fb38f0b4433f582960825244eb4b916a43bbaef9dee13cfd81c0d4bab18d0b2755441e003f944957134165a84168285cd876af7fe33152ceb3ab0e60c9e855e3ea40828add081166d39fb7c83bb95078dc0f51070d2ec4799838f8015e426ca1f898c1535f8c2e50028ef05365c019f9a08330ce4c093d1a3fb5db053e55b8b3b54b48e1d59a67f4414d50fc720ccf16db0438ff0a0d7f125fd98076058d8a6eb3f36214be7f7fbec484c8baf6260518c66faac802753384f74e4cbaf1412caf05809cdcec706af69ac840d9cb0a267311257afe52646ecb9f3be4b9aaf1f50d69aa65b309a3cb661e85f9cde9b583fc665e0ba4d21baf889067195b294a0a584c65284bd65426dfc2f24a71697834de398cbe2a90331dc1a452feca5b2d1a5bcfd1ab140af4c5ec5c3bf7fa9e9c1e28742495d412ce03da09abf1d7ea6289c2f1e7aff017e05c3fdbd95e5cafcae4d1a3f4567f3c18fd06b42670fa0efb27b8d40a7504004090f9a08292a096a2008017daf5095866a98b01f64ff7646f3798df7a725a2c92f3ecd95c3a535e52c0b38eb0c5789fe19c717414bb9d2152d1583edab8e2bb321e6481b9664d8d1.sha2.512',
    'nebule:link/2:0_0>020210714/l>01351dd781453092d99377d94990da9bf220c85c43737674a257b525f6566fb4.sha2.256>9e854553b868627af36369b5d9e1e9d5ae31a398e2bacb0816e98e5fb6e806ef.sha2.256_88848d09edc416e443ce1491753c75d75d7d8790c1253becf9a2191ac369f4ea.sha2.256>46b1dbd873bc547d6d7c0cbd9ded5eb9356735fa1944c391420cf8a5b637f2721ca0816621f71ed11e8a2d29a3ac7d5e36cebcc00fdf2545c15af902306f8d9bcd7df679768d4bf80e1a9f86979beb73accfd5f37f9784d44a5caaf1d442e4c66da7986c1a1c8760b07b1c550f751f16f99cd79aa5b639161169421b1ca58e8038aaa5fea7a2dfdf1a8bf18aa1a56a960b06e3637eeba28bc03a7b7326852c6e8890d7e1a7de3fa904e8027ba7142cb190d45832b871f5ba5a3b0230179e5a9ffc2ff8d11cd7ffb681311ca27dfd9aac246a5180f325cf7fb88d3a1c208b695725e365bce130f0b8761523409e0da0b7eec6c76b737d9d3e0c2e2675eadf6f27e60be613c31cd8837f756aa8e8cdca7164437cf19fa3f403cf0ed7a1a146cb2749df0d2d376dd58d18f5aa78c5b3669375ffbb242e1e65b1a78b88213efa7928225de4d09c217e12b941d8dca26719461a1730c45d1d34a88e3f2ea392a706fec654d44793bf1754e7a728e4f8c5a9b258ebc88f916b8f3b906b774145e4270d277f1962b0cfa0141462b7c6a2909966bf94d9b605b1dd89f81c94ed45f511dd0be7489dbf9018d073837d66f4e637dded4e1ea1ff6c0d32ef010df25b38315b0c0ecec8f809a4b1739a96701a143113d5662d31c586310dff7405f45e96ae6fdd2536376533b416e62d0282875d5c8ceb3dd293831613a49a0b492870b8b835.sha2.512',
    'nebule:link/2:0_0>020210714/l>19762515dd804577f9fd8c005a7803ddee413f264319748e30aa2aedf318ca57.sha2.256>b6fef678931e0761314983d9a08c19b095b088cf6500891206ca1f8b78c2d008.sha2.256_88848d09edc416e443ce1491753c75d75d7d8790c1253becf9a2191ac369f4ea.sha2.256>30093ab7ca813bfaeedb75a5cad9a1a85c66fb541e64d6a3f15853b39d7727704f2fe305c93d3c329941be88c4015098aadfcd2df15e36eb93c29aa97b24f5336fac7fb1e2be8b5d8d2af31239352bce431ab9497b30235a5ddf41a8cb914c1658d8ab6b4c43c492401820aac47b476e085599bbc194ef6820bb8d89cb0663a1c37ac573caffa60f44e0d09f5ac6890fc118b9bf563ce11fc2c02508d54c0d4c340e6da2287a1522b6496644702801b0b669eb32f76f3d55587f74e56d0709ec5a4abd1a86530cbf038ff9ff9b83bbeb9f116e9fabaa8d0b8d426cdd444de489e17898b8d9fe952adb44bcafc0ef1aa1b6389c1ee372ed925c871de08b9cff2d38043c541da66ac8792a421fe44626eefaed010102792f0a3cc6a47a3972f093a8529aa89890630e944da7760b1ef59030bf29e364c7b5576a60a29e6507d93f70d03d3500b3546c2e8cdb81e0bf57507f27d5b76874fa9af0bd417388420fbb070ddbdadb5556e6ec98d6577acf4a52d0856a36a0c1608568792fb21ab668a5ab1b23b508213ee82872605ef0010879d84470399d68ca80996995fdb7fefa261b81b8a3dbb2c60d74508aa671970c2df4029ff345f8e506ec6c503a7db84bc63c29cf56af53296b6f1baf0cd674d9391dc8675cb1c90b7ca1a462a0cb5fc2b1af678d6420bfb6633739502a56dbf8457d530dfbcc40cefd4d0919d64488a8f6.sha2.512',
    'nebule:link/2:0_0>020210714/l>4e72933c991c2bb27415cfeff02e179b9a3002934e472142c4f612e3893e46e1.sha2.256>83db082578142c900e36765ebc210893d79ed0ab1127d687f3307c0c061802e6.sha2.256_88848d09edc416e443ce1491753c75d75d7d8790c1253becf9a2191ac369f4ea.sha2.256>2a6d15ec23edb07da6e1271026a252c5a3b96bf7931cc25dcbe85ba8d488ff5128e243720202f3a792d3700845b387b8f7b8f0da70770c34fc3172ae9fb17bc8b2e2235a92dd133136cc5b63ebd06ccedeb2c4291b11ff3dd89c73caf65ec14279e08ae2ce02672da9f6de5f40b249857c128d2c2c7932de5fc8223fffd0db899abefeaf725dac4526711594ab06f16a1702b34afef83c17b30b4cde0fe080031a36fb3a676e79199b2601cd1dcf7dc52d43b990634cad8df3dafb645c6fe446aaf25a276103c5989f9536ca4fe7e35d079ea7b61c5d68132bc5c2ac4fdb1cb0762a566fc9da85075ee454a6e2f14af2facd084bda59ce98131f066dff3af7935d107e518310bd84fe54c60be549e48b00937a998969db572bd33757c637b556f12203e999f2a9d5e4f62e2c632a08fdc0c877ef0a75603e5e44f6a5f3b3ac5dbfa4ffec1cb3431a992143d5534f9ded09b0a183c135b5759ddedef9426da41e82f6d522f94c1c4c422fc8983d68685966de408e029d2324e0e9baf00c8bb18454f3f32285b73b4b68abca210afaa8cfe089f7d3b32b1289a57119e8115b85cdc1b2d5756675fce351ef4501f4d7226075d8092e1e428551c8133764751b58311ae0c54e2a57065517020f0286fb51e96a01226db1143e479a94d6ff2c922ec27c5f64af5bc8e8794fb5391400bac6666bd5e21f61d23aefc94db0f3a525a59c.sha2.512',
    'nebule:link/2:0_0>020210714/l>abdbaa31e404463ecc644f1eecdeb9b5f94428eb140fa5c66a7687ee96ed47aa.sha2.256>663eb81c89c27739f0f875617bcd45b3a18d4b8eb859b8c6e5dccbf9085a2ef9.sha2.256_88848d09edc416e443ce1491753c75d75d7d8790c1253becf9a2191ac369f4ea.sha2.256>7a76055a8e051f927027018b7d82ff2b5e388513f6e901ad61a07a02b6b23ea6f58e1d498eea7aebf597c9975f4422babed00b3dc9c4b1ba09967cd245246412d3827d010f99da45b7408d5d0e6b47a3df8e719675dc907108013ccbd698731d6b74912d1723e58d70cb96ceaac979cfdf2b332d9d010402ef581b4d509ead6d0e03b3587d265e5e460b7f78261315aeb1057ca02e2b4d24590bbc5986d8882d97e1afe080708b8f5d6768b1a423e2fe981916aef2ce663be384c8cff0cffae3f72316fc0bf068b031a068b9f6090cf2cac0be1360acebcb1ad22d67dacb7b46eb51f69e7898d25a9511ae9c4100c42eb0c7a6317d5a90ca1ac40f37d95f83ff9de81843c3206c11c4a26d2b0093b49e48c436f9b1b07ad5828ea711493e69bb08ed6c2940004d56af796c3daf68ad6dbadaecff717f6d7373d1cf182d6be14a5e8c37d4abfdc9f0c843d59de875e4501f202d87b6a14940e0725eb5e5d2a94bea3f2764fa9918093340d7948aab7846fd820dfe1c73345389d8f1a2ea1c4aa943bdeaf73c234812a46f997ebc058caa0a912ce02fe2414ef84bd957c47e78582601ee5aee78f973ff3fe318ac091e2a8021435203d0a7a4b459ab4714bf5d1395324cd4a098777fbaa70716c21d8f2c82632a0f7abb9e366ae3138fd7eb5e024823f80275d486fc7763d3ac5147992807c779ad1fedcf60446de306e453dade.sha2.512',
    'nebule:link/2:0_0>020210714/l>01351dd781453092d99377d94990da9bf220c85c43737674a257b525f6566fb4.sha2.256>a4b210d4fb820a5b715509e501e36873eb9e27dca1dd591a98a5fc264fd2238adf4b489d.none.288_88848d09edc416e443ce1491753c75d75d7d8790c1253becf9a2191ac369f4ea.sha2.256>5ef73754556326b9bde83230cc4ed503364821fa96b774086c2146a451f842339b5ec66741f6608d5fa16a7bde0d80f7711c828163a9b2222c128fa6403130b97592d11b2001551724c65360195764dda11e58c4b3ef8cb7870dd9f1add0ab5680e957d3adcd6b60e22fc718ddd14aa9048f2c26b466b0a0139e7f93a7ffc39df0d430646eff6581548b1cb09b032a829e4a905a712a6400641408a8574d50db98e52a60eae13966ea266023c11c174b86bc4f2e43f10bd4c94e86a8a7b17f9a9eb95cdf82d3f08b25605ba0f7a1b4fe54aaa7bd263cde55bf7e62ab73ddf4d8b5aceccb8d1491344ce001702111e04eb887b45ef8c437c25e1bf4928abded74d1bab4104fa734ccdf22310d771b44972f8aeeaa389e3b0fc2ca32cfc6a4ab89f89ed712b8c13f1e36fde7b00a69a726df4cfc0234d57131d7d5650849be5ba2f1eb8693da15e3502a1787d6e6b5bb74f5cc40e806e53e4888c8d5dd2d0f0f4a8922e9863e0c432dc491260ac6ff34a041e8317e4edf6a265c8f0ce16a39d4ec27ae4d34e8a9c0027318b9f52d35362429f706b9dd9ea6d6c2bb8cf71d6322f62f78ec62532be1abd30f8bc5c5a004c399ce13a53a98d42947c02426e93028918d6d0cd84d81b7e533c8306d81faa1333f2dd904156d8feecf610f1b02096aebac63daa8a59785de0e9e30d4941ebd152bd82ce12cf9d460c01d001c394a404a.sha2.512',
    'nebule:link/2:0_0>020210714/l>19762515dd804577f9fd8c005a7803ddee413f264319748e30aa2aedf318ca57.sha2.256>2b9dd679451eaca14a50e7a65352f959fc3ad55efc572dcd009c526bc01ab3fe304d8e69.none.288_88848d09edc416e443ce1491753c75d75d7d8790c1253becf9a2191ac369f4ea.sha2.256>85662c55aecc78be3d4decb1c97236b0ee574ac9a76bce59f8f7badd0a6697812b64722351c5ff23f230a6a3f2701e0b9abf1ebaa78a61986e2b551ffe9fb53b53d9b617213102dc219e9aff304e5290c9573c5d2b258dfca2bf493ba2b4b9a105335d8efe32cb41ac52035fff04da2b6023c96dc6b3fad2ab3ec5fc6f6c9eb45bc3888241f920b315c679b76f20b6397810da6a9d35e1c7b8c77f2068b6ca99eee5cbe4539fe52b6e0bcb402b8d52da7322b11e083c24fbca066c4a01d6d925cec684f3c8426582ac1123596ff2c79007c7275fa16dcb1297a98c0a5769fdf024994ba085e9f76de875e3e56d82f464432cc56f243c4d8224e7bed16137c8bf17067fdac04494fd3f7aed052f843b01fb611fe5d1874dcbef452b0fcc4898f8c4022673d436a15a75dc1fb664f79c819fef692ff24dd5c411ee169523fb8d7d175f1c681acb42e88669e21a48760a657c53a243fa14740c9ce20e12d78e7184a7fef8ea8e80ecc55e15be78ed99f300a6fa1a864ad532c96351bb4ea6a3608e933c3f6f9baf1c952754d74370a83f917253fb18a707b64ac668ad5a4845602fdf8196f68ba7d71190e2e92f2a71359e6fbc0c05a021efe3ce6d7fa6cb2fd13d4043549ecea2318ef8d515daf1c04e2741ef2946389b547d59d8256fb1dbadd7cee689dbf4fdae0133cda0171fe0131792ec6ab947625783e21a7878b553dc62.sha2.512',
    'nebule:link/2:0_0>020210714/l>4e72933c991c2bb27415cfeff02e179b9a3002934e472142c4f612e3893e46e1.sha2.256>0a4c1e7930a65672379616a2637b84542049b416053ac0d9345300189791f7f8e05f3ed4.none.288_88848d09edc416e443ce1491753c75d75d7d8790c1253becf9a2191ac369f4ea.sha2.256>57408e07d0430677174b0e50385ef605a172639f9dd6710b0dafbf1568585d1cdfe9c2149e6b57c585362051c802841e9105c17efbf5502342e624c9c6561a1413b73d79b8ead07131fecc0616d9b1aa25f874809731e52f3c5993821fef827f2fb2d668033f4573f8b7c65e29d69130f3b084bc48b8deb976c44a8874cd9231472390cd9caaed9dbd1a897d48ddb6cf50bfa9d54a870122a18e57064efa4b1c74959f265f280acc16d986c4e767cab2fb88db3d9e1fb6314362dfdfaa6f14d648976518530f3d325d40a6d75fa792f1d34c92f83738a230df743d3f774169a2cb6d8cef187caa3039e899d65f9b6c897a72f8a4ad4b6cd16d43ad843d36c6c762390dadc8b68327e2525e8bb2c27a01e4216e8120d1e60f9651dec68396e85cd953b456e361317f25ceab9b28ebc5a2c850f719978cd6f28b18e07f85e7c962bee9195f9f6bce3061025247aed71905f4f6a77015752a0f370af1302f4c7261de9eb65701d42cae9b0d4c308c51d597c0a5af68b9a60a45f8bfb47b82cd5e4999143cabdeaf49e7cad9d4057a2d2b892418386a79d9ab73390a474bf45045d99a0f589a1ddf70ccecaf51cae014e2a4401571719fd9d3361df062bebd7dd65b15fc0c7d63c186aa21c4c8a38d9a7d66cbf162600b4815c005815e414a0d2ee8174475a67b2a9b31eb53deca780a49649e5638ca867fb80cd2fdb7aea18099cb.sha2.512',
    'nebule:link/2:0_0>020210714/l>abdbaa31e404463ecc644f1eecdeb9b5f94428eb140fa5c66a7687ee96ed47aa.sha2.256>bab7966fd5b483f9556ac34e4fac9f778d0014149f196236064931378785d81cae5e7a6e.none.288_88848d09edc416e443ce1491753c75d75d7d8790c1253becf9a2191ac369f4ea.sha2.256>a0fcf7e0dd428892f8e8d95ec5683b37eb00578904b092812a41b32c6ad9e769ee4c6e45fdd628b27e237c89ba2d7faa0b466024f5397aa331e24de3cf0a09501b411f34b91e910273f52eca056d9618e43132302b8dd9c81b7e4b8831dd983fd6674cb8fe8348c7a7baac0d2a68b1538f153e7a316e3c6eff4e59d3b699578cdaf5b00e691f46e7971f0faa74889184509303b49f9b2d6becf74b6f546d7c61deb7709a68446266b35d134df92772f38b5557e6ecf6c5e671c3316f4df28ded39e328c730783d3a030e2c167a581566bfdf19f5fcabd83ccb65b625590aa2402fdcca823611467f17cbf9bc154aefe535055f8674c27e24cad84c9f2984ce1718b133f72ff1eec56d5df8fd1d25a9646044fb28eeb1a4a0a277b844e22ed559efadafc3959bcbde44aa6b6f4fbbee149ecb13a4537edcf654720dd4bf9b5a8b2bb0c322cc182e3ef7bb2971052aa6b3af706da3a04f3854d2b77f4fde40981fbd4ef857fc338303f2ebdd3bff3b9335ed0357730b35a2d5bb9f2d16440cf1230487fb72a5187a82e4d1e6daf66b2d24e8970e6e1aff18218fbfc4a65bd494cd13a345f7bb6c2bc906029af5ab25217e1227915c676437dacf695ac277b9ddabf4910aec25513b39ed1ae82f8fce136674a8e0b061065755230f458fab98818aeae2e9fa3a4542e55361b8d8fd8e07f1d63f411e75903a161f3143d40d70247a.sha2.512',
)

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
    'application/x-pem-file',
    'application/octet-stream',
    'application/x-httpd-php',
    'text/plain',
    'sha224',
    'sha256',
    'sha384',
    'sha512',
)

# Command line args.
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

BREAK_DESCRIPTIONS = (
    ('00', 'unknown buggy interrupt reason'),
    ('11', 'user interrupt'),
    ('21', 'library init error'),
    ('22', "library i/o : link's folder error"),
    ('23', "library i/o : link's folder error"),
    ('24', "library i/o : object's folder error"),
    ('25', "library i/o : object's folder error"),
    ('31', 'library load : finding library IID error.'),
    ('32', 'library load : finding library OID error.'),
    ('41', 'library load : find code error'),
    ('42', 'library load : include code error'),
    ('43', 'library load : load error'),
    ('44', 'application : find code error'),
    ('45', 'application : include code error'),
    ('46', 'application : load error'),
    ('51', 'unknown bootstrap hash'),
    ('61', 'no local server entity'),
    ('62', 'local server entity error'),
    ('71', 'need sync puppetmaster'),
    ('72', 'need sync authorities of security'),
    ('73', 'need sync authorities of security'),
    ('74', 'need sync authorities of code'),
    ('75', 'need sync authorities of code'),
    ('76', 'need sync authorities of time'),
    ('77', 'need sync authorities of time'),
    ('78', 'need sync authorities of directory'),
    ('79', 'need sync authorities of directory'),
    ('81', 'library init : I/O open error'),
    ('82', 'library init : puppetmaster error'),
    ('83', 'library init : security authority error'),
    ('84', 'library init : code authority error'),
    ('85', 'library init : time authority error'),
    ('86', 'library init : directory authority error'),
)

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
    'linkMaxRLUID',
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
    ('linkMaxRLUID', 'integer'),
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
    ('linkMaxRLUID', 4),
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


nebule_ghost_public_entity = ''
nebule_ghost_private_entity = ''
nebule_ghost_password_entity = ''


def lib_get_option_as_string(name):
    if name == '' or not (name in LIB_CONFIGURATIONS_NAME):
        return ''
    # TODO

def lib_get_option_as_bool(name):
    if name == '' or not (name in LIB_CONFIGURATIONS_NAME):
        return lib_get_option_as_string(name)
    # TODO


def lib_increment_metrology(type):
    # TODO
    return ''


def lib_get_metrology(type):
    # TODO
    return ''


def lib_set_metrology_timer(type):
    # TODO
    return ''


def lib_get_metrology_timer(type):
    # TODO
    return ''


def lib_init():
    if not io_open():
        bootstrap_set_break('81', traceback.extract_stack()[0][3])
    puppetmaster = lib_get_option_as_string('puppetmaster')
    # TODO

    return True


def io_open():
    if not io_check_link_folder() or not io_check_object_folder():
        return False
    return True


def io_check_link_folder():
    if not os.path.isdir(LIB_LOCAL_LINKS_FOLDER):
        io_create_link_folder()
    if not os.path.isdir(LIB_LOCAL_LINKS_FOLDER):
        bootstrap_set_break('22', traceback.extract_stack()[0][3])
        return False
    # TODO

    return True


def io_check_object_folder():
    if not os.path.isdir(LIB_LOCAL_OBJECTS_FOLDER):
        io_create_object_folder()
    if not os.path.isdir(LIB_LOCAL_OBJECTS_FOLDER):
        bootstrap_set_break('24', traceback.extract_stack()[0][3])
        return False
    # TODO

    return True


def io_create_link_folder():
    if lib_get_option_as_bool('permitWrite') \
            and lib_get_option_as_bool('permitWriteLink') \
            and not os.path.isdir(LIB_LOCAL_LINKS_FOLDER):
        os.mkdir(LIB_LOCAL_LINKS_FOLDER)
    if os.path.isdir(LIB_LOCAL_LINKS_FOLDER):
        return True
    return False


def io_create_object_folder():
    if lib_get_option_as_bool('permitWrite') \
            and lib_get_option_as_bool('permitWriteLink') \
            and not os.path.isdir(LIB_LOCAL_OBJECTS_FOLDER):
        os.mkdir(LIB_LOCAL_OBJECTS_FOLDER)
    if os.path.isdir(LIB_LOCAL_OBJECTS_FOLDER):
        return True
    return False


def io_check_node_have_link(nid):
    if os.path.isfile(f'{LIB_LOCAL_LINKS_FOLDER}/{nid}'):
        return True
    return False


def io_check_node_have_content(nid):
    if os.path.isfile(f'{LIB_LOCAL_OBJECTS_FOLDER}/{nid}'):
        return True
    return False


def crypto_asymmetric_encrypt(data, private_oid, password, entity_check):
    if private_oid == '' or password == '' or data == '' or (entity_check and not ent_check_is_private_key(private_oid)):
        return ''
    private_cert = ''

    # FIXME
    return ''


def blk_generate(rc='', req='', nid1='', nid2='', nid3='', nid4=''):
    if (req == ''
            or not nod_check_nid(nid1, False, False)
            or not nod_check_nid(nid2, True, False)
            or not nod_check_nid(nid3, True, False)
            or not nod_check_nid(nid4, True, False)):
        return ''
    bh = f"nebule:link/{LIB_LINK_VERSION}"
    if rc == '' or not lnk_check_rc(rc):
        date = datetime.datetime.now()
        rc = '0>0' + date.strftime('0%Y%m%d%H%M%S')
    rl = req + '>' + nid1
    if nid2 != '' and nid2 != '0':
        rl = rl + '>' + nid2
    if nid3 != '' and nid3 != '0':
        rl = rl + '>' + nid3
    if nid4 != '' and nid4 != '0':
        rl = rl + '>' + nid4
    bl = rc + '/' + rl
    return bh + '_' + bl


def blk_sign(bh_bl):
    if bh_bl == '':
        return ''

    if not ent_check_is_public_key(nebule_ghost_public_entity):
        return ''

    if not ent_check_is_private_key(nebule_ghost_private_entity):
        return ''

    if nebule_ghost_password_entity == '':
        return ''

    sign = crypto_asymmetric_encrypt(bh_bl, nebule_ghost_private_entity, nebule_ghost_password_entity, True)
    if sign == '':
        return ''

    return f"{bh_bl}_{sign}"


def blk_generate_sign(rc='', req='', nid1='', nid2='', nid3='', nid4=''):
    bh_bl = blk_generate(rc, req, nid1, nid2, nid3, nid4)
    if bh_bl == '':
        return ''
    return blk_sign(bh_bl)


def lnk_get_list():
    # TODO
    return True


def lnk_check_exist():
    # TODO
    return True


def lnk_check_not_suppressed():
    # TODO
    return True


def lnk_date_compare():
    # TODO
    return True


def blk_filter_structure():
    # TODO
    return True


def blk_filter_by_signers():
    # TODO
    return True


def lnk_get_list_filter_nid():
    # TODO
    return True


def lnk_get_distant_anywhere():
    # TODO
    return True


def lnk_get_distant_on_locations():
    # TODO
    return True


def blk_check_bh(bh):
    if len(bh) > 15:
        return False
    i = bh.find('/')
    rf = bh[:i - 1]
    if rf.len == 0 or rf == bh:
        return False
    rv = bh[i + 1:]
    if rv.len == 0:
        return False
    if not blk_check_rf(rf):
        return False
    if not blk_check_rv(rv):
        return False
    return True


def blk_check_rf(rf):
    # TODO
    return True


def blk_check_rv(rv):
    # TODO
    return True


def blk_check_bl(bl):
    # TODO
    return True


def lnk_check_rc(rc):
    # TODO
    return True


def lnk_check_rl(rl):
    # TODO
    return True


def lnk_check_req(req):
    # TODO
    return True


def blk_check_bs(bs):
    # TODO
    return True


def blk_check_rs(rs):
    # TODO
    return True


def blk_check_sig(sig):
    # TODO
    return True


def blk_verify():
    # TODO
    return True


def blk_parse():
    # TODO
    return True


def blk_write():
    # TODO
    return True


def nod_check(nid, check):
    # TODO
    return True


def nod_check_nid(nid = '', permit_null = False, permit_zero = False):
    if permit_null and nid == '':
        return True
    if permit_zero and nid == '0':
        return True

    l = nid.split('.')
    if len(l) != 3:
        print(f"invalid parts count nid={nid}")
        return False

    hash_val = l[0]
    algo_val = l[1]
    size_val = l[2]

    if algo_val == 'none' or algo_val == 'string':
        min_size = LIB_NID_MIN_NONE_SIZE
    else:
        min_size = LIB_NID_MIN_HASH_SIZE

    hash_ok = True
    valid = 'abcdef0123456789'
    for c in hash_val:
        if c not in valid:
            hash_ok = False
            break
    if (hash_val == ''
            or not min_size < (len(hash_val) * 4) < LIB_NID_MAX_HASH_SIZE
            or not hash_ok):
        print(f"invalid hash value {hash_val}")
        return False

    if algo_val == '' or not LIB_NID_MIN_ALGO_SIZE < len(algo_val) < LIB_NID_MAX_ALGO_SIZE:
        print(f"invalid algo value {algo_val}")
        return False

    if (size_val == '' or not min_size < int(size_val) < LIB_NID_MAX_HASH_SIZE
            or (len(hash_val) * 4) != int(size_val)):
        print(f"invalid size value {size_val}")
        return False
    return True


def ent_check_is_public_key(nid):
    return True


def ent_check_is_private_key(nid):
    return True


def bootstrap_set_break(errorCode, function):
    errorDesc = _get_from_array(BREAK_DESCRIPTIONS, errorCode)
    if errorDesc == '':
        errorDesc = _get_from_array(BREAK_DESCRIPTIONS, '00')
    bootstrapBreak.append([errorCode, errorDesc])
    log_add(f'bootstrap break code={errorCode} : {errorDesc}', 'error', function, f'100000{errorCode}')


def bootstrap_get_user_break():
    # TODO
    return True


def bootstrap_display_router():
    if False == True:  # FIXME check need first sync
        log_add('load first', 'msg', traceback.extract_stack()[0][3], '63d9bc00')
    if len(bootstrapBreak) != 0:
        log_add('load break', 'msg', traceback.extract_stack()[0][3], '4abf554b')
        return
    # TODO
    log_add_disp('TEST')


def bootstrap_log_metrology():
    timers = ''


def main():
    print('Start')
    if not lib_init():
        bootstrap_set_break('21', traceback.extract_stack()[0][3])
    bootstrap_display_router()
    # TODO
    bootstrap_log_metrology()


def _get_from_array(array, name):
    for line in array:
        if line[0] == name:
            return line[1]
    return ''


# OK, now play...
if __name__ == '__main__':
    main()
