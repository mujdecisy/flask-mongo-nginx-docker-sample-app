import unittest
from flaskmgnd.util.pojo import Pojo

class B(Pojo):
    ba: str
    bb: int
    def __init__(self, ba: str, bb: int, data:str = None, fromclass = None) -> None:
        self.ba, self.bb = ba, bb
        return super().__init__(data, fromclass)
                
class A(Pojo):
    a: str
    b: int
    c: float
    d: B
    def __init__(self, a:str, b:int, c:float, d:B, data:str = None, fromclass = None) -> None:
        self.a, self.b, self.c, self.d = a, b, c, d
        return super().__init__(data, fromclass)
    

class TestPojo(unittest.TestCase):
    def setUp(self) -> None:
        self.b = B("b str", 0)
        self.bdict = {
            "ba": "b str", 
            "bb": 0
        }

        self.a = A("a str", 1, 2.5, self.b)
        self.adict = {
            "a" : "a str",
            "b" : 1,
            "c" : 2.5,
            "d" : self.bdict
        }

    def test_01todict(self):
        r = self.a.to_dict()
        self.assertEqual(r, self.adict)

    def test_02fromdict(self):
        r = A(None, None, None, None, self.adict, A)
        self.assertEqual(r.to_dict(), self.a.to_dict())
