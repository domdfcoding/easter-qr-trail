# this package
from easter_qr_trail.qr import generate_qr_codes, generate_starter_qr

server_address = "http://192.168.1.50:8001"

generate_qr_codes(server_address)
generate_starter_qr(server_address)
