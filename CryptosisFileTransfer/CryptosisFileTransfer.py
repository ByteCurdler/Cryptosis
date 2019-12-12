import random, socket, base64

def hsh(n):
    tmp = 0
    for i in n:
        tmp *= 256
        tmp += i
    return tmp

def encode(n, k):
    random.seed(hsh(k))
    f = bytearray()
    for i in n:
        f.append((i+random.randint(0,255))%256)
    return f

def encode(n, k):
    random.seed(hsh(k))
    f = bytearray()
    for i in n:
        f.append((i-random.randint(0,255))%256)
    return f

def randKey(leng):
    tmp = bytearray()
    for i in range(leng):
        tmp.append(random.randint(0, 255))
    return tmp

def transfer(isHost, host=socket.gethostname(), port=8082, file=None):
    def send(data, conn):
        conn.send(data)
        
    def recv(conn):
        return bytearray(conn.recv(256))
        
    if isHost:
        s = socket.socket()
        s.bind((host, port))
        s.listen(1)
        c, addr = s.accept()
        print("Connection from: " + addr[0] + ":" + str(addr[1]))
        pKey = randKey(256)
        myKey = randKey(1024)
        
        # Send PK
        send(pKey, c)
        # Recv' PK%client
        data = recv(c)
        if not data:
            c.close()
        sKey = encode(data, myKey)
        # Send PK%host
        send(encode(pKey, myKey), c)
        data = bytearray(open(file, "rb").read())
        # Send len
        c.send(str(len(data)).encode("ascii"))
        # Recv' ACK
        c.recv(3)
        # Send filename
        c.send(file.split("/")[-1].encode("utf-8"))
        # Recv' ACK
        c.recv(3)
        # Send file
        send(data, c)
        c.close()
    else:
        c = socket.socket()
        c.connect((host, port))
        myKey = randKey(1024)
        # Recv' PK
        pKey = recv(c)
        # Send PK%client
        send(encode(pKey, myKey), c)
        # Recv' PK%host
        data = recv(c)
        sKey = encode(data, myKey)
        # Recv' len
        leng = int(c.recv(256))
        # Send ACK
        send(b'ACK', c)
        # Recv' filename
        name = c.recv(1024).decode("utf-8")
        # Send ACK
        send(b'ACK', c)
        # Recv' file
        data = bytearray(c.recv(leng))
        f = open("Recv'd/" + name, "wb")
        f.write(data)
        f.close()
        c.close()

if __name__ == "__main__":
    isHost = input("Is Host? (Y/n) ").upper().startswith("Y")
    port = int(input("Port? "))
    file = None
    host = socket.gethostname()
    if isHost:
        file = input("File to transfer? ")
    else:
        host = input("Host IP? ")
    transfer(isHost, port=port, file=file, host=host)
