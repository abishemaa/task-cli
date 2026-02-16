

def main():
    print("Task-cli is running...")
    cli_input = input("Enter a command: ")
    cli_handle_input(cli_input)

def cli_handle_input(cli_input):
    value = cli_input.split()[0]
    case = {
        "help": cli_help,
        "exit": cli_exit,
        "add": cli_add,
        "list": cli_list,
        "remove": cli_remove,
    }

    func = case.get(value, cli_invalid_command)
    func(cli_input.split()[1:])  # Pass the arguments to the function





if __name__ == "__main__":    main()
