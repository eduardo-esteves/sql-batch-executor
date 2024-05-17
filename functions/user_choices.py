def get_user_option() -> int:
    """
    Prompts the user to select an option for the execution mode.

    Returns:
        int: The selected option.
    """

    print('Please choose one of the numbers representing the following options before updating the Database:\n')

    while True:
        try:
            option = int(input(
                '1 - Pre-installed database, update and create new tables\n'
                '2 - Database without dependencies on new tables needing to be updated\n'
                'Enter your choice: '
            ))

            print()

            if option in {1, 2}:
                return option
            else:
                print("Invalid option. Please enter 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        print()
