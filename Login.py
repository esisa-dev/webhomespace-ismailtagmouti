import crypt
import os
import subprocess
import spwd

class login :
    def __init__(self,username : str, password : str) -> None:
        self.username = username
        self.password = password

    def TesterUser(self) -> bool:
        try:
            if self.username in os.listdir("/home"):
                user_info = spwd.getspnam(self.username)
                hashed_password, salt = user_info.sp_pwd, user_info.sp_pwdp
                generated_hash = crypt.crypt(self.password, salt)
                if generated_hash == hashed_password:
                    return True 
        except :
            return False
        return False
    
    def adduser(self) -> bool:
        if self.username in os.listdir("/home"):
            print("x")
            return False
        try :
            cmd = f"sudo adduser {self.username} --gecos '' --disabled-password"
            subprocess.run(cmd.split(), check=True)
            cmd = f"echo '{self.username}:{self.password}' | sudo chpasswd"
            subprocess.run(cmd, shell=True, check=True)
            print("x")
            return True
        except :
            return False

    def login(self) -> bool:
        try :
            if self.TesterUser() == True :
                return True
        except : 
            return False
        return False

if __name__ == "__main__":
    p = login("user1","1234")
    print(p.adduser())