import unittest


# Python tkinter hello world program 

from tkinter import Tk, Label

class TestName(unittest.TestCase):

    def test_HelloWorld(self):
        root = Tk() # TK Root-Widget
        a = Label(root, text ="Hello World") # TK widget, instantiated in root
        a.pack() 

        #print(a.configure().keys())
        root.mainloop() 



if __name__.__contains__("__main__"):
    unittest.main()
    # Run just 1 test.
    # unittest.main(defaultTest='TestFoo.test_foo', warnings='ignore')
