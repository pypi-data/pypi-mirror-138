# myprofile.py

def Hello():
    print('Hello NarMaw The Series')

class Profile:
    '''
    Example:
        my = Profile('Neko')
    my.company = 'narmaw-theseries'
    my.hobby = ['Watch Series', 'Sleeping', 'Cooking']
    print(my.name)
    my.show_email()
    my.show_myart()
    my.show_hobby()
    '''
    
    def __init__(self,name):
        self.name = name
        self.company = ''
        self.hobby = []
        self.art = '''
   |\---/|
   | ,_, |
    \_`_/-..----.
 ___/ `   ' ,""+ \\
(__...'   __\    |`.___.'; 
  (_,...'(_,.`__)/'.....+   Nar-Maw The Series
        Source: https://www.asciiart.eu/animals/cats
        '''
        
    def show_email(self):
        if self.company != '':
            print('{}@{}.com'.format(self.name.lower(),self.company))
        else:            
            print('{}@gmail.com'.format(self.name.lower() ) )
    
    def show_myart(self):
        print(self.art)
        
    def show_hobby(self):
        if len(self.hobby) != 0:
            print('--------my hobby--------')
            for i, h in enumerate(self.hobby, start=1):
                print(i, h)
            print('------------------------')
        else:
            print('No hobby')

# print('NAME:',__name__)
# รันในไฟล์ testoop.py

# ใช้รันคำสั่งนี้เพื่อทดสอบ สร้างขึ้นเพื่อให้รันคำสั่งด้านล่างนี้ เฉพาะในไฟล์นี้เท่านั้น
if __name__=='__main__':
    my = Profile('Neko')
    my.company = 'narmaw-theseries'
    my.hobby = ['Watch Series', 'Sleeping', 'Cooking']
    print(my.name)
    my.show_email()
    my.show_myart()
    my.show_hobby()
    # help(my) # ใช้สำหรับโชว์ว่าโปรแกรมเราทำงานยังไง
    print('------------------------')
    
    
    friend = Profile('Mumu')
    print(friend.name)
    friend.show_email()
    
    