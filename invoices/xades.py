import os
import base64
import subprocess
import logging

class Xades(object):

    def sign(self, xml_document, file_pk12, password):
        """
        Metodo que aplica la firma digital al XML
        TODO: Revisar return
        """
        xml_str = xml_document.encode('utf-8')
        JAR_PATH = 'firma/firmaXadesBes.jar'
        JAVA_CMD = 'java'
        firma_path = os.path.join(os.path.dirname(__file__), JAR_PATH)
        command = [
            JAVA_CMD,
            '-jar',
            firma_path,
            xml_str,
            base64.b64encode(file_pk12),
            base64.b64encode(password)
        ]
        try:
            logging.info('Probando comando de firma digital')
            subprocess.check_output(command)
        except subprocess.CalledProcessError as e:
            returncode = e.returncode
            output = e.output
            logging.error('Llamada a proceso JAVA codigo: %s' % returncode)
            logging.error('Error: %s' % output)

        p = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        res = p.communicate()
        return res[0]