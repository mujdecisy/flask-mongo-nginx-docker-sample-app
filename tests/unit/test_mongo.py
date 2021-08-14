import unittest, yaml, os
from flaskmgnd.util.damongo import DaMongo

class TestPojo(unittest.TestCase):
        
    def test_01insert(self):
        res = self.m.insert(self.col, [self.d])
        self.ids += res
        self.assertFalse(len(self.ids) < 1)

    def test_02select(self):
        res = self.m.select(self.col, self.d, with_id=True)
        self.assertEqual(res[0]["_id"], self.ids[0])

    def test_03update(self):
        newval = "b str"
        self.m.update(self.col, self.d, {"a": newval})
        res = self.m.select(self.col, {"_id": self.ids[0]})
        self.assertEqual(res[0]["a"], newval)

    def test_04delete(self):
        res = self.m.delete(self.col, {"_id": self.ids[0]})
        self.assertFalse(res < 1)

    @classmethod
    def setUpClass(cls) -> None:
        cls.db = "unittestdb"
        cls.col = "unittestcollection"

        dp = os.path.dirname(os.path.abspath(__file__))
        with open( f"{dp}/../../instance/config.yml", "r") as fp:
            conf = yaml.safe_load(fp)
        conf["MONGO"]["database"] = cls.db

        cls.m = DaMongo(conf["MONGO"])
        cls.d = {"a": "a str", "b": 1, "c" : 0}
        cls.ids = []

    @classmethod
    def tearDownClass(cls) -> None:
        cls.m.client.drop_database(cls.db)