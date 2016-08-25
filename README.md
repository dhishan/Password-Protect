# Implementation Project
## Password Protect

> Dhishan Amaranath   
> N16909360

## Introduction

Password protect is a command line utility to save all your passwords in one place. It uses complex algorithms and cryptography tools to store the passwords. It protects all data using a single _[Master Password]_ . The data is only accessible only from this application run on the **same host** with the same Master password.

**Features:**
- Store username and password combination in either of CBC,ECB and CTR modes
- Retrieve or verify your passwords for a given username
- Protection against brute force
- Protection against stolen master key
- Completely Erases the data if stored data is tampered.

## Usage
#### _this is all you need to know_

The application is bundled with a source and dependencies, a file for storing encrypted data. It is a python based application and needs python to be installed in your system and a path in the bin directory. Precautions are taken to make it compatible for OSX and Linux based systems. Tested on OSX.

Running for the first time, the application asks for creation of master password

![][firstrun]

The application then provides itself with an option to either store a password, Retrieve a stored password or check for validity of the password, Each option triggered by the first letter of the option

### Storing a Password `s`

Then upon providing the username and passwords to save, The application provides an option to use either of the encryption modes **ECB,CBC** and **CTR** for encrypting the password against the provided username

![][options]

### Retrieving a Password `r`

The Application upon providing `r` as the option, it asks for the username for which the password wants to be retrieved and displays passwords for all matching usernames

![][retrieve]

### Verifying Passwords `c`

With option `v` The application verifies the validity of the password from the database

![][validity]

![][full]
## Protection
#### _Protecting the protector_

### Saving the master Key

The access to the application and its data are mainly based on master key. A key component in the application. Saving the master key in the data is a dangerous move. To make the hacker job harder if he had access to the master key, an another layer of security is making the application and master key dependent on the system.

The master key entered by the user is concatenated with the unique ID of the system [MAC address] and hashed using `SHA256` and stored in the application data. **So now even though the hacker knew the master key, he cant decrypt the passwords as long as he run the application in the same system.**

### Same username and password combinations but saved differently

If two usernames have the same passwords, and are encrypted using the same mode and same key their encryption would be same. In order to differentiate and make the hacker job harder, the application uses a unique integer for each username password pair and generates the key for the encryption. **Thus for any pair the saved encrypted password would appear differently in the file.**


### Not saving the Keys

The encryption and decryption mainly depends on the `key` used. Storing the key in any form is dangerous, even in the application binary.
With the same username and the unique number the algorithm can be triggered to generate the same key again _on the fly_ and then use it to decrypt the password.
**Since the key is generated _on the fly_ for encrypting and decrypting we are eliminating the need to save the key.**


## Working
#### _Dig Deep_

### Overview
The core of the application is the Pycrypto library and Two custom random string generation algorithms. The application stores the usernames and the passwords in a file located along with the application data. The data stored consists of the username and certain details required for the decryption of the passwords for that username.


### Modularity
The application is divided modularly into
- Cryptography
- Special Algorithms
- File Operations

**Cryptography:**

There are three Modes available for encrypting the passwords
**CBC & ECB** [_Block Modes_] and **CTR** [_Stream Mode_]. The python built in Pycrypto module provides the use of the above three using AES Symmetric encryption.
For each of these modes the required component is the **key** for encryption. And the **CBC** mode needs an IV, an initial vector.
Block Modes also have a requirement on the size of the data to be encrypted. These has to be in multiples of `block_size` parameter usually `16`. These leads us to a new problem of padding the data. This is done by special Algorithms described below

**Special Algorithms:**
_Hide data in plain sight_

This application implements two special algorithms for generating random strings based on an integer value.**The speciality of this random string generator is, it generates the same set of random string irrespective of nth run for the same set of arguments.**

> Applications of the Algorithms:
> - Generate Key for encryption and decryption on the fly
> - Generate padding string to extend the password to match block_size
> - Generate initial vector uniquely
> - Eliminating the need to store the keys in file.

**Unique Repeatable Random String Algorithms:**

_Algorithm 1:_
```python
def randomString1(ivn,length):
    rstring = ""
    rnum = ivn
    counter = 1
    while(len(rstring) < length):
        rchar = chr(rnum % 74 + 48)
        rstring += rchar
        rnum += 2
        rnum *= 7
        rnum /= counter
        counter += 1
        if(rnum <= 1):
            rnum = ivn + 2
    return rstring
```
The above algorithm takes two arguments, an integer `ivn` and the length of the random string to be generated `length`. The random string generated can consists of all readable Ascii ranging from `48` to `122`. The algorithm performs certain mathematical operations on the `ivn` recursively and generates ascii characters. Therefore as long as you provide the same `ivn` the characters generated will be the same sequence.
Using this algorithm the probability of overlapping is `74/(possible ivns)` So eventually the probability will come to the `74/probability of getting the same random number`

_Algorithm 2:_ A slight different version of the above.
```python
def randomString2(ivn,length):
    rstring = ""
    rnum = ivn
    counter = 1
    while(len(rstring) < length):
        rchar = chr(rnum % 74 + 48)
        rstring += rchar
        rnum += 5
        rnum *= 3
        rnum /= counter
        counter += 1
        if(rnum <= 1):
            rnum = ivn + 2
    return rstring
```

**File Operations:**

This module handles the operation of files using the _os_ python library. It also erases the content of the file if the master password is tampered and a new one is provided. All the data in the files are in JSON format for portability.

**Data Format:**
**Sample:**
```json
[{"msp": "7a36650566715e48b8da3506e509bfd5490d92e34214b1c26e703b8a15ff055a"},
{"uname": "dhishan", "ivn": 3416, "plen": 9, "mode": 1, "lpass": [132, 174, 111, 89, 30, 170, 207, 130, 9, 42, 41, 225, 69, 196, 14, 217]},
{"uname": "dhishan", "ivn": 6939, "plen": 9, "mode": 6, "lpass": [225, 155, 109, 182, 53, 2, 71, 181, 248, 152, 147, 1, 220, 206, 228, 77]}]
```
The data corresponding to the `msp` key is the hash value of the master password. Each of the following _JSON_ objects corresponds to a individual username and password pair. The `uname` is the username, `ivn` is the 4 digit random number used in special algorithms and the `plen` is the original password length and the `lpass` is the list of the ascii characters of the encrypted password.


### Known Security Flaws

- The file saved itself is not encrypted, Even though the passwords are encrypted the username and ivn fields are visible
- The encryption of passwords are dependent on username and ivn alone, Master password and getnode should be incorporated to encrypt the passwords

### Possible scope for Further Developments

- Option to list all usernames
- Option to save the additional details for a given pair to distinguish between same usernames
- Name matching from partial data
- Option to delete

### Known Bugs

- Passwords are assumed to be of maximum length 16 bytes, Might lead to unexpected behaviors if exceeded

[//] : #
[firstrun] : <http://i.imgur.com/iykrWcN.png>
[options] : <http://i.imgur.com/YgFVHup.png>
[retrieve]: <http://i.imgur.com/arMdlw0.png>
[validity] : <http://i.imgur.com/FeNZl8F.png>
[full] : <http://i.imgur.com/t2JDlxi.png>
