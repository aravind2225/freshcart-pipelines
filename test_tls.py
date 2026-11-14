
import socket
import ssl

hostname = "warthog-01.lmq.cloudamqp.com"
port = 5671

try:
    print("Connecting to individual CloudAMQP host...")

    context = ssl.create_default_context()

    with socket.create_connection(
        (hostname, port),
        timeout=15
    ) as sock:

        print("TCP connection successful!")

        with context.wrap_socket(
            sock,
            server_hostname=hostname
        ) as tls:

            print("TLS handshake successful!")
            print("TLS Version:", tls.version())
            print("Cipher:", tls.cipher())

except Exception as e:

    print("TLS connection failed!")
    print(type(e).__name__, repr(e))
