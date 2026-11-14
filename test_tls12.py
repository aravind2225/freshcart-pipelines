
import socket
import ssl

HOST = "warthog-01.lmq.cloudamqp.com"
PORT = 5671

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.minimum_version = ssl.TLSVersion.TLSv1_2
context.maximum_version = ssl.TLSVersion.TLSv1_2
context.load_default_certs()

try:
    print("Connecting to:", HOST)

    with socket.create_connection(
        (HOST, PORT),
        timeout=15
    ) as sock:

        print("TCP connection successful!")

        with context.wrap_socket(
            sock,
            server_hostname=HOST
        ) as tls:

            print("TLS handshake successful!")
            print("TLS version:", tls.version())
            print("Cipher:", tls.cipher())

except Exception as e:
    print("TLS 1.2 failed")
    print(type(e).__name__, repr(e))
