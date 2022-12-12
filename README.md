# BoxDrop - A DropBox Clone

BoxDrop is a file synchronisation service which helps users sync their files across multiple devices. BoxDrop uses an efficient file chunking algorithm which saves badnwidth and storage by uploading duplicate data within a file only once and updating only those chunks in the cloud which have been changed on the users' device.

## Usage Instructions

To install and use BoxDrop, you need either a MacOS or a Linux system. We assume that you also have `python3` and `virtualenv` installed on your system.

First, clone the repository on to your system. Then follow the following instructions:

```
cd boxdrop
chmod u+x install.sh
chmod u+x run.sh
./install.sh
./run.sh
```

The BoxDrop client will start and you will be asked to either create an account or to login to an existing account. After loggin in, the BoxDrop client will create a folder in your home directory called `BoxDrop<random_id_characters>`. Once the initialisation process is complete, the client will start monitoring your BoxDrop directory for changes. You can start copying files into this folder to upload them.

You can repeat the same process on another device and you will see that BoxDrop automatically synchronizes both the devices over the internet. So, all your changes made on any one of your devices will be communicated to all your other devices and thus all your files will remain in sync across your multiple devices.