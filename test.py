# mars_mission_computer.py
# 더미 센서 시스템
# 2025-03-23

class TEST:
    C_1 = 'class var'

    @classmethod
    def class_sensor(cls):
        aa = cls.C_1
        print('--', aa)
    
        return aa

    @staticmethod
    def static_sensor():
        aa = 20
        print('**', aa)
        return aa
    
    def instance_func(self):
        aa = 50
        print('$$$', aa)
        return aa
    
    def normal_func():
        aa = 50
        print('@@@', aa)
        return aa

    def get_ins(self):
        self.aa = 99
        print('##', self.aa)

        ## method가 인스턴스, 클래스에 링크되어 있는가
        ## static 메소드는 어디에도 링크 안됨

        # staticmethod / not link, 인스턴스-클래스로 호출 가능
        self.static_sensor()
        TEST.static_sensor()

        # instance method / instance(self) link, 인스턴스로 호출 가능능
        self.instance_func()

        # normal method / not link, 클래스로 호출 가능
        TEST.normal_func()

        # classmethod / class link, 인스턴스-클래스로 호출 가능
        self.class_sensor()
        TEST.class_sensor()

        return self.aa

print('classmethod - ', TEST.class_sensor())
print('staticmethod - ', TEST.static_sensor())
print('normal function - ', TEST.normal_func())

t = TEST()
t.get_ins()

print('classmethod - ', t.class_sensor())
print('staticmethod - ', t.static_sensor())
# 오류 - print('normal function - ', t.normal_func())
