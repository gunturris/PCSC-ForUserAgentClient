import web
import string
import xml.etree.ElementTree as ET
import os
from smartcard.scard import *
import smartcard.util 
  
urls = (
    '/readers', 'list_readers',
    '/cardid', 'card_number'
)

app = web.application(urls, globals())
clear = lambda: os.system('cls')
clear()
msgText ='''
 #########################################################
 #                                                       #
 #  PC/SC JSserver 0.1 Beta                              #
 #  Developed by Guntur@Bumblebee                        #
 #                                                       #
 #  1. Pastikan smartcard reader terkoneksi dengan baik  #
 #  2. Pastikan browser web anda mendukung javascript    #
 #  3. Disarankan menggunakan chrome atau firefox        #
 #                                                       #
 #  Contact : gunturris@gmail.com                        #
 #                                                       #
 ######################################################### 
 Ctrl + C untuk keluar
'''
print msgText


class list_readers:        
    def GET(self):
		try:
			hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
			if hresult != SCARD_S_SUCCESS:
				raise Exception('Failed to establish context : ' + SCardGetErrorMessage(hresult))
			

			try:
				hresult, readers = SCardListReaders(hcontext, [])
				if hresult != SCARD_S_SUCCESS:
					raise Exception('Failed to list readers: ' + SCardGetErrorMessage(hresult)) 

				if len(readers) < 1:
					return 'No smart card readers'

				reader = readers[0]
				return reader 

			except:
				hresult = SCardReleaseContext(hcontext)
				if hresult != SCARD_S_SUCCESS:
					raise Exception('Failed to release context: ' +
							SCardGetErrorMessage(hresult))
				return 'Released context.'

		except Exception, message:
			return "Exception:", message
 

def jsload():
	#COMMAND = [0xFF, 0xCA, 0x00, 0x00, 0x04] #MifareUID
	COMMAND = [0xFF, 0xCA, 0x00, 0x00, 0x00] #MifareUID
	#COMMAND = [0xA0, 0xA4, 0x00, 0x00, 0x02, 0x3F, 0x00]
	#COMMAND = [0xA0, 0xC0, 0x00, 0x00, 0x20]

	try:
		hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
		if hresult != SCARD_S_SUCCESS:
			raise Exception('Failed to establish context : ' +	SCardGetErrorMessage(hresult))
		

		try:
			hresult, readers = SCardListReaders(hcontext, [])
			if hresult != SCARD_S_SUCCESS:
				raise Exception('Failed to list readers: ' + SCardGetErrorMessage(hresult)) 

			if len(readers) < 1:
				raise Exception('No smart card readers')

			reader = readers[0] 

			try:
				hresult, hcard, dwActiveProtocol = SCardConnect(hcontext, reader,SCARD_SHARE_SHARED, SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1)
				if hresult != SCARD_S_SUCCESS:
					#raise Exception('Unable to connect: ' + SCardGetErrorMessage(hresult))
					raise Exception("function getUIDCard(){$('#responeArea').val('Kartu tidak terdeteksi');")
				
				try:
					hresult, response = SCardTransmit(hcard, dwActiveProtocol,    COMMAND)
					if hresult != SCARD_S_SUCCESS:
						raise Exception('Failed to transmit: ' + SCardGetErrorMessage(hresult))
					
					hexdata = smartcard.util.toHexString(response ,smartcard.util.PACK)
					return int(hexdata , 16 ) 
				
				except Exception, message: 
					return message

			except Exception, message: 
				return message

		except Exception, message:
			#print message
			return  5 # 'Pembaca kartu tidak terdeteksi'

	except Exception, message:
		#print message
		return  3 #'Kesalan tidak dikenal'

 
def split_kode(kode):
	text = str(kode)
	if(len(text) < 4):
		return text
	else:
		kecil = text[-4:]
		besar = text[:-4]
		return split_kode(besar) + '-' + kecil
		
class card_number:        
    def GET(self):
		data = jsload() 
		if( data == 3 ):
			res = 'Kesalahan tidak dikenal'
			return ("function getUIDCard(){$('#responeArea').val('%s');}" ) % res 
		elif(data == 5 ):
			res  = 'Pembaca kartu tidak terdeteksi'
			return ("function getUIDCard(){$('#responeArea').val('%s');}" ) % res 
		else:   
			return   ("function getUIDCard(){$('#responeArea').val('%s');}" ) %  data 

 
if __name__ == "__main__":
    app.run()
