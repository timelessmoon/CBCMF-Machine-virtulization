# CBCMF-Machine-virtulization
3D printer and Robotic arm virtulization

This file is used for test machine to machine talking, which will initiated by cloud and be based on socket through local networks. For now it's only invlove two machines (one Bukito 3D printer, one Uarm-metal Robotic arm). 

Scenario:
The Scenario would be the user initial the machine to machine on cloud, which means the cloud would send corresponding Ip address to each machine as long as commands. While printing, the printer-raspberry pi would keep publish status-XML, after printing, the Robotic arm would be able to detect that changes, so it will automatically start it's movement.
