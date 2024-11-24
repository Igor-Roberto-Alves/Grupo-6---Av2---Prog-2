#!/bin/bash

RED="\033[0;31m"
GREEN="\033[0;32m"
BLUE="\033[0;34m"
RESET="\033[0m"

UNIX_TIMESTAMP=$(date +%s)
DEFAULT_EACH_TIME=60

# flags
duration=""
amount=1
pass_n_flag=false
while [[ $# -gt 0 ]]; do
    case "$1" in
        --duration)
            if [[ -n "$2" && "$2" =~ ^[0-9]+$ ]]; then
                duration=$2
                shift 2
            else
                echo "Error: --duration requires a valid number."
                exit 1
            fi
            ;;
        --amount)
            if [[ -n "$2" && "$2" =~ ^[0-9]+$ ]]; then
                amount=$2
                shift 2
            else
                echo "Error: --amount requires a valid number."
                exit 1
            fi
            ;;
        -n)
            pass_n_flag=true
            shift
            ;;
        *)
            echo "Usage: $0 [--duration <time_in_seconds>] [--amount <number>] [-n]"
            exit 1
            ;;
    esac
done

# verificar se --duration foi fornecido
if [[ -z "$duration" ]]; then
    echo "Error: --duration argument is required."
    echo "Usage: $0 --duration <time_in_seconds> [--amount <number>] [-n]"
    exit 1
fi

# exibir as flags fornecidas
echo
echo -e "${BLUE}-----${RESET}"


if [[ -n "$amount" ]]; then
    echo -e "${BLUE}Simulations amount: ${GREEN}$amount${RESET}"
fi
echo -e "${BLUE}Simulation duration: ${GREEN}$duration${RESET}"
if $pass_n_flag; then
    echo -e "${RED}**Running with ${RESET}${RED}NO${RED} display**${RESET}"
fi

echo -e "${BLUE}-----${RESET}"
echo

# simulations

echo -e "${BLUE}Starting $amount simulation(s) simultaneously:${RESET}"
for i in $(seq $amount $END); do
    timestamp=${UNIX_TIMESTAMP}_${i}
    python_command="python mymesa.py -s $timestamp"
    if $pass_n_flag; then
        python_command+=" -n"
    fi

    timeout --foreground "$duration" $python_command &
done

wait

echo
echo -e "${GREEN}Simulation ended!${RESET}"


# graphs

echo
echo -e "${BLUE}Generating graphs:${RESET}"
for i in $(seq $amount $END); do
    timestamp=${UNIX_TIMESTAMP}_${i}
    python helpers/generate_graphs.py -f $timestamp &
done

wait

echo
echo -e "${GREEN}Graphs generated!${RESET}"