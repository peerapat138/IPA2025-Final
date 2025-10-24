import subprocess
# import os

# EXPECTED_FILENAME='show_run_66070138_R3-Exam.txt'

def showrun():
    # if os.path.exists(EXPECTED_FILENAME): #มีเพื่อทำการลบไฟล์เดิมที่ชื่อซ้ำกับคีย์ที่ใส่ไป เพื่อให้มันเขียนมาใส่ไฟล์ใหม่
    #     os.remove(EXPECTED_FILENAME) #แต่ถ้าไม่ใช้จะเป็นการทับไปเลย
    # read https://www.datacamp.com/tutorial/python-subprocess to learn more about subprocess
    command = ['ansible-playbook', 'playbook.yaml']
    result = subprocess.run(command, capture_output=True, text=True)
    result = result.stdout
    print(result)
    if 'ok=2' in result:
        return "ok"
    else:
        return "Error: Ansible"
