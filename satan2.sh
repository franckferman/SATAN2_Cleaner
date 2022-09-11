#!/usr/bin/env bash
#: satan2.sh

red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

error=77
success=0

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

Ask_Yes_Or_No()
{
read -p "Are you sure you want to continue (nN/yY): " answer
case $answer in
[Yy]* ) ;;
[Nn]* ) echo;echo "Good luck to you.";exit$success;;
* ) echo "${red}A choice is required.${reset}";echo;Ask_Yes_Or_No
esac
}

Check_agreement()
{
Get_Banner
echo "${red}This product is designed for legal purposes only. 
Any use of this product outside of a legal framework is strictly prohibited. 
This product is intended for use by law enforcement, security professionals, and licensed individuals only. 
By using this product, you agree to abide by all local, state, and federal laws.${reset}";echo
Ask_Yes_Or_No
}

Check_dependencies()
{
satan2dir=/mnt/satan2

clear
echo "Check dependencies..."
if command -v zuluCrypt-cli>/dev/null 2>&1;then
    echo "${green}zuluCrypt-cli found.${reset}"
else
    echo "${red}Error, missing dependencies.${reset}"
    echo "${red}zuluCrypt-cli not found.${reset}"
    exit $error
fi

if command -v cryptsetup>/dev/null 2>&1;then
    echo "${green}cryptsetup found.${reset}"
else
    echo "${red}Error, missing dependencies.${reset}"
    echo "${red}cryptsetup not found.${reset}"
    exit $error
fi
echo;echo
}

