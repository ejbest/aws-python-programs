import sys
import base64

sInputFileName	= sys.argv[1]
sOutputFileName	= sys.argv[2]

oInputFile=open( sInputFileName, 'rb' )
oInputFileData	= oInputFile.read()

decodedFileData	= base64.decodebytes( oInputFileData )
oInputFile.close()

print( decodedFileData )

oOutputFile	= open( sOutputFileName,'xb' )
oOutputFile.write( decodedFileData )
oOutputFile.close()