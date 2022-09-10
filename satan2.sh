#!/usr/bin/env bash
#: satan2.sh

red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

error=77

Check_AdminRights()
{
uid_root=0

    if [ "$UID" -ne "$uid_root" ]
        then
        echo "${red}Error, please run the script with sudo.${reset}"
        exit $error
    
    elif [ "$UID" -eq "$uid_root" ]
        then
        main

    else
        echo
        echo "${red}An unexpected error was caused.${reset}"
        exit $error

    fi
}

Check_dependencies()
{
success=0
satan2dir=/mnt/satan2

clear
echo "Check dependencies..."
if command -v zuluCrypt-cli>/dev/null 2>&1;then
    echo;echo "${green}zuluCrypt-cli found.${reset}"
else
    echo;echo "${red}Error, missing dependencies.${reset}"
    echo "${red}zuluCrypt-cli not found.${reset}"
    exit $error
fi
}

main()
{
Check_dependencies

echo "List of disks: ";echo"";lsblk -d|tail -n+2|awk '{print $1" "$4}'|nl -v 0 -w2 -s'> ';echo "";read -p "Your choice: " userchoice
disks=( $(lsblk -d|tail -n+2|awk '{print $1}') )
echo "${green}${disks[userchoice]} ${reset}selected."

echo;echo "Disk unmounting."
sudo umount /dev/${disks[userchoice]}

echo;echo "Disk formating."
sudo mkfs -t ext4 /dev/${disks[userchoice]} <<<y

if [[ ! -e $satan2dir ]]; then
    echo "SATAN2 file not detected, creation."
    sudo mkdir -p $satan2dir
else 
    echo "SATAN2 file detected, regeneration"
    sudo rm -Rf $satan2dir
    sudo mkdir -p $satan2dir
fi

echo;echo "Disk mounting."
sudo mount $disk /dev/${disks[userchoice]} $satan2dir

echo;echo "Overwriting of data."
dd if=/dev/urandom of=/dev/${disks[userchoice]} bs=4096 status=progress

passwd="$(openssl rand -base64 42 | tr -dc 'a-zA-Z0-9!@#$%^&*()_+-=')"
passwd="$(echo $passwd|rev)"
rand=$[($RANDOM%10)+1]
passwd="$(echo $passwd|cut -c ${rand}-)"

passwd2="$(echo $passwd|base64)"
passwd2="$(echo $passwd2|rev)"
rand=$[($RANDOM%32)+1]
passwd2="$(echo $passwd2|cut -c ${rand}-)"
passwd=$passwd2$passwd
passwd="$(echo $passwd|rev)"
rand=$[($RANDOM%10)+1]
passwd="$(echo $passwd|cut -c ${rand}-)"

echo;echo "Disk unmounting."
sudo umount $disk /dev/${disks[userchoice]}

echo;echo "Encryption of the hard disk (SERPENT(TWOFISH(AES)))."
sudo zuluCrypt-cli -c -d /dev/sdb -z ext4 -t tcrypt -g "/dev/urandom.serpent:twofish:aes.xts-plain64.256.whirlpool" -p $passwd -f ./satan2.sh -k

exit $success
}

Check_AdminRights
