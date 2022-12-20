"""FIRMADO DE ARCHIVOS XML"""
"""ESTADO: FALTA COMPROBAR CON WS DE SRI"""

from signxml import XMLSigner, XMLVerifier
import xml.etree.ElementTree as ET
from OpenSSL import crypto
import os

def firmar_xml(xml_filename):
    """ RETORNA XML STRING FIRMADO """
    # clave = "sf3LnaMZMz"
    clave = "owq9128"
    with open("invoices/firma/5760703_identity.p12", "rb") as file:
        p12 = crypto.load_pkcs12(file.read(), clave.encode())

    key = crypto.dump_privatekey(crypto.FILETYPE_PEM, p12.get_privatekey())
    cert = crypto.dump_certificate(crypto.FILETYPE_PEM, p12.get_certificate())

    # archivod de prueba
    filename = xml_filename

    root = ET.parse(filename).getroot()

    # sha1 por defecto
    final_firmado = XMLSigner().sign(root, key=key, cert=cert)

    # verified_data = XMLVerifier().verify(signed_root).signed_xml
    # print (final_firmado.values)

    # xml_str = xml.etree.ElementTree.tostring(signed_root, encoding='utf-8')
    xml_str = ET.tostring(final_firmado)
    #print (xml_str.decode())
    final = str(xml_str.decode())
    final2 = final.replace('ns0', 'ds')
    return final2


"""abre un xml,lo firma y guarda en otro xml"""


def save_xml_firmado(xml_firmado_name, xml_origen):
    """name : xxxxx.xml"""
    file1 = open(xml_origen, "w")
    # file1.write(str(xml_str))
    file1.write(firmar_xml(xml_origen))
    file1.close()  # to change file access modes
    pass

# print (firmar_xml("new.xml"))
