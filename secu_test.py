import unittest

import secu

class TestSecuMethods(unittest.TestCase):

    def test_xor(self):
        """
        Test de la function xor
        """
        self.assertEqual(secu.xor('0','0'), '0')
        self.assertEqual(secu.xor('0','1'), '1')
        self.assertEqual(secu.xor('1','0'), '1')
        self.assertEqual(secu.xor('1','1'), '0')
        
    def test_encrypt(self):
        """
        Test de la function encrypt
        """
        self.assertEqual(secu.encrypt('1110011','10'),'0100110')

    def test_to_bin(self):
        """
        Test de la function to_bin
        """
        self.assertEqual(secu.to_bin('0123'),'0000000100100011')

    def test_is_valid_ssid(self):
        """
        Test de la function is_valid_ssid
        """
        self.assertTrue(secu.is_valid_ssid('255081416802538'))
        self.assertFalse(secu.is_valid_ssid('255081468025455'))
        self.assertFalse(secu.is_valid_ssid('25508146802545'))

    def test_decode(self):
        """
        Test de la fonction decode
        """
        encoded = "101011110101101101111101110111111000001010101101001111111010"
        indice = '1980106'
        ssid,key = secu.decode(encoded,indice)
        self.assertEqual(ssid, "198010623476521")
        self.assertEqual(key,"10110110110110110110110110111101")

    def test_gen_key(self):
        """
        Test de la fonction gen_key
        """
        key = secu.gen_key()
        self.assertEqual(len(key),8)

    def test_gen_ssid(self):
        """
        Test de la fonction gen_ssid
        """
        ssid , err = secu.gen_ssid()
        if err != None:
            self.assertTrue(False)
        self.assertTrue(secu.is_valid_ssid(ssid))

    def test_process(self):
        """
        Test du process sur une centaine de cas tirés au hasard 
        """
        # iteration sur 100 cas
        for i in range(100):
            # tirage aleatoire d'un ssid
            key = str(secu.gen_key())
            # tirage aleatoire d'une clé
            ssid,err = secu.gen_ssid()
            if err == None :
                # codeage du ssid avec la clé
                encoded = secu.encrypt(secu.to_bin(str(ssid)),secu.to_bin(key))
                # decodage de la chaine encode à apartir d'un indice(7 premier chiffre du ssid)
                ssid2, key2 = secu.decode(str(encoded),str(ssid[0:7]))
                # verification du ssid calculé
                self.assertEqual(ssid,ssid2)
                # verification de la clé calculé
                self.assertEqual(secu.to_bin(key),key2)
                print("test ", i, "ssid:",ssid, "key:", key,"key en binaire:", secu.to_bin(key), "chaine encodée:",encoded, "indice:", str(ssid[0:7]), "ssid calculé:", ssid2, "clé calculée:", key2 )
            else:
                print("erreur dans la generation du ssid ",ssid)
                self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()