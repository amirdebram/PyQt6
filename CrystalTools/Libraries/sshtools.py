#!/usr/bin/env python3

__author__ = 'Amir Debram'
__version__ = '1.0'
__email__ = 'amirdebram@gmail.com'

from paramiko import SSHClient, AutoAddPolicy, AuthenticationException, ssh_exception
from socket import timeout
import time

from PyQt6.QtWidgets import QMessageBox

class SecureShell(object):

    def __init__(self):
        super(SecureShell, self).__init__()

        self.client = SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
    
    def connect(self, *args):
        host = args[0][0]
        port = args[0][1]
        username = args[0][2]
        password = args[0][3]
        timeout = int(args[0][4])
        try:
            self.client.connect(host, port, username, password, timeout=timeout)
            return self.client
        except TimeoutError:
            self.error_Timeout()
        except AuthenticationException:
            self.error_Authentication()
        except ssh_exception.NoValidConnectionsError:
            self.error_Key_Exchange()
        except ssh_exception.SSHException:
            time.sleep(5)
            self.client.connect(host, port, username, password, timeout=timeout)
            return self.client

    def send_shell_commands(self, *args):
        try:
            with self.client.invoke_shell() as shell:
                shell.recv(65507)
                shell_response = []
                for command in args[0]:
                    shell.send(rf"{command}")
                    shell.send('\n')
                    shell.settimeout(5)
                    while True:
                        try:
                            shell_response.append(shell.recv(65507).decode('ascii'))
                            time.sleep(0.5)
                        except timeout:
                            break
            self.client.close()
            return shell_response
        except AttributeError:
            self.error_Connection()

    def clear_cups_spooler(self):
        try:
            commands = ["rm -rf /var/spool/cups/c*", "rm -rf /var/spool/cups/d*", "service cups restart", "logout"]
            for command in commands:
                self.client.exec_command(rf"{command}")
                self.client.exec_command("\n")
            QMessageBox.information(None, 'Spooler Cleared', f"Spooler has been cleared, and CUPS service has been restarted", QMessageBox.StandardButton.Ok)
            self.client.close()
        except AttributeError:
            self.error_Connection()

    def files_in_cups_spooler(self):
        try:
            sftp = self.client.open_sftp()
            path = '/var/spool/cups'
            files = sftp.listdir(path)
            if len(files) == 1:
                QMessageBox.information(None, 'Files in Spooler', 'Spooler is empty', QMessageBox.StandardButton.Ok)
            else:
                reply = QMessageBox.question(None, 'Files in Spooler', f"{len(files)-1} files in spooler.\nWould you like to clear the spooler?", 
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.Yes:
                    self.clear_cups_spooler()
                else:
                    pass
            sftp.close()
            self.client.close()
        except AttributeError:
            self.error_Connection()
    
    def list_cups_printers(self):
        try:
            command = "lpstat -v"
            stdin,stdout,stderr = self.client.exec_command(command)
            result = stdout.read().decode(encoding="ASCII").split('\n')
            msg = ""
            self.printerdata = []
            for x in result[:-1]:
                name, location = x.replace('device for ', '').split(': ')
                protocoltype, ip = location.replace('///', '//').split('://')
                self.printerdata.append([name, protocoltype, ip])
            self.client.close()
            return self.printerdata
        except AttributeError:
            self.error_Connection()
    
    def add_cups_printer(self, Printername: str, CUPS_Protocol: str, DeviceURI: str, Port: int, Username: str="", Password: str=""):
        match CUPS_Protocol:
            case "lpd":
                command = f"lpadmin -p {Printername} -m lsb/usr/cupsfilters/textonly.ppd -v lpd://{DeviceURI}/{Printername} -E -o printer-error-policy=retry-job"
            case "socket":
                if Port:
                    command = f"lpadmin -p {Printername} -m lsb/usr/cupsfilters/textonly.ppd -v socket://{DeviceURI}:{Port} -E -o printer-error-policy=retry-job"
                else:
                    command = f"lpadmin -p {Printername} -m lsb/usr/cupsfilters/textonly.ppd -v socket://{DeviceURI}/ -E -o printer-error-policy=retry-job"
            case "smb":
                command = " ".join(["lpadmin", "-p", Printername, "-E", "-v", "smb://"+Username+":"+Password+"@"+DeviceURI+"/"+Printername, "-o printer-error-policy=retry-job"])
            case _:
                pass
        try:
            stdin,stdout,stderr = self.client.exec_command(command)
            result = stdout.read().decode(encoding="ASCII").split('\n')
            stdin,stdout,stderr = self.client.exec_command("service cups restart")
            result = stdout.read().decode(encoding="ASCII").split('\n')
            QMessageBox.information(None, 'Printer Added', f"Printer [ {Printername} ] at {DeviceURI} has been added to CUPS", QMessageBox.StandardButton.Ok)
            return self.client.close()
        except AttributeError:
            self.error_Connection()

    def delete_cups_printer(self, Printername: str):
        if Printername == None:
            msg = f"You have not selected a valid printer, Please select a valid printer"
            QMessageBox.warning(None, 'Cannot Delete Printer', msg, QMessageBox.StandardButton.Ok)
            return self.client.close()
        reply = QMessageBox.question(None, 'Delete Printer', f"You are about to delete printer [ {Printername} ] from CUPS.\nWould you like to continue?", 
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            command = " ".join(["lpadmin", "-x", Printername])
            try:
                stdin,stdout,stderr = self.client.exec_command(command)
                result = stdout.read().decode(encoding="ASCII").split('\n')
                stdin,stdout,stderr = self.client.exec_command("service cups restart")
                result = stdout.read().decode(encoding="ASCII").split('\n')
                QMessageBox.information(None, 'Printer Deleted', f"Printer [ {Printername} ] has been deleted from CUPS", QMessageBox.StandardButton.Ok)
                return self.client.close()
            except AttributeError:
                self.error_Connection()
        else:
            self.client.close()
        
    def error_Connection(self):
        msg = f"Connection Could Not Be Established."
        QMessageBox.warning(None, 'Conection Error', msg, QMessageBox.StandardButton.Ok)
        return self.client.close()
    
    def error_Timeout(self):
        msg = f"Connection Timed Out, Check Host or Port"
        QMessageBox.warning(None, 'Timeout Error', msg, QMessageBox.StandardButton.Ok)
        return self.client.close()

    def error_Key_Exchange(self):
        msg = f"No matching key exchange method found."
        QMessageBox.warning(None, 'Key Exchange Error', msg, QMessageBox.StandardButton.Ok)
        return self.client.close()

    def error_Authentication(self):
        msg = f"Incorrect Username or Password."
        QMessageBox.warning(None, 'Authentication Error', msg, QMessageBox.StandardButton.Ok)
        return self.client.close()