import hashlib

if __name__ == '__main__':
    print('Do not call directly!')

class Crypto:
    def __init__(self):
        print('Do not call directly!')

    def get_hash(self, data):
        sha256 = hashlib.sha256()
        sha256.update(data)
        return sha256.hexdigest()
