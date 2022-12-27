import os
import base64
import subprocess
import logging

class Xades(object):

    # def sign(xml_document):
    #     """
    #     Metodo que aplica la firma digital al XML
    #     TODO: Revisar return
    #     """
    #     file_pk12 = "invoices/firma/5760703_identity.p12"
    #     password = "owq9128"

    #     xml_str = xml_document.encode('utf-8')
    #     JAR_PATH = 'firma/firmaXadesBes.jar'
    #     JAVA_CMD = 'java'
    #     firma_path = os.path.join(os.path.dirname(__file__), JAR_PATH)
    #     print(firma_path)
    #     command = [
    #         JAVA_CMD,
    #         '-jar',
    #         firma_path,
    #         xml_str,
    #         base64.b64encode(file_pk12),
    #         base64.b64encode(password)
    #     ]
    #     try:
    #         logging.info('Probando comando de firma digital')
    #         subprocess.check_output(command)
    #     except subprocess.CalledProcessError as e:
    #         returncode = e.returncode
    #         output = e.output
    #         logging.error('Llamada a proceso JAVA codigo: %s' % returncode)
    #         logging.error('Error: %s' % output)

    #     p = subprocess.Popen(
    #         command,
    #         stdout=subprocess.PIPE,
    #         stderr=subprocess.STDOUT
    #     )
    #     res = p.communicate()
    #     return res[0]

    def apply_digital_signature(self, access_key, file_pk12, password):
        """
        Metodo que aplica la firma digital al XML
        """
        OPT_PATH = os.path.join(os.path.abspath(os.curdir),'invElect\\')
        JAR_PATH = 'firma\\firmaXadesBes.jar'
        JAVA_CMD = 'java'
        file_pk12 = os.path.join(os.path.dirname(__file__), 'firma\\5760703_identity.p12')
        ds_document = False
        name = '%s%s.xml' % (OPT_PATH, access_key)
        print(name)
        print(file_pk12)
        # firma electrónica del xml
        firma_path = os.path.join(os.path.dirname(__file__), JAR_PATH)
        print(firma_path)
        # invocación del jar de la firma electrónica
        subprocess.call([JAVA_CMD, '-jar', firma_path, name, name, file_pk12, password], shell=True)
        return ds_document