from http.server import BaseHTTPRequestHandler
import qrcode
import io
import urllib.parse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Analizar la URL y los parámetros de consulta
            parsed_path = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_path.query)
            
            # Obtener el parámetro 'text', por defecto usa un enlace de ejemplo
            text_to_encode = query_params.get('text', ['https://github.com'])[0]
            
            # Generar la imagen del código QR
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=4,
            )
            qr.add_data(text_to_encode)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Guardar la imagen en un buffer de memoria en bytes
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_bytes = buffered.getvalue()
            
            # Enviar la respuesta HTTP exitosa con la imagen PNG
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            self.wfile.write(img_bytes)
            
        except Exception as e:
            # Manejo básico de errores
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"Error interno: {str(e)}".encode('utf-8'))
        
        return