Get_Banner()
{
cat << "EOF"
                            ,-.                            
       ___,---.__          /'|`\          __,---,___       
    ,-'    \`    `-.____,-'  |  `-.____,-'    //    `-.    
  ,'        |           ~'\     /`~           |        `.  
 /      ___//              `. ,'          ,  , \___      \ 
|    ,-'   `-.__   _         |        ,    __,-'   `-.    |
|   /          /\_  `   .    |    ,      _/\          \   |
\  |           \ \`-.___ \   |   / ___,-'/ /           |  /
 \  \           | `._   `\\  |  //'   _,' |           /  / 
  `-.\         /'  _ `---'' , . ``---' _  `\         /,-'  
     ``       /     \    ,='/ \`=.    /     \       ''     
             |__   /|\_,--.,-.--,--._/|\   __|             
             /  `./  \\`\ |  |  | /,//' \,'  \             
            /   /     ||--+--|--+-/-|     \   \            
           |   |     /'\_\_\ | /_/_/`\     |   |           
            \   \__, \_     `~'     _/ .__/   /            
             `-._,-'   `-._______,-'   `-._,-'             

              __  ___  _____  ___  __  __ 2
             ((  ||=||  ||   ||=|| ||\\||  
            \_)) || ||  ||   || || || \||
EOF
echo;echo
}

main()
{
clear
Check_agreement
Check_dependencies
Get_Banner

echo "List of disks: ";echo"";lsblk -d|tail -n+2|awk '{print $1" "$4}'|nl -v 0 -w2 -s'> ';echo "";read -p "Your choice: " userchoice
disks=( $(lsblk -d|tail -n+2|awk '{print $1}') )
echo "${green}${disks[userchoice]} ${reset}selected."

echo;Ask_Yes_Or_No

echo;echo "Disk unmounting."
sudo umount /dev/${disks[userchoice]}

echo;echo "Disk formating."
sudo mkfs -t ext4 /dev/${disks[userchoice]} <<<y

if [[ ! -e $satan2dir ]]; then
    echo "SATAN2 file not detected, creation."
    sudo mkdir -p $satan2dir
else 
    echo "SATAN2 file detected, regeneration."
    sudo rm -Rf $satan2dir
    sudo mkdir -p $satan2dir
fi

echo;echo "Disk mounting."
sudo mount /dev/${disks[userchoice]} $satan2dir

echo;echo "Overwriting of data."
dd if=/dev/urandom of=/dev/${disks[userchoice]} bs=4096 status=progress
shred -n 2 -z -v /dev/${disks[userchoice]}

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
sudo zuluCrypt-cli -c -d /dev/${disks[userchoice]} -z ext4 -t tcrypt -g "/dev/urandom.serpent:twofish:aes.xts-plain64.256.whirlpool" -p $passwd -f ./satan2.sh -k

echo;echo "Disk formating."
sudo mkfs -t ext4 /dev/${disks[userchoice]} <<<y

if [[ ! -e $satan2dir ]]; then
    sudo mkdir -p $satan2dir
else
    sudo rm -Rf $satan2dir
    sudo mkdir -p $satan2dir
fi

echo;echo "Disk mounting."
sudo mount /dev/${disks[userchoice]} $satan2dir

echo;echo "Overwriting of data."
dd if=/dev/urandom of=/dev/${disks[userchoice]} bs=4096 status=progress
shred -n 3 -z -v /dev/${disks[userchoice]}

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

echo;echo "Generation of a keyfile."
SIZE=2048
OUTFILE=./satan2.key
dd if=/dev/urandom of=$OUTFILE bs=$SIZE count=1048576

echo;echo "Encryption of the hard disk."
sudo zuluCrypt-cli -c -d /dev/${disks[userchoice]} -z ext4 -t luks -p $passwd -f $OUTFILE -k

echo;echo "Disk formating."
sudo mkfs -t ext4 /dev/${disks[userchoice]} <<<y

if [[ ! -e $satan2dir ]]; then
    sudo mkdir -p $satan2dir
else
    sudo rm -Rf $satan2dir
    sudo mkdir -p $satan2dir
fi

echo;echo "Disk mounting."
sudo mount /dev/${disks[userchoice]} $satan2dir

echo;echo "Overwriting of data."
dd if=/dev/urandom of=/dev/${disks[userchoice]} bs=4096 status=progress
shred -n 2 -z -v /dev/${disks[userchoice]}

echo;echo "Disk unmounting."
sudo umount $disk /dev/${disks[userchoice]}

echo;echo "Generation of a keyfile."
SIZE=2048
OUTFILE=sarmat.bin
dd if=/dev/urandom of=$OUTFILE bs=$SIZE count=2097152

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

echo;echo "Encryption of the used keyfile."
sudo zuluCrypt-cli -c -d ./satan2.key -z ext4 -t luks -p $passwd -f $OUTFILE -k

echo;echo "Overwrite the used keyfile."
shred -n 8 -z -v ./satan2.key

echo;echo "Disk unmounting."
sudo umount /dev/${disks[userchoice]}

echo;echo "Disk formating."
sudo mkfs -t ext4 /dev/${disks[userchoice]} <<<y

if [[ ! -e $satan2dir ]]; then
    sudo mkdir -p $satan2dir
else 
    sudo rm -Rf $satan2dir
    sudo mkdir -p $satan2dir
fi

echo;echo "Disk mounting."
sudo mount /dev/${disks[userchoice]} $satan2dir

echo;echo "Overwriting of data."
dd if=/dev/urandom of=/dev/${disks[userchoice]} bs=4096 status=progress
shred -n 2 -z -v /dev/${disks[userchoice]}

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

echo;echo "Encryption of the hard disk using cryptsetup."
echo $passwd|sudo cryptsetup -y -v luksFormat /dev/${disks[userchoice]}
passwd="$(echo $passwd|rev)"
echo $passwd|sudo cryptsetup -y -v luksFormat /dev/${disks[userchoice]}

echo;echo "Disk formating."
sudo mkfs -t ext4 /dev/${disks[userchoice]} <<<y

if [[ ! -e $satan2dir ]]; then
    sudo mkdir -p $satan2dir
else
    sudo rm -Rf $satan2dir
    sudo mkdir -p $satan2dir
fi

echo;echo "Disk mounting."
sudo mount /dev/${disks[userchoice]} $satan2dir

echo;echo "Overwriting of data."
dd if=/dev/urandom of=/dev/${disks[userchoice]} bs=4096 status=progress
shred -n 2 -z -v /dev/${disks[userchoice]}

echo;echo "Disk unmounting."
sudo umount /dev/${disks[userchoice]}

exit $success
}

Check_AdminRights