# getsos
A tool to collect sosreports from multiple machines.

## Prerequisites
1. Python 3.x
2. passwordless ssh to all the machines.

## Installation
1. Download the project files from github.
```
# git clone https://github.com/kshithijiyer/getsos.git
```
2. Change directory to the project directory. 
```
# cd  getsos
```
3. Now run the installation script.
```
# python3 setup.py install
```
4. To check run ``` getsos --help ```

## Usage
There are 2 ways of using the tool. 
1. Passing IP addresses through command line seperated by comma(,):
```
# getsos -m machine_1,machine_2,machine_3 
```
2. Passing a file with all the IP addresses sepearted by comma(,):
```
# cat config_file
machine_1,machine2,machine3,
machine4,machine5
machine6
# getsos -f config_file
```
**Note**: 
The default user used by the script is __root__ but can be changed using the ```-u``` or ```--username``` option. 
The default destination directory is __.__ (present dir) ```-d``` or ```--dist-dir``` option.

## Built with 
[IDLE 3](https://www.python.org/downloads/)

## Author
[Kshithij Iyer](https://www.linkedin.com/in/kshithij-iyer/)

## Licence 
The project is released under BSD 2-Clause "Simplified" License.
