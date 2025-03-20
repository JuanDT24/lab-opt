#!/bin/bash

clear

while true; do
    echo "Selecciona una opción:"
    echo "Punto 1"
    echo "Punto 2"
    echo "Punto 3"
    echo "Punto 4"
    echo "Salir"
    read opcion

    case $opcion in
        1)
            python3 punto1.py 2>/dev/null
            clear
            ;;
        2)
            python3 punto2.py 2>/dev/null
            clear
            ;;

        3)
            python3 punto3.py 2>/dev/null
            clear
            ;;

        4)
            python3 punto4.py 2>/dev/null
            clear
            ;;

        5)
            break
            ;;
        *)
            echo "Opción incorrecta"
            ;;

    esac
    clear
done
