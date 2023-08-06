#-*- coding: utf-8 -*-
"""
@author:MD.Nazmuddoha Ansary
"""
from __future__ import print_function
#-------------------------------------------
# imports
#-------------------------------------------
import os 
import unittest
from wordCleaner import WordCleaner 
WC=WordCleaner()
#-------------------------------------------
# unittestcase
#-------------------------------------------
class TestWordCleaner(unittest.TestCase):
    def test_values(self):
        '''
            test known failure cases
        '''
        # case:unwanted doubles
        ## (a)'যুুদ্ধ'==(b)'যুদ্ধ'
        self.assertEqual(WC.clean('যুুদ্ধ'),'যুদ্ধ')
        ## (a)'দুুই'==(b)'দুই'
        self.assertEqual(WC.clean('দুুই'),'দুই')
        # case:unwanted middle connector '্'  
        ## (a)'চু্ক্তি'==(b)'চুক্তি' 
        self.assertEqual(WC.clean('চু্ক্তি'),'চুক্তি')
        ## (a)'যু্ক্ত'==(b)'যুক্ত' 
        self.assertEqual(WC.clean('যু্ক্ত'),'যুক্ত')
        # case: replace broken diacritic 
        ## (a)'আরো'==(b)'আরো'
        self.assertEqual(WC.clean('আরো'),'আরো')
        ## (a)'পৌঁছে'== (b)'পৌঁছে'
        self.assertEqual(WC.clean('পৌঁছে'),'পৌঁছে')
        ## (a)সংস্কৄতি==(b)সংস্কৃতি
        self.assertEqual(WC.clean('সংস্কৄতি'),'সংস্কৃতি')
        # case: nukta  
        ## (a)কেন্দ্রীয়==(b)কেন্দ্রীয়
        self.assertEqual(WC.clean('কেন্দ্রীয়'),'কেন্দ্রীয়')
        ## (a)রযে়ছে==(b)রয়েছে
        self.assertEqual(WC.clean('রযে়ছে'),'রয়েছে')
        ## (a)জ়ন্য==(b)জন্য
        self.assertEqual(WC.clean('জ়ন্য'),'জন্য')
        ## missed case
        self.assertEqual(WC.clean('য়'),'য়')

        # case: invalid hosonto after or before symbols
        ## (a)এ্তে==(b)এতে
        self.assertEqual(WC.clean('এ্তে'),'এতে')
        ##(a)নেট্ওয়ার্ক==(b)নেটওয়ার্ক
        self.assertEqual(WC.clean('নেট্ওয়ার্ক'),'নেটওয়ার্ক')
        
        ### case: Vowel Diacs after vowels (Also Normalizes 'এ' and 'ত্র')
        ## (a)উুলু==(b)উলু
        self.assertEqual(WC.clean('উুলু'),'উলু')
        ## (a)একএে==(b)একত্রে
        self.assertEqual(WC.clean('একএে'),'একত্রে')
        ## (a)একএ==(b)একত্র
        self.assertEqual(WC.clean('একএ'),'একত্র')
        
        ### case: normalize to+hosonto
        ## (a)উত্স==(b)উৎস
        self.assertEqual(WC.clean('উত্স'),'উৎস')
        ## স্নাতকোত্ত্তর
        self.assertEqual(WC.clean('স্নাতকোত্ত্তর'),'স্নাতকোৎত্তর')
        
        
        ### case: multiple folas
        self.assertEqual(WC.clean('ন্দ্ব্ব্ব্ব্ব'),'ন্দ্ব')
        

        # Dummy Non-Bangla,Numbers and Space cases/ Invalid start end cases
        # english
        self.assertEqual(WC.clean('ASD1234'),None)
        # numbers
        self.assertEqual(WC.clean('১২৩'),None)
        # random
        self.assertEqual(WC.clean('টেলগ্রািফস্ট'),None)
        self.assertEqual(WC.clean('িত'),'ত')
        self.assertEqual(WC.clean('সং্যুক্তি'),"সংযুক্তি")
        # Ending
        self.assertEqual(WC.clean("অজানা্"),"অজানা")
        
    def test_types(self):
        '''
            test the invalid input types
        '''
        # int
        self.assertRaises(TypeError,WC.clean,123)
        # float
        self.assertRaises(TypeError,WC.clean,123.456)
        # boolean
        self.assertRaises(TypeError,WC.clean,True)
        # complex
        self.assertRaises(TypeError,WC.clean,3+4j)
        # list
        self.assertRaises(TypeError,WC.clean,['যুদ্ধ','চুক্তি'])

        
        
        


        
        
        
                


                
                