from hashlib import *
file = "YOUR FILE WITH PASSWORDS"


class CrackHashes:

    def check_length(self, length):
        """Return tuple of possible types of hashes"""
        if length == 32:
            return md5
        elif length == 40:
            return sha1
        elif length == 56:
            return sha224, sha3_224
        elif length == 64:
            return sha3_256, sha256, blake2s
        elif length == 96:
            return sha3_384, sha384
        elif length == 128:
            return sha3_512, sha512, blake2b

    def creating_hashes(self, passwd1, num_hash, length1=0, create_new_hash=False):
        length1 = length1 / 2
        """It is True if user wants to encode his text"""
        if create_new_hash:
            try:
                """Converting str to function and returning hash"""
                num_hash = eval(num_hash)
                sh = num_hash(passwd1.encode("utf-8"))
                final_sh = sh.hexdigest()
                return final_sh
            except:
                """Returning hash in sha256 because user passed wrong parameters"""
                sh = sha256(passwd1.encode("utf-8"))
                final_sh = sh.hexdigest()
                text = 'You passed wrong format so your text is encoded in "sha256"'
                return final_sh, str(text)
        else:
            """It happens only with guessing passwords and it returns coded hash"""
            sh = num_hash(passwd1.encode("utf-8"))
            if length1 != 0:
                final_sh = sh.hexdigest(length1)
            else:
                final_sh = sh.hexdigest()
            return final_sh

    def guessing_hashes(self, hash1):
        """Taking one argument (hash1) and trying to crack it"""
        ag = CrackHashes()
        try:
            hash1 = hash1.lower()
        except:
            pass
        length = len(hash1)
        every_method_tuple = ag.check_length(length=length)

        with open(file, mode="r", errors="ignore", encoding="utf-8") as passwords:
            for password in passwords:
                passwd = password.strip()

                for method in every_method_tuple:
                    final_func = ag.creating_hashes(passwd, method)
                    if hash1 == str(final_func).lower():
                        try:
                            hash_type = method.__name__.split("ssl_")[1]
                        except:
                            hash_type = method.__name__
                        return str(passwd), hash_type

        return "Hash not broken"
