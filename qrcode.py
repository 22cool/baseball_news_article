import qrcode

#와이파이 정보
ssid = "와이파이 이름"
password = "비밀번호"
security_type = "WPA"

#QR 코드 데이터 생성
wifi_info = f"WIFI:T{security_type};S:{ssid};P:{password};;"

#QR코드 생성
qr = qrcode.make(wifi_info)

qr.save("wifi_qr.png")