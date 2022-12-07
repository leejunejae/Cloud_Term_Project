from sshtunnel import SSHTunnelForwarder
import pymysql

with SSHTunnelForwarder(
        ('ec2-43-201-22-33.ap-northeast-2.compute.amazonaws.com'),
        ssh_username="aws-htcondor-master",
        ssh_pkey="/test.pem",
        remote_bind_address=('ec2apnortheast2.amazonaws.com', 3306)
) as tunnel:
    print("== SSH Tunnel ==")

    db = pymysql.connect(
        host='127.0.0.1', user="root",
        password="1234", port=9618
    )
    # Run sample query in the database to validate connection
    try:
        # Print all the databases
        with db.cursor() as cur:
            cur.execute('SHOW DATABASES')
            for r in cur:
                print(r)
    finally:
        db.close()

print("SSH 터널링 완료 !!")