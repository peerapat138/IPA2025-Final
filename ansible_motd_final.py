import subprocess
import tempfile
import os

def set_motd(ip, message):
    try:
        inventory_content = f"""
        [all]
        {ip} ansible_user=admin ansible_password=cisco ansible_network_os=ios ansible_connection=network_cli
        """
        with tempfile.NamedTemporaryFile("w", delete=False) as temp_inventory:
            temp_inventory.write(inventory_content)
            temp_inventory_path = temp_inventory.name

        playbook_content = f"""
        - name: Configure MOTD
          hosts: all
          gather_facts: no
          connection: network_cli
          tasks:
            - name: Set MOTD banner
              ios_banner:
                banner: motd
                text: "{message}"
        """
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".yml") as temp_playbook:
            temp_playbook.write(playbook_content)
            temp_playbook_path = temp_playbook.name

        cmd = [
            "ansible-playbook",
            "-i", temp_inventory_path,
            temp_playbook_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            return f"Ok: success"
        else:
            return f"Error: cannot set MOTD"

    except Exception as e:
        return f"Error: {str(e)}"

    finally:
        if os.path.exists(temp_playbook_path):
            os.remove(temp_playbook_path)
        if os.path.exists(temp_inventory_path):
            os.remove(temp_inventory_path)
