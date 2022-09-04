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
exit $success
}

Check_AdminRights
