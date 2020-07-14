import os
from cryptography.fernet import Fernet


class Encryptor:
    def __init__(self, file_ext_targets, key=None):
        # 암호화 툴 클래스의 인스턴스를 초기화합니다.
        self.file_ext_targets = file_ext_targets
        self.key = key
        self.cryptor = None

    def generate_key(self):
        # 암호화를 위한 128-bit AES Key를 생성합니다.
        self.key = Fernet.generate_key()
        self.cryptor = Fernet(self.key)

    def read_key(self, keyfile_name):
        # 파일로부터 Key를 읽어옵니다.
        # rb: (읽기 위해 2진 파일을 열기)
        with open(keyfile_name, 'rb') as f:
            self.key = f.read()
            self.cryptor = Fernet(self.key)

    def write_key(self, keyfile_name):
        # Key를 파일로 저장합니다.
        # wb: (쓰기 위해 비어 있는 2진 파일을 작성)
        print('Key:', self.key)
        with open(keyfile_name, 'wb') as f:
            f.write(self.key)

    def crypt_root(self, root_dir, encrypting):
        # 루트 디렉토리에서 시작하여 해당 확장자에 맞는 모든 파일을 암호화/복호화 합니다.
        for root, _, files in os.walk(root_dir):
            for f in files:
                abs_file_path = os.path.join(root, f)
                # 우리가 목표로 하는 확장자가 아니면 제외합니다.
                if not abs_file_path.split('.')[-1] in self.file_ext_targets:
                    continue
                self.crypt_file(abs_file_path, encrypting=encrypting)

    def crypt_file(self, file_path, encrypting):
        data = None
        # 암호화/복호화를 수행합니다.
        with open(file_path, 'rb') as f:
            _data = f.read()
            if encrypting:
                data = self.cryptor.encrypt(_data)
                print('File Encrypted:', file_path)
            else:
                data = self.cryptor.decrypt(_data)
                print('File Decrypted:', file_path)
        # 수행된 결과를 파일에 저장합니다.
        with open(file_path, 'wb') as f:
            f.write(data)


if __name__ == '__main__':
    # 현재 폴더부터 암호화: '.'
    # 사용자 루트 폴더부터 암호화: '~'
    root_dir = '.'
    file_ext_targets = ['txt', 'exe']

    # args를 전달 받습니다.
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('--action', required=True)
    parser.add_argument('--keyfile')

    args = parser.parse_args()
    action = args.action.lower()
    keyfile = args.keyfile

    encryptor = Encryptor(file_ext_targets)

    # 복호화를 수행합니다.
    if action == 'decrypt':
        if keyfile is None:
            print('--keyfile 옵션으로 키 파일을 설정해주세요.')
        else:
            encryptor.read_key(keyfile)
            encryptor.crypt_root(root_dir, encrypting=False)
            print('복호화가 완료되었습니다.')
    # 암호화를 수행합니다.
    elif action == 'encrypt':
        encryptor.generate_key()
        encryptor.write_key('key')
        encryptor.crypt_root(root_dir, encrypting=True)
        print('암호화가 완료되었습니다.')
    else:
        print('--action: encrypt 혹은 decrypt를 넣어주세요.')
