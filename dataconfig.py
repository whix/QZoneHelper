#coding:UTF8
import traceback


class Config:

    def __init__(self):

        self.CONFIG_PATH = "config"
        self.config = {}
        self.decode = lambda x: x.decode("zlib")
        self.encode = lambda x: x.encode("zlib")
        self.read()

    def write(self):
        try:
            with open(self.CONFIG_PATH, "wb") as f:
#                print Recorder.config
                data = str(self.config)
                data = self.encode(data)
                f.write(data)
        except:
            traceback.print_exc()

    def read(self):
        try:
            with open(self.CONFIG_PATH, "rb") as f:
                data = f.read()
                data = self.decode(data)
                self.config = eval(data)
        except:
            traceback.print_exc()

    def get(self, key, default={}):

        #print self.config
        if not self.config.has_key(key):
            self.config[key] = default

        return self.config[key]


    def __setitem__(self, key, value):

        self.config[key] = value



if "__main__" == __name__:

    test = Config()
    test["a"] = "a"
    print test["a"]
