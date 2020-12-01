def main():
    print("Hello World!")

    # Create state machine object
    # Initialize logger
    # Initialize signal handler
    # Parse config file
    # Initialize file change notifier on config file

    # LOOP START #

    # Watch dynamic config changes

    # ----------------#
    # -- Init State --#
    # ----------------#

    # Create data sets

    # ----------------#
    # -- Idle State --#
    # ----------------#

    # Wait for initialization

    # Go to Working

    # ( Go to Failed )

    # -------------------#
    # -- Working State --#
    # -------------------#

    # Internal Working State: Read Input

    # Internal Working State: Data Processing

    # Internal Working State: Set Output

    # Internal Working State: Cleanup -> Go to Read Input

    # Go to Done

    # ( Go to Failed )

    # ----------------#
    # -- Done State --#
    # ----------------#

    # Cleanup

    # Go to Idle

    # ( Go to Failed )

    # ------------------#
    ### Failed State ###
    # ------------------#

    # Shutdown safely


if __name__ == "__main__":
    main()